# Open Evals integration

Last updated: 2026-11-10

Open Evals owns reusable evaluation definitions/results/gates and system-prompt
improvement. Lab's optional `evals` selector depends on the standalone Python
SDK package inside open-evals. Follow the
[composition manifest](../../src/lab/composition.json) for its exact selected
source revision and review PR; packaging does not create a separate evaluator.

For the current CPU fixture and an optional SDK connection:

```sh
python3 -m pip install '.[compute,distillation,evals]'
```

An application may explicitly send evidence from an actual fixture execution:

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

The result identifies authored responses and a hypothetical GPU-cost calculation,
with `observed_billing: false`. Sending the trace does not turn those fixtures
into model outputs, billing observations or a scored evaluation run.

Keep the service root explicit and the key server-held. The SDK sends supplied
evidence without local redaction; preserve the source result if delivery fails.
No automatic retry queue is introduced. Existing role/scope checks remain
authoritative; installing a client grants no service access.

Research-controller is a planned consumer of training and evaluation
adapters. It owns bounded model-research sequencing and promotion policy.
Open Evals remains the scoring and prompt-improvement owner, and Lab remains
an integration consumer. Inference-benchmarks owns performance workloads/
measurements and can link quality-evaluation outcomes without cloning an
evaluation engine.

The [expanded installed result](../results/2026/11-10/expanded-installed-package.md)
records the current client/package/profile proof and its limits. Mocked transport
is distinct from live hosted/service acceptance.
[Canonical Open Evals documentation](https://github.com/alvarovillalbaa/open-evals)
owns service contracts and privacy behavior at the selected source revision.
