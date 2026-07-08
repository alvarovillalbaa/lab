import json
import unittest
from pathlib import Path

from lab.routing import providers_for
from lab.validation import validate_spec


ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_experiment_configs_validate(self):
        for path in sorted((ROOT / "configs" / "experiments").glob("*.json")):
            with self.subTest(path=path.name):
                spec = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(validate_spec(spec), [])

    def test_invalid_spec_reports_missing_keys(self):
        issues = validate_spec({"experiment_id": "bad"})
        self.assertIn("missing top-level key: budget", issues)
        self.assertIn("missing top-level key: resources", issues)

    def test_routing_knows_public_serving(self):
        self.assertEqual(providers_for("serving_public")[0], "baseten")


if __name__ == "__main__":
    unittest.main()
