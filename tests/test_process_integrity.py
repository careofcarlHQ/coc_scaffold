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

TABLE_LINK_PATTERN = re.compile(r"\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|")
BACKTICK_PATH_PATTERN = re.compile(r"`[^`/\\]*[/\\][^`]+`")


class ProcessIntegrityTests(unittest.TestCase):
    def test_readme_index_links_resolve(self):
        failures: list[str] = []

        for scaffold in SCAFFOLDS:
            readme_path = ROOT / scaffold / "README.md"
            content = readme_path.read_text(encoding="utf-8")

            links = TABLE_LINK_PATTERN.findall(content)
            if len(links) < 10:
                failures.append(
                    f"{scaffold}/README.md expected at least 10 table links, found {len(links)}"
                )
                continue

            for raw_link in links:
                link = raw_link.split("#", 1)[0]
                target = (readme_path.parent / link).resolve()
                if not target.exists():
                    failures.append(
                        f"{scaffold}/README.md broken table link: {raw_link}"
                    )

        if failures:
            self.fail("\n".join(failures))

    def test_agents_templates_have_minimum_navigation_contract(self):
        failures: list[str] = []

        for scaffold in SCAFFOLDS:
            agents_template = ROOT / scaffold / "templates" / "AGENTS.md.template"
            content = agents_template.read_text(encoding="utf-8")
            lowered = content.lower()

            if not content.lstrip().startswith("# AGENTS.md"):
                failures.append(
                    f"{scaffold}/templates/AGENTS.md.template must start with '# AGENTS.md'"
                )

            has_mission_or_phase = (
                "## mission" in lowered
                or "## current phase" in lowered
                or "## current stage" in lowered
            )
            if not has_mission_or_phase:
                failures.append(
                    f"{scaffold}/templates/AGENTS.md.template missing mission/current phase section"
                )

            has_sources_section = (
                "read these files" in lowered
                or "read in this order" in lowered
                or "sources of truth" in lowered
                or "source of truth" in lowered
            )
            if not has_sources_section:
                failures.append(
                    f"{scaffold}/templates/AGENTS.md.template missing source navigation section"
                )

            path_refs = BACKTICK_PATH_PATTERN.findall(content)
            if len(path_refs) < 2:
                failures.append(
                    f"{scaffold}/templates/AGENTS.md.template has too few file path references ({len(path_refs)} < 2)"
                )

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
