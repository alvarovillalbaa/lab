import json
import io
import sys
import tomllib
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from contextlib import redirect_stderr

from lab.workflow import run_smoke, declared_composition
from lab.evidence import submit_execution_evidence


class IntegrationTests(unittest.TestCase):
    def test_legacy_estimate_command_keeps_spec_validation(self):
        from lab.cli import main
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / "configs/experiments/lab_124m_pretrain_smoke.json").read_text())
        spec["budget"]["hard_cap_usd"] = -1
        stderr = io.StringIO()
        with patch.object(Path, "read_text", return_value=json.dumps(spec)), redirect_stderr(stderr):
            self.assertEqual(main(["estimate-cost", "fixture.json"]), 1)
        self.assertIn("budget.hard_cap_usd", stderr.getvalue())

    def test_cpu_workflow_is_explicitly_fixture_based(self):
        result = run_smoke(code_ref="fixture:unit-test")
        self.assertEqual(result["source"], "authored_fixture")
        self.assertEqual(result["record"]["resources"], {"device": "cpu", "gpus": 0})
        self.assertEqual(result["output"]["pair"]["chosen"], "4")
        self.assertEqual(result["planning"]["job_order"], ["cpu-fixture"])
        self.assertNotEqual(result["execution_id"], run_smoke(code_ref="fixture:unit-test")["execution_id"])

    def test_blank_code_identity_fails(self):
        with self.assertRaises(ValueError):
            run_smoke(code_ref="")

    def test_sdk_receives_actual_execution_evidence(self):
        client = Mock()
        client.submit_trace.return_value = 202
        constructor = Mock(return_value=client)
        result = run_smoke(code_ref="fixture:unit-test")
        with patch.dict(sys.modules, {"open_evals_sdk": types.SimpleNamespace(OpenEvalsPythonClient=constructor)}):
            self.assertEqual(submit_execution_evidence(result, endpoint="https://fixture.invalid", api_key="fixture-key"), 202)
        constructor.assert_called_once_with(endpoint="https://fixture.invalid", api_key="fixture-key")
        payload = client.submit_trace.call_args.args[0]
        self.assertEqual(payload["traceId"], result["execution_id"])
        self.assertEqual(payload["output"], result["output"])
        self.assertNotIn("api_key", json.dumps(payload))
        self.assertNotIn("expected_answer", payload["input"])

    def test_sdk_failure_propagates_without_retry(self):
        client = Mock()
        client.submit_trace.side_effect = OSError("fixture failure")
        with patch.dict(sys.modules, {"open_evals_sdk": types.SimpleNamespace(OpenEvalsPythonClient=Mock(return_value=client))}):
            with self.assertRaises(OSError):
                submit_execution_evidence(run_smoke(code_ref="fixture:unit-test"), endpoint="https://fixture.invalid", api_key="fixture-key")
        self.assertEqual(client.submit_trace.call_count, 1)

    def test_profile_pins_match_declared_composition(self):
        root = Path(__file__).resolve().parents[1]
        metadata = tomllib.loads((root / "pyproject.toml").read_text())
        declared = declared_composition()
        self.assertEqual(declared["status"], "candidate")
        requirements = metadata["project"]["dependencies"] + sum(metadata["project"]["optional-dependencies"].values(), [])
        for name in ("experiment-kit", "compute-planner", "model-distillation"):
            self.assertTrue(any(declared["components"][name]["revision"] in req for req in requirements))

    def test_bad_evidence_and_missing_configuration_fail_before_sdk(self):
        with self.assertRaises(ValueError):
            submit_execution_evidence({}, endpoint="", api_key="")
        with self.assertRaises(ValueError):
            submit_execution_evidence({}, endpoint="https://fixture.invalid", api_key="fixture-key")


if __name__ == "__main__":
    unittest.main()
