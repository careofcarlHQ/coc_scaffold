from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDS = [
    "greenfield",
    "repo-documentation",
    "refactoring",
    "feature-addition",
    "bug-investigation",
    "testing-retrofit",
    "migration",
    "incident-response",
    "spike",
]
REQUIRED_NUMBERED_GUIDES = [
    "00-philosophy.md",
    "01-process-overview.md",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
]


class ScaffoldStructureTests(unittest.TestCase):
    def test_expected_scaffolds_exist(self):
        for scaffold in SCAFFOLDS:
            scaffold_path = ROOT / scaffold
            self.assertTrue(
                scaffold_path.is_dir(), f"Missing scaffold directory: {scaffold}"
            )

    def test_each_scaffold_has_required_top_level_files(self):
        for scaffold in SCAFFOLDS:
            scaffold_path = ROOT / scaffold
            self.assertTrue(
                (scaffold_path / "README.md").is_file(),
                f"{scaffold} is missing README.md",
            )
            self.assertTrue(
                (scaffold_path / "templates").is_dir(),
                f"{scaffold} is missing templates/ directory",
            )

    def test_each_scaffold_has_numbered_guides_00_to_08(self):
        for scaffold in SCAFFOLDS:
            scaffold_path = ROOT / scaffold
            files = {path.name for path in scaffold_path.glob("*.md")}

            self.assertIn("00-philosophy.md", files, f"{scaffold}: missing 00 guide")
            self.assertIn("01-process-overview.md", files, f"{scaffold}: missing 01 guide")

            for prefix in REQUIRED_NUMBERED_GUIDES[2:]:
                matched = any(name.startswith(f"{prefix}-") for name in files)
                self.assertTrue(matched, f"{scaffold}: missing {prefix}-*.md")

    def test_templates_have_agents_template(self):
        for scaffold in SCAFFOLDS:
            agents_template = ROOT / scaffold / "templates" / "AGENTS.md.template"
            self.assertTrue(
                agents_template.is_file(),
                f"{scaffold}: missing templates/AGENTS.md.template",
            )


if __name__ == "__main__":
    unittest.main()
