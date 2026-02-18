from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

EXPECTED_SCAFFOLDS = {
    "greenfield",
    "repo-documentation",
    "refactoring",
    "feature-addition",
    "bug-investigation",
    "testing-retrofit",
    "migration",
    "incident-response",
    "spike",
}


class ReadmeCrossReferenceTests(unittest.TestCase):
    def test_root_readme_lists_all_scaffolds(self):
        content = README.read_text(encoding="utf-8")
        for scaffold in EXPECTED_SCAFFOLDS:
            self.assertIn(
                f"[{scaffold}/]({scaffold}/)",
                content,
                f"Root README is missing table entry for {scaffold}/",
            )

    def test_root_readme_start_here_links_exist(self):
        content = README.read_text(encoding="utf-8")
        for scaffold in EXPECTED_SCAFFOLDS:
            link = f"[{scaffold}/README.md]({scaffold}/README.md)"
            self.assertIn(link, content, f"Root README missing link: {link}")
            self.assertTrue(
                (ROOT / scaffold / "README.md").exists(),
                f"Missing scaffold README file for {scaffold}",
            )


if __name__ == "__main__":
    unittest.main()
