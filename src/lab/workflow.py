"""A real CPU execution over authored fixtures, not a model experiment."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from importlib.resources import files
from uuid import uuid4

from experiment_kit import validate_record


def declared_composition():
    return json.loads(files("lab").joinpath("composition.json").read_text(encoding="utf-8"))


def run_smoke(*, code_ref: str):
    from compute_planner import Job, providers_for, value_first
    from model_distillation import Task, TeacherResponse, verify_exact_match, build_preference_pair

    started = datetime.now(timezone.utc).isoformat()
    execution_id = str(uuid4())
    record = {"schema_version": 1, "experiment_id": execution_id,
              "kind": "distillation_fixture", "objective": "Exercise component composition on CPU",
              "code_ref": code_ref, "seed": 0, "inputs": [],
              "resources": {"device": "cpu", "gpus": 0}}
    issues = validate_record(record)
    if issues:
        raise ValueError("; ".join(issues))
    task = Task("math-1", "math", "2+2?", 0.1, "4")
    chosen = TeacherResponse(task.task_id, "fixture-a", "4", "MIT", True)
    rejected = TeacherResponse(task.task_id, "fixture-b", "5", "MIT", True)
    pair = build_preference_pair(task, chosen, rejected, verify_exact_match(task, chosen))
    jobs = value_first([Job("cpu-fixture", "distillation", 1, 0, 1)])
    return {"schema_version": 1, "execution_id": execution_id, "source": "authored_fixture",
            "started_at": started, "ended_at": datetime.now(timezone.utc).isoformat(),
            "record": record, "input": {"task_id": task.task_id, "prompt": task.prompt},
            "output": {"pair": asdict(pair)},
            "planning": {"job_order": [job.job_id for job in jobs],
                         "candidate_providers": providers_for("distillation")},
            "declared_composition": declared_composition()}
