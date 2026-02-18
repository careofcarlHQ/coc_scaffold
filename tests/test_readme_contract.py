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


class ReadmeContractTests(unittest.TestCase):
    def test_each_scaffold_readme_has_operator_sections(self):
        failures: list[str] = []
        for scaffold in SCAFFOLDS:
            readme = ROOT / scaffold / "README.md"
            content = readme.read_text(encoding="utf-8").lower()

            if not (
                "## when to use this scaffold" in content
                or "## who is this for?" in content
            ):
                failures.append(
                    f"{scaffold}/README.md missing audience section (when-to-use or who-is-this-for)"
                )

            if "## how to use this scaffold" not in content:
                failures.append(
                    f"{scaffold}/README.md missing section: ## how to use this scaffold"
                )

            if "document index" not in content:
                failures.append(f"{scaffold}/README.md missing document index section")

            if "(templates/)" not in content and "## templates" not in content:
                failures.append(
                    f"{scaffold}/README.md missing templates guidance (templates section or templates/ link)"
                )

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
