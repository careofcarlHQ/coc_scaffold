from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SelfApplicationTrackingTests(unittest.TestCase):
    def test_testing_retrofit_tracking_artifacts_exist(self):
        required_files = [
            "self-application/README.md",
            "self-application/testing-retrofit/AGENTS.md",
            "self-application/testing-retrofit/ci-gate-verification.md",
            "self-application/testing-retrofit/coverage-baseline.md",
            "self-application/testing-retrofit/risk-priority-map.md",
            "self-application/testing-retrofit/testing-checklist.md",
            "self-application/testing-retrofit/coverage-report.md",
        ]

        missing = [path for path in required_files if not (ROOT / path).is_file()]
        if missing:
            joined = "\n".join(f"- {path}" for path in missing)
            self.fail(f"Missing self-application tracking artifacts:\n{joined}")


if __name__ == "__main__":
    unittest.main()
