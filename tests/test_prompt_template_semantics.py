from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROMPT_SCAFFOLDS = [
    "repo-documentation",
    "refactoring",
    "feature-addition",
    "bug-investigation",
    "migration",
    "testing-retrofit",
    "incident-response",
    "spike",
]
ALL_SCAFFOLDS = [
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

PROMPT_HEADING_PATTERN = re.compile(
    r"^(###\s+Prompt:.*|##\s+Prompt\s+\d+:.*|##\s+.*Prompt\s*)$",
    re.IGNORECASE | re.MULTILINE,
)
PLACEHOLDER_PATTERN = re.compile(r"\{[^{}\n]+\}")


class PromptTemplateSemanticTests(unittest.TestCase):
    def test_prompt_playbooks_have_minimum_structure(self):
        failures: list[str] = []

        for scaffold in PROMPT_SCAFFOLDS:
            path = ROOT / scaffold / "07-agent-prompts.md"
            content = path.read_text(encoding="utf-8")

            prompt_headings = PROMPT_HEADING_PATTERN.findall(content)
            code_fence_count = content.count("```")
            code_block_pairs = code_fence_count // 2

            if len(prompt_headings) < 5:
                failures.append(
                    f"{scaffold}/07-agent-prompts.md has too few prompt sections ({len(prompt_headings)} < 5)"
                )

            if code_block_pairs < len(prompt_headings):
                failures.append(
                    f"{scaffold}/07-agent-prompts.md has fewer code blocks ({code_block_pairs}) than prompt sections ({len(prompt_headings)})"
                )

            if "Tasks:" not in content and "1." not in content:
                failures.append(
                    f"{scaffold}/07-agent-prompts.md lacks actionable task instructions"
                )

        if failures:
            self.fail("\n".join(failures))

    def test_markdown_templates_are_actionable(self):
        failures: list[str] = []

        for scaffold in ALL_SCAFFOLDS:
            templates_dir = ROOT / scaffold / "templates"
            md_templates = sorted(templates_dir.glob("*.md.template"))

            if len(md_templates) < 4:
                failures.append(
                    f"{scaffold}/templates has too few markdown templates ({len(md_templates)} < 4)"
                )
                continue

            for template in md_templates:
                content = template.read_text(encoding="utf-8")
                stripped = content.strip()
                if not stripped.startswith("# "):
                    failures.append(
                        f"{template.relative_to(ROOT).as_posix()} should start with an H1"
                    )
                    continue

                has_placeholder = bool(PLACEHOLDER_PATTERN.search(content))
                has_checklist = "- [ ]" in content
                has_table = "|" in content

                if not (has_placeholder or has_checklist or has_table):
                    failures.append(
                        f"{template.relative_to(ROOT).as_posix()} lacks placeholders/checklists/tables"
                    )

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
