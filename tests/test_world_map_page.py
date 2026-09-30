import unittest
from pathlib import Path


class WorldMapPageTests(unittest.TestCase):
    def test_world_map_page_contains_map_controls_and_node_layer(self):
        html = Path("web/world-map.html").read_text(encoding="utf-8")
        self.assertIn("World Map", html)
        self.assertIn("leaflet", html.lower())
        self.assertIn("nodes", html.lower())
        self.assertIn("addNode", html)


if __name__ == "__main__":
    unittest.main()
