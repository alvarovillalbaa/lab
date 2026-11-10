#!/usr/bin/env python3
"""Verify third-stage product routing over the unchanged V1/V2 recovery chain."""
import argparse
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(workspace, map_path):
    lab = workspace / "lab"
    mapping = json.loads(map_path.read_bytes())
    require(mapping["schema_version"] == 3, "Expected V3 product map")
    previous = mapping["previous_manifest"]
    digest = lambda value: hashlib.sha256(value).hexdigest()
    require(digest((lab / previous["path"]).read_bytes()) == previous["sha256"],
            "Historical V2 map changed")
    prior = runpy.run_path(str(lab / "scripts/check-expanded-provenance.py"))["check"](
        workspace, lab / previous["path"])
    environment = dict(os.environ, GIT_NO_LAZY_FETCH="1")

    def local(repository, path):
        require(repository in {p.name for p in workspace.iterdir() if p.is_dir()},
                f"Unknown local repository: {repository}")
        root = (workspace / repository).resolve()
        target = (root / path).resolve()
        require(target.is_relative_to(root), f"Unsafe destination: {path}")
        return target

    @lru_cache(maxsize=None)
    def blob(repository, revision, path):
        return subprocess.check_output(["git", "show", f"{revision}:{path}"],
            cwd=workspace / repository, env=environment, stderr=subprocess.PIPE)

    def inventory(repository, revision):
        return subprocess.check_output(["git", "ls-tree", "-r", "--name-only", revision],
            cwd=workspace / repository, env=environment, text=True,
            stderr=subprocess.PIPE).splitlines()

    manifest = json.loads((lab / "src/lab/composition.json").read_bytes())
    revisions = {name: record["revision"] for name, record in mapping["new_homes"].items()}
    require(len(mapping["changed_owners"]) == 2
            and {r["repository"] for r in mapping["changed_owners"]}
            == {"model-distillation", "model-pretraining"}, "Incomplete changed-owner inventory")
    revisions.update({r["repository"]: r["revision"] for r in mapping["changed_owners"]})
    require(set(mapping["new_homes"]) ==
            {"verification-runtime", "model-architectures", "research-artifacts"},
            "Missing or unexpected new product home")
    for name, revision in revisions.items():
        require(manifest["components"][name]["revision"] == revision,
                f"Composition pin drift: {name}")
    checked = 0
    expected_sections = set()
    for name, home in mapping["new_homes"].items():
        require(len(home["files"]) == len({r["path"] for r in home["files"]}),
                "Duplicate new-home inventory record")
        require(set(inventory(name, home["revision"])) == {r["path"] for r in home["files"]},
                f"Incomplete new-home inventory: {name}")
        for record in home["files"]:
            require(digest(blob(name, home["revision"], record["path"])) == record["sha256"],
                    f"New-home snapshot hash mismatch: {name}/{record['path']}")
            require(local(name, record["path"]).is_file(), "Missing current product file")
            if record["path"].startswith("docs/sources/"):
                require(digest(local(name, record["path"]).read_bytes()) == record["sha256"],
                        "Frozen new-home source changed")
            checked += 1
        lineage = json.loads(blob(name, home["revision"], "docs/sources/lineage.json"))
        for source in lineage.get("sources", lineage.get("original_lab_sections", [])):
            if source.get("repository", "alvarovillalbaa/lab") == "alvarovillalbaa/lab":
                expected_sections.add((name, source["path"], source["start_line"], source["end_line"]))
    intermediate = 0
    for owner in mapping["changed_owners"]:
        name, revision = owner["repository"], owner["revision"]
        content = blob(name, revision, owner["map_path"])
        require(digest(content) == owner["map_sha256"], "Component map changed")
        component = json.loads(content)
        require(component["source_revision"] == owner["source_revision"], "Source revision drift")
        paths = inventory(name, owner["source_revision"])
        require(set(paths) == set(owner["source_inventory"]), "Incomplete previous inventory")
        require(len(component["files"]) == len(paths)
                and {f["source_path"] for f in component["files"]} == set(paths),
                "Orphaned intermediate file")
        for record in component["files"]:
            require(digest(blob(name, owner["source_revision"], record["source_path"]))
                    == record["source_sha256"], "Intermediate source hash mismatch")
            require(record["destinations"], "Unrouted component file")
            for target in record["destinations"]:
                require(digest(blob(target["repository"], revisions[target["repository"]], target["path"]))
                        == target["sha256"], "Destination snapshot hash mismatch")
                require(local(target["repository"], target["path"]).is_file(), "Missing current owner")
                checked += 1
        intermediate += len(paths)
    v2 = json.loads((lab / previous["path"]).read_bytes())
    originals = {f["source_path"]: f for f in v2["files"]}
    require(len(mapping["original_route_overrides"]) == 2
            and {r["source_path"] for r in mapping["original_route_overrides"]}
            == {"src/lab/distillation.py", "tests/test_distillation_scheduler.py"},
            "Incomplete original verification routing")
    for route in mapping["original_route_overrides"]:
        require(originals[route["source_path"]]["source_sha256"] == route["source_sha256"],
                "Original source identity changed")
        require(route["current_destinations"], "Original source lost current owners")
        for target in route["current_destinations"]:
            require(local(target["repository"], target["path"]).is_file(), "Missing original owner")
    actual_sections = {(s["destination_repository"], s["path"], s["start_line"], s["end_line"])
                       for s in mapping["section_routes"]}
    require(len(actual_sections) == len(mapping["section_routes"])
            and actual_sections == expected_sections, "Incomplete original section routing")
    for section in mapping["section_routes"]:
        lines = blob("lab", section["revision"], section["path"]).splitlines(keepends=True)
        start, end = section["start_line"] - 1, section["end_line"]
        require(0 <= start < end <= len(lines), "Invalid section range")
        content = b"".join(lines[start:end])
        require(digest(content) == section["sha256"], "Original section hash mismatch")
        target = section["destination_repository"]
        require(local(target, section["active_contract"]).is_file(), "Missing section contract owner")
        if "destination_path" in section:
            require(local(target, section["destination_path"]).read_bytes() == content,
                    "Archived original section changed")
    fixture = local("research-artifacts", "examples/hello.txt").read_bytes()
    reference = json.loads(local("research-artifacts", "examples/artifact-ref.json").read_bytes())
    require(reference["sha256"] == digest(fixture) and reference["size_bytes"] == len(fixture),
            "Illustrative artifact reference does not match its fixture")
    return {"status": "passed", "original_files": prior["original_files"],
            "previous_stage": prior, "new_homes": len(mapping["new_homes"]),
            "intermediate_files": intermediate, "destination_checks": checked,
            "original_route_refinements": len(mapping["original_route_overrides"]),
            "section_routes": len(mapping["section_routes"]),
            "artifact_reference_fixture": "passed; specification example only",
            "limits": "Local source/provenance only; installed behavior and laptop recovery are separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--map", type=Path, default=Path(__file__).resolve().parents[1]
                        / "docs/sources/repository-split-v3-map.json")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.workspace.resolve(), args.map.resolve()), indent=2))
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as error:
        print(f"Provenance check failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
