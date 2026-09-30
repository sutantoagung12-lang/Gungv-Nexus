import unittest

from core.daily_skill_frontier import DailySkillFrontier


class DailySkillFrontierTests(unittest.TestCase):
    def setUp(self):
        self.frontier = DailySkillFrontier()

    def test_creates_new_skill_from_frontier_candidate(self):
        result = self.frontier.generate_skill(
            {"id": "web-research", "problem": "discover useful AI workflows"}
        )
        self.assertEqual(result["status"], "proposed")
        self.assertTrue(result["skill"]["id"].startswith("generated-"))

    def test_creates_node_page_for_new_frontier(self):
        node = self.frontier.create_node(
            {"id": "ai-automation", "title": "AI Automation"}
        )
        self.assertEqual(node["type"], "frontier-node")
        self.assertEqual(node["status"], "discovered")

    def test_daily_cycle_is_deterministic_without_external_execution(self):
        result = self.frontier.daily_cycle(
            [{"id": "research", "problem": "find new AI capability"}]
        )
        self.assertEqual(result["policy"], "daily-frontier")
        self.assertEqual(len(result["generated_skills"]), 1)
        self.assertEqual(len(result["nodes"]), 1)


if __name__ == "__main__":
    unittest.main()
