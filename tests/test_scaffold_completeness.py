from pathlib import Path
import re
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

NUMBERED_FILE_PATTERN = re.compile(r"^\d{2}-.*\.md$")


class ScaffoldCompletenessTests(unittest.TestCase):
    def test_readme_index_covers_all_numbered_guides(self):
        failures: list[str] = []

        for scaffold in SCAFFOLDS:
            scaffold_dir = ROOT / scaffold
            readme = scaffold_dir / "README.md"
            content = readme.read_text(encoding="utf-8")

            numbered_guides = sorted(
                path.name
                for path in scaffold_dir.glob("*.md")
                if NUMBERED_FILE_PATTERN.match(path.name)
            )

            for guide in numbered_guides:
                expected_link = f"[{guide}]({guide})"
                if expected_link not in content:
                    failures.append(
                        f"{scaffold}/README.md missing document index link for {guide}"
                    )

            has_templates_index = "[templates/](templates/)" in content
            has_templates_section = "## templates" in content.lower() and "(templates/" in content

            if not (has_templates_index or has_templates_section):
                failures.append(f"{scaffold}/README.md missing templates/ index link")

        if failures:
            self.fail("\n".join(failures))

    def test_process_overview_has_sufficient_phase_depth(self):
        failures: list[str] = []

        for scaffold in SCAFFOLDS:
            process_overview = ROOT / scaffold / "01-process-overview.md"
            content = process_overview.read_text(encoding="utf-8")
            lowered = content.lower()

            phase_mentions = lowered.count("phase")
            lifecycle_mentions = lowered.count("lifecycle")
            numbered_sections = len(re.findall(r"^###\s+\d+\.", content, re.MULTILINE))

            if phase_mentions < 3 and lifecycle_mentions < 1 and numbered_sections < 4:
                failures.append(
                    f"{scaffold}/01-process-overview.md appears shallow (phase={phase_mentions}, lifecycle={lifecycle_mentions}, numbered={numbered_sections})"
                )

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
