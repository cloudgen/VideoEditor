# TP-DOC-01 — user document structure. Primary law: requirement-python-readme.
# The badge matches the package string. Every PNG is an absolute https link.
# TP-DOC-03 (catalog paragraph equality) is not this file yet.
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
IMAGE_BASE = "https://raw.githubusercontent.com/cloudgen/VideoTools/main/screenshots/"
GUI_SHOTS = (
    "gui-edit.png",
    "gui-join.png",
    "gui-language.png",
    "gui-self-management.png",
)
RELATED = (
    "https://github.com/Wilgat/VideoJoin",
    "https://pypi.org/project/VideoJoin/",
    "https://github.com/Wilgat/AnimeDlp",
    "https://github.com/Wilgat/ChronicleLogger",
    "https://github.com/Wilgat/VideoSpeed",
    "https://github.com/cloudgen/ciao",
    "https://github.com/cloudgen/ciao-lite",
    "https://github.com/cloudgen/safe-rm",
)
HEADINGS = (
    "Features",
    "Advantages",
    "Quick Installation",
    "Usage",
    "Screenshots",
    "Examples",
    "Platform Compatibility",
    "Related Projects",
    "Contributing",
    "License",
    "Last Update",
)


def _package_version():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    init_text = (ROOT / "src" / "VideoTools" / "__init__.py").read_text(encoding="utf-8")
    py_match = re.search(r'(?m)^version = "([^"]+)"', pyproject)
    init_match = re.search(r'__version__ = "([^"]+)"', init_text)
    return py_match.group(1), init_match.group(1)


class TestReadmeStructure(unittest.TestCase):
    """TP-DOC-01."""

    def test_tp_doc_01_badge_links_headings_and_related_projects(self):
        """TP-DOC-01: badge, absolute picture URLs, headings, clocks, no setup.sh."""
        py_version, init_version = _package_version()
        self.assertEqual(py_version, init_version)
        self.assertIn("Version-" + py_version + "-blue", README)
        self.assertIn("local clock", README)
        self.assertIn("HH:MM:SS", README)
        self.assertIn("00:00.00", README)
        self.assertIn("github/stars/cloudgen/VideoTools", README)
        self.assertNotIn("setup.sh", README)
        self.assertNotIn("sudo pip", README)
        self.assertNotIn("curl | sh", README)
        self.assertNotIn("video.png", README)
        headings = re.findall(r"(?m)^## ([^#\n].*)$", README)
        self.assertEqual(tuple(headings), HEADINGS)
        names = tuple(sorted(path.name for path in (ROOT / "screenshots").glob("*.png")))
        self.assertEqual(names, GUI_SHOTS)
        for name in names:
            self.assertIn(IMAGE_BASE + name, README, name)
        self.assertIsNone(re.search(r"!\[[^\]]*\]\(\.?/?screenshots/", README))
        related = README.split("## Related Projects", 1)[1].split("## Contributing", 1)[0]
        urls = re.findall(r"\((https://[^)]+)\)", related)
        self.assertEqual(tuple(urls), RELATED)


if __name__ == "__main__":
    unittest.main()
