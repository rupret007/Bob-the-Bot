from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "openclaw-operator-index.md"
README = ROOT / "README.md"
COORDINATION = ROOT / "COORDINATION.md"

DRAFT_URLS = (
    "https://github.com/rupret007/Bob-the-Bot/pull/26",
    "https://github.com/rupret007/Bob-the-Bot/pull/27",
    "https://github.com/rupret007/Bob-the-Bot/pull/28",
)
SECRET_LIKE = re.compile(
    r"(?:CURSOR_API_KEY\s*=\s*\S+|sk-[A-Za-z0-9]{8,}|Bearer\s+[A-Za-z0-9._-]{12,})",
    re.IGNORECASE,
)
LOCAL_PATH = re.compile(
    r"(?:/Users/|/home/|/var/folders/|file://|[A-Za-z]:[\\/]Users[\\/])",
    re.IGNORECASE,
)


class OpenClawOperatorIndexTests(unittest.TestCase):
    def test_entry_points_link_the_index_and_unmerged_drafts(self) -> None:
        readme = README.read_text(encoding="utf-8")
        coordination = COORDINATION.read_text(encoding="utf-8")
        self.assertIn("docs/openclaw-operator-index.md", readme)
        self.assertIn("docs/openclaw-operator-index.md", coordination)
        for url in DRAFT_URLS:
            self.assertIn(url, readme)
            self.assertIn(url, coordination)

    def test_index_maps_three_drafts_without_merging_them(self) -> None:
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("This is a map, not a merge.", index)
        self.assertIn("do not merge", index.casefold())
        self.assertIn("legacy", index.casefold())
        self.assertIn("cursor-openclaw-integration", index.casefold())
        self.assertIn("andrea", index.casefold())
        self.assertIn("gateway", index.casefold())
        self.assertIn("secrets", index.casefold())
        for url in DRAFT_URLS:
            self.assertIn(url, index)
        self.assertNotIn("tools/openclaw/cursor_openclaw.py", index)
        self.assertNotIn("tools/openclaw_cli_fallback.py", index)

    def test_index_stays_free_of_secrets_and_local_paths(self) -> None:
        for path in (INDEX, README, COORDINATION):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(SECRET_LIKE.search(text), path.name)
            self.assertIsNone(LOCAL_PATH.search(text), path.name)


if __name__ == "__main__":
    unittest.main()
