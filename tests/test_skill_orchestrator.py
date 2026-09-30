import unittest

from core.skill_orchestrator import SkillOrchestrator


class SkillOrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.orchestrator = SkillOrchestrator()

    def test_considers_all_registered_skills_and_selects_relevant_ones(self):
        plan = self.orchestrator.plan("audit and fix the GitHub repository, then run tests")

        self.assertEqual(plan["policy"], "all-relevant")
        self.assertEqual(plan["considered_count"], plan["registered_count"])
        self.assertIn("adaptive-task-routing", plan["selected"])
        self.assertIn("qodo-codebase-wisdom", plan["selected"])
        self.assertIn("test-driven-development", plan["selected"])
        self.assertIn("github", plan["selected"])

    def test_never_claims_unavailable_host_skills_were_executed(self):
        plan = self.orchestrator.plan("write and deploy an application")

        self.assertEqual(plan["executed"], [])
        self.assertTrue(plan["requires_host_or_connector_execution"])


if __name__ == "__main__":
    unittest.main()
