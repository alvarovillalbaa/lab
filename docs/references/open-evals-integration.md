# Open Evals integration

Last updated: 2026-11-10

Open Evals owns evaluation. Lab does not add another evaluator service.
The optional `evals` installation profile depends on the SDK package from
[Open Evals PR #1](https://github.com/alvarovillalbaa/open-evals/pull/1), pinned
to its exact candidate commit. The SDK stays owned by open-evals.

```sh
python3 -m pip install '.[compute,distillation,evals]'
```

An application can explicitly submit evidence from its real CPU smoke execution:

```python
import os
from lab.workflow import run_smoke
from lab.evidence import submit_execution_evidence

result = run_smoke(code_ref="your-checkout@exact-commit")
status = submit_execution_evidence(
    result,
    endpoint=os.environ["OPEN_EVALS_URL"],
    api_key=os.environ["OPEN_EVALS_API_KEY"],
)
```

This performs an SDK trace write only when the function is called. Keep the
configured URL explicit and the project key server-held. The client sends
supplied evidence without local redaction; the example payload contains authored
fixtures and excludes credentials. Preserve the original result if delivery fails.
No automatic retry queue is introduced.

The service's existing role/scope checks remain authoritative. SDK installation
does not grant access. Evaluation runs use Open Evals' own workflows; trace
delivery is not scored evaluation. Supplied-output and HTTP-target run profiles
retain their existing capabilities and restrictions. No new API-key evaluation
route, hosted configuration, or private evaluation-lab code is introduced.

[Canonical SDK and privacy contract](https://github.com/alvarovillalbaa/open-evals/blob/d1002d58109156683be3ad4fc394c7cc6c534057/docs/trace-ingestion.md).
