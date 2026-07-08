import unittest

from lab.distillation import (
    TeacherResponse,
    Task,
    build_preference_pair,
    verify_exact_match,
)
from lab.scheduler import Job, cheapest_first, value_first, value_per_dollar


class DistillationSchedulerTests(unittest.TestCase):
    def test_exact_match_respects_license_gate(self):
        task = Task("math-1", "math", "2+2?", 0.1, expected_answer="4")
        response = TeacherResponse("math-1", "teacher", "4", "apache-2.0", True)

        result = verify_exact_match(task, response)

        self.assertTrue(result.accepted)

    def test_preference_pair_requires_accepted_result(self):
        task = Task("math-1", "math", "2+2?", 0.1, expected_answer="4")
        chosen = TeacherResponse("math-1", "teacher-a", "4", "apache-2.0", True)
        rejected = TeacherResponse("math-1", "teacher-b", "5", "apache-2.0", True)
        result = verify_exact_match(task, chosen)

        pair = build_preference_pair(task, chosen, rejected, result)

        self.assertEqual(pair.chosen, "4")
        self.assertEqual(pair.rejected, "5")

    def test_value_first_prefers_information_per_risk_adjusted_dollar(self):
        cheap_low_value = Job("cheap", "evals", expected_value=1, expected_cost_usd=1, risk=1)
        useful = Job("useful", "evals", expected_value=10, expected_cost_usd=2, risk=1)

        self.assertGreater(value_per_dollar(useful), value_per_dollar(cheap_low_value))
        self.assertEqual(value_first([cheap_low_value, useful])[0].job_id, "useful")
        self.assertEqual(cheapest_first([useful, cheap_low_value])[0].job_id, "cheap")


if __name__ == "__main__":
    unittest.main()

