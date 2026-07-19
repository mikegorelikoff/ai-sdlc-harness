"""Starting regression tests for the onboarding tutorial fixture."""

import unittest

from app import route


class RouteTests(unittest.TestCase):
    def test_version(self) -> None:
        self.assertEqual(route("/version"), (200, {"version": "1.0"}))

    def test_unknown_path(self) -> None:
        self.assertEqual(route("/missing"), (404, {"error": "not found"}))


if __name__ == "__main__":
    unittest.main()
