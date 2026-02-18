from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
NUMBERED_FILE_PATTERN = re.compile(r"^(\d{2})-.*\.md$")


class MarkdownStyleTests(unittest.TestCase):
    def test_markdown_files_start_with_h1(self):
        failures: list[str] = []

        for file_path in ROOT.rglob("*.md"):
            if (
                ".git" in file_path.parts
                or "tests" in file_path.parts
                or ".venv" in file_path.parts
            ):
                continue

            content = file_path.read_text(encoding="utf-8").strip()
            if not content:
                failures.append(f"{file_path.relative_to(ROOT).as_posix()} is empty")
                continue

            first_line = content.splitlines()[0]
            if not first_line.startswith("# "):
                failures.append(
                    f"{file_path.relative_to(ROOT).as_posix()} first line is not an H1: {first_line}"
                )

        if failures:
            self.fail("\n".join(failures))

    def test_numbered_guides_have_matching_h1_prefix(self):
        failures: list[str] = []

        for file_path in ROOT.rglob("*.md"):
            if (
                ".git" in file_path.parts
                or "tests" in file_path.parts
                or ".venv" in file_path.parts
            ):
                continue

            match = NUMBERED_FILE_PATTERN.match(file_path.name)
            if not match:
                continue

            expected_prefix = f"# {match.group(1)}"
            first_line = file_path.read_text(encoding="utf-8").splitlines()[0].strip()
            if not first_line.startswith(expected_prefix):
                failures.append(
                    f"{file_path.relative_to(ROOT).as_posix()} should start with '{expected_prefix}'"
                )

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
