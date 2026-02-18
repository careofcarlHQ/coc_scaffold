from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```", re.MULTILINE)


def markdown_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and "tests" not in path.parts
        and ".venv" not in path.parts
    ]


def should_validate(target: str) -> bool:
    stripped = target.strip()
    if not stripped:
        return False
    if stripped.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return True


class MarkdownLinkTests(unittest.TestCase):
    def test_all_local_markdown_links_resolve(self):
        failures: list[str] = []

        for file_path in markdown_files():
            raw_content = file_path.read_text(encoding="utf-8")
            content = FENCED_CODE_BLOCK_PATTERN.sub("", raw_content)
            for raw_target in LINK_PATTERN.findall(content):
                target = raw_target.split("#", 1)[0].strip()
                if not should_validate(target):
                    continue

                resolved = (file_path.parent / target).resolve()
                if not resolved.exists():
                    relative_file = file_path.relative_to(ROOT).as_posix()
                    failures.append(
                        f"{relative_file} -> {raw_target} (resolved to {resolved})"
                    )

        if failures:
            joined = "\n".join(f"- {entry}" for entry in failures)
            self.fail(f"Broken local links found:\n{joined}")


if __name__ == "__main__":
    unittest.main()
