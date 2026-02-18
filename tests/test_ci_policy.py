from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "scaffold-validation.yml"


class CiPolicyTests(unittest.TestCase):
    def test_workflow_enforces_required_quality_gates(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("pull_request:", content)
        self.assertIn("python -m coverage run", content)
        self.assertIn("python -m coverage report", content)

        match = re.search(r"--fail-under=(\d+)", content)
        self.assertIsNotNone(match, "Coverage floor (--fail-under) is missing")

        floor = int(match.group(1))
        self.assertGreaterEqual(
            floor,
            80,
            f"Coverage floor is too low ({floor}); expected at least 80",
        )


if __name__ == "__main__":
    unittest.main()
