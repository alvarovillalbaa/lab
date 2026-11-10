#!/usr/bin/env python3
"""Check local recovery provenance without installing, fetching or changing repos.

Run from any directory with --workspace pointing to the explicitly supplied
directory containing Lab and the component checkouts. This is recovery tooling,
not an application dependency on sibling source trees.
"""

import argparse
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def digest(content):
    return hashlib.sha256(content).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(workspace, map_path):
    mapping = json.loads(map_path.read_bytes())
    git_environment = dict(os.environ, GIT_NO_LAZY_FETCH="1")
    require(mapping["schema_version"] == 2, "Expected V2 migration map")
    aliases = {
        a["former_repository"].split("/")[-1]:
        a["canonical_repository"].split("/")[-1]
        for a in mapping["aliases"]
    }

    def canonical(repository):
        name = repository.split("/")[-1]
        return aliases.get(name, name)

    def local(repository, path):
        root = (workspace / canonical(repository)).resolve()
        target = (root / path).resolve()
        require(target.is_relative_to(root), f"Unsafe mapped path: {path}")
        return target

    @lru_cache(maxsize=None)
    def blob(repository, revision, path):
        return subprocess.check_output(
            ["git", "-C", str(workspace / canonical(repository)),
             "show", f"{revision}:{path}"], stderr=subprocess.PIPE,
            env=git_environment,
        )

    def inventory(repository, revision):
        return subprocess.check_output(
            ["git", "-C", str(workspace / canonical(repository)),
             "ls-tree", "-r", "--name-only", revision], text=True,
            stderr=subprocess.PIPE,
            env=git_environment,
        ).splitlines()

    def same(content, expected, label):
        require(digest(content) == expected, f"Hash mismatch: {label}")

    destination_count = 0

    def destination(record, revisions=None):
        nonlocal destination_count
        repository, path = record["repository"], record["path"]
        require(local(repository, path).is_file(), f"Missing owner: {repository}/{path}")
        if record.get("role", "").startswith("frozen_"):
            same(local(repository, path).read_bytes(), record["sha256"],
                 f"current archive {repository}/{path}")
        if revisions and "sha256" in record:
            same(blob(repository, revisions[canonical(repository)], path),
                 record["sha256"], f"destination snapshot {repository}/{path}")
        destination_count += 1

    lab = workspace / "lab"
    previous = mapping["previous_manifest"]
    previous_bytes = (lab / previous["path"]).read_bytes()
    same(previous_bytes, previous["sha256"], "unchanged V1 manifest")
    same(blob("lab", previous["lab_destination_snapshot_revision"], previous["path"]),
         previous["sha256"], "V1 manifest at its original migration commit")
    v1 = json.loads(previous_bytes)
    require(mapping["source_revision"] == v1["source_revision"], "Source revision changed")
    require(mapping["original_main"] == v1["original_main"], "Original main changed")
    original = {f["source_path"]: f for f in v1["files"]}
    expanded = {f["source_path"]: f for f in mapping["files"]}
    require(len(original) == len(v1["files"]) == 57, "V1 inventory must have 57 unique files")
    require(len(expanded) == len(mapping["files"]) == mapping["original_file_count"],
            "Duplicate V2 source record")
    require(set(original) == set(expanded) == set(inventory("lab", v1["source_revision"])),
            "Orphaned or unexpected original source file")
    for path, old in original.items():
        same(blob("lab", v1["source_revision"], path), old["source_sha256"], path)
        require(expanded[path]["source_sha256"] == old["source_sha256"],
                f"V2 changed original hash: {path}")
        for target in old["destinations"]:
            revision = target.get("revision") or previous["lab_destination_snapshot_revision"]
            same(blob(target["repository"], revision, target["path"]),
                 target["sha256"], f"V1 destination {target['path']}")
        require(expanded[path]["current_destinations"], f"No current owner: {path}")
        for target in expanded[path]["current_destinations"]:
            destination(target)

    registry = json.loads((lab / mapping["alias_registry"]).read_bytes())
    for alias in mapping["aliases"]:
        matches = [a for a in registry["renames"]
                   if a["former_repository"] == alias["former_repository"]]
        require(len(matches) == 1, "Missing or duplicate historical alias")
        require(all(matches[0].get(k) == value for k, value in alias.items()),
                f"Alias identity drift: {alias['former_repository']}")
        inventory(alias["canonical_repository"], alias["pre_expansion_revision"])

    intermediate_count = 0
    for ref in mapping["second_stage_maps"]:
        content = blob(ref["repository"], ref["revision"], ref["path"])
        same(content, ref["sha256"], f"pinned component map {ref['repository']}")
        component = json.loads(content)
        require(component["source_revision"] == ref["source_revision"], "Component source drift")
        require(component["source_repository"] == ref["source_repository"], "Component owner drift")
        paths = inventory(ref["source_repository"], ref["source_revision"])
        require(len(ref["source_inventory"]) == len(set(ref["source_inventory"]))
                and set(paths) == set(ref["source_inventory"]), "Incomplete intermediate inventory")
        records = component.get("files", component.get("file_migrations", []))
        for record in records:
            same(blob(ref["source_repository"], ref["source_revision"], record["source_path"]),
                 record["source_sha256"], f"intermediate source {record['source_path']}")
        routes = component["files"] if ref["kind"] == "scope_expansion" else ref["complete_routes"]
        require(len(routes) == len(paths) and {r["source_path"] for r in routes} == set(paths),
                "Orphaned second-stage source")
        for route in routes:
            require(route["destinations"], f"Unrouted intermediate source: {route['source_path']}")
            for target in route["destinations"]:
                destination(target, ref["destination_snapshot_revisions"])
        if ref["kind"] == "tokenizer_boundary":
            for record in records:
                for section in record.get("section_migrations", []):
                    source = blob(ref["source_repository"], ref["source_revision"],
                                  record["source_path"]).decode().splitlines()
                    require(source[section["start_line"] - 1] == section["heading"],
                            "Tokenizer section heading moved")
                    require(section["start_line"] <= section["end_line"] <= len(source),
                            "Tokenizer section range invalid")
        if ref["kind"] == "economics_extraction":
            for record in records:
                same(blob(ref["repository"], ref["exact_extraction_revision"],
                          record["destination_path"]), record["source_sha256"],
                     f"exact initial economics snapshot {record['source_path']}")
            correction_ref = ref["correction_manifest"]
            correction_bytes = blob(ref["repository"], correction_ref["revision"],
                                    correction_ref["path"])
            same(correction_bytes, correction_ref["sha256"], "economics correction manifest")
            correction = json.loads(correction_bytes)
            require(correction["initial_snapshot_commit"] == ref["exact_extraction_revision"],
                    "Economics exact snapshot was redefined")
            require(correction["source_revision"] == ref["source_revision"],
                    "Economics correction source drift")
            require({f["source_path"] for f in correction["files"]}
                    == {f["source_path"] for f in records}, "Economics correction coverage drift")
            for record in correction["files"]:
                same(blob(ref["repository"], correction_ref["revision"],
                          record["destination_path"]), record["destination_sha256"],
                     f"corrected economics snapshot {record['destination_path']}")
        intermediate_count += len(paths)

    for section in mapping["section_routes"]:
        lines = blob("lab", v1["source_revision"], section["source_path"]).splitlines(keepends=True)
        start, end = section["start_line"] - 1, section["end_line"]
        require(0 <= start < end <= len(lines), "Invalid original section range")
        require(lines[start].decode().strip() == section["heading"], "Original heading drift")
        same(b"".join(lines[start:end]), section["sha256"], section["heading"])
        for target in section["destinations"]:
            destination(target)
    for home in mapping["current_homes"]:
        require(local(home, "README.md").is_file(), f"Missing component home: {home}")
    return {"status": "passed", "original_files": len(original),
            "second_stage_maps": len(mapping["second_stage_maps"]),
            "intermediate_files": intermediate_count,
            "section_routes": len(mapping["section_routes"]),
            "destination_checks": destination_count,
            "history_aliases": len(mapping["aliases"]),
            "limits": "Local structural provenance only; no network, runtime or laptop recovery proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--map", type=Path, default=Path(__file__).resolve().parents[1]
                        / "docs/sources/repository-split-v2-map.json")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.workspace.resolve(), args.map.resolve()), indent=2))
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as error:
        print(f"Provenance check failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
