from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TemplateConsistencyTests(unittest.TestCase):
    def test_all_template_files_use_md_template_extension(self):
        failures: list[str] = []

        for templates_dir in ROOT.glob("*/templates"):
            if not templates_dir.is_dir():
                continue
            for path in templates_dir.iterdir():
                if path.is_dir():
                    failures.append(
                        f"{path.relative_to(ROOT).as_posix()} should be a file, not a directory"
                    )
                    continue
                if not path.name.endswith(".template"):
                    failures.append(
                        f"{path.relative_to(ROOT).as_posix()} must end with .template"
                    )

        if failures:
            self.fail("\n".join(failures))

    def test_templates_are_not_empty(self):
        failures: list[str] = []

        for template in ROOT.rglob("*.md.template"):
            content = template.read_text(encoding="utf-8").strip()
            if not content:
                failures.append(f"{template.relative_to(ROOT).as_posix()} is empty")

        if failures:
            self.fail("\n".join(failures))


if __name__ == "__main__":
    unittest.main()
