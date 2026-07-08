import unittest

from lab.costing import estimate_from_spec


class CostingTests(unittest.TestCase):
    def test_estimate_from_spec_has_positive_flops(self):
        spec = {
            "model": {"parameters": 124_000_000},
            "training": {"tokens_target": 500_000_000},
            "resources": {
                "gpus": 1,
                "gpu_tflops": 82,
                "gpu_hourly_usd": 0.69,
                "utilization": 0.35,
            },
            "budget": {"overhead_multiplier": 2.0},
        }

        estimate = estimate_from_spec(spec)

        self.assertGreater(estimate.training_flops, 0)
        self.assertGreater(estimate.raw_gpu_hours, 0)
        self.assertGreater(estimate.realistic_cost_usd, estimate.raw_cost_usd)


if __name__ == "__main__":
    unittest.main()

