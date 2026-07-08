"""Small distillation primitives for verifier-gated data generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Task:
    task_id: str
    domain: str
    prompt: str
    difficulty: float
    expected_answer: str | None = None


@dataclass(frozen=True)
class TeacherResponse:
    task_id: str
    teacher_id: str
    response: str
    license: str
    allowed_for_distillation: bool


@dataclass(frozen=True)
class VerificationResult:
    task_id: str
    teacher_id: str
    accepted: bool
    verifier: str
    reason: str


@dataclass(frozen=True)
class PreferencePair:
    task_id: str
    chosen: str
    rejected: str
    source: str


def verify_exact_match(task: Task, response: TeacherResponse) -> VerificationResult:
    if not response.allowed_for_distillation:
        return VerificationResult(
            task_id=task.task_id,
            teacher_id=response.teacher_id,
            accepted=False,
            verifier="exact_match",
            reason="teacher output is not allowed for distillation",
        )
    if task.expected_answer is None:
        return VerificationResult(
            task_id=task.task_id,
            teacher_id=response.teacher_id,
            accepted=False,
            verifier="exact_match",
            reason="task has no expected answer",
        )
    accepted = response.response.strip() == task.expected_answer.strip()
    return VerificationResult(
        task_id=task.task_id,
        teacher_id=response.teacher_id,
        accepted=accepted,
        verifier="exact_match",
        reason="matched expected answer" if accepted else "did not match expected answer",
    )


def build_preference_pair(
    task: Task,
    accepted: TeacherResponse,
    rejected: TeacherResponse,
    accepted_result: VerificationResult,
) -> PreferencePair:
    if not accepted_result.accepted:
        raise ValueError("accepted_result must be accepted before building a preference pair")
    if accepted.task_id != task.task_id or rejected.task_id != task.task_id:
        raise ValueError("responses must belong to the task")
    return PreferencePair(
        task_id=task.task_id,
        chosen=accepted.response,
        rejected=rejected.response,
        source=f"{accepted.teacher_id}_over_{rejected.teacher_id}",
    )


def task_from_record(record: dict[str, Any]) -> Task:
    return Task(
        task_id=str(record["task_id"]),
        domain=str(record["domain"]),
        prompt=str(record["prompt"]),
        difficulty=float(record.get("difficulty", 0.0)),
        expected_answer=record.get("expected_answer"),
    )

