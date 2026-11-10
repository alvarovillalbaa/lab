"""Optional application instrumentation through the existing Open Evals SDK."""
from __future__ import annotations


def submit_execution_evidence(result: dict, *, endpoint: str, api_key: str) -> int:
    if not endpoint or not api_key:
        raise ValueError("explicit service endpoint and project key are required")
    if result.get("source") != "authored_fixture" or result.get("schema_version") != 1:
        raise ValueError("expected an actual Lab CPU smoke result")
    from open_evals_sdk import OpenEvalsPythonClient

    payload = {"traceId": result["execution_id"], "startedAt": result["started_at"],
               "endedAt": result["ended_at"], "status": "completed",
               "input": result["input"], "output": result["output"],
               "metadata": {"source": result["source"], "code_ref": result["record"]["code_ref"],
                            "declared_composition": result["declared_composition"]}}
    return OpenEvalsPythonClient(endpoint=endpoint, api_key=api_key).submit_trace(payload)
