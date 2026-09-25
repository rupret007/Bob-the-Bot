from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "openclaw-operator-index.md"
README = ROOT / "README.md"
COORDINATION = ROOT / "COORDINATION.md"

DRAFTS = (
    {
        "number": "26",
        "url": "https://github.com/rupret007/Bob-the-Bot/pull/26",
        "branch": "cursor/openclaw-consolidation-fences-f6bd",
        "sha": "b1eec45a2e1693656520412ebfce52157706f353",
        "files": ("COORDINATION.md",),
    },
    {
        "number": "27",
        "url": "https://github.com/rupret007/Bob-the-Bot/pull/27",
        "branch": "cursor/openclaw-operator-docs-7588",
        "sha": "d200c1d7b648fae65dc090609f6c2c3d0cd2b13f",
        "files": (
            "docs/openclaw/README.md",
            "docs/openclaw/operator-guide.md",
            "docs/openclaw/hard-fences.md",
            "docs/openclaw/not-moved.md",
            "tools/openclaw_cli_fallback.py",
            "tests/test_openclaw_cli_fallback.py",
        ),
    },
    {
        "number": "28",
        "url": "https://github.com/rupret007/Bob-the-Bot/pull/28",
        "branch": "cursor/vendor-openclaw-cli-6baa",
        "sha": "fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066",
        "files": (
            "docs/openclaw/operator-notes.md",
            "tools/openclaw/README.md",
            "tools/openclaw/cursor_openclaw.py",
            "tools/openclaw/cursor_api_common.py",
            "tools/openclaw/env_loader.py",
            "tools/openclaw/__init__.py",
            "tests/test_openclaw_cli.py",
        ),
    },
)
ABSENT_FROM_THIS_CHECKOUT = (
    ROOT / "docs" / "openclaw",
    ROOT / "tools" / "openclaw",
    ROOT / "tools" / "openclaw_cli_fallback.py",
)
SECRET_LIKE = re.compile(
    r"(?:CURSOR_API_KEY\s*=\s*\S+|sk-[A-Za-z0-9]{8,}|Bearer\s+[A-Za-z0-9._-]{12,})",
    re.IGNORECASE,
)
LOCAL_PATH = re.compile(
    r"(?:/Users/|/home/|/var/folders/|file://|[A-Za-z]:[\\/]Users[\\/])",
    re.IGNORECASE,
)


def _blob(sha: str, path: str) -> str:
    return f"https://github.com/rupret007/Bob-the-Bot/blob/{sha}/{path}"


class OpenClawOperatorIndexTests(unittest.TestCase):
    def test_entry_points_link_the_index_unmerged_drafts_and_exact_shas(
        self,
    ) -> None:
        readme = README.read_text(encoding="utf-8")
        coordination = COORDINATION.read_text(encoding="utf-8")
        self.assertIn("docs/openclaw-operator-index.md", readme)
        self.assertIn("docs/openclaw-operator-index.md", coordination)
        self.assertIn("not a stack", readme)
        self.assertIn("stops at the Andrea bridge", readme)
        self.assertIn("Stack Ops lane", readme)
        self.assertIn("- Andrea bridge: [draft #26]", readme)
        self.assertIsNone(re.search(r"(?m)^- fences:", readme))
        self.assertIn("not treat #27/#28 as a stack", coordination)
        self.assertIn("stops at the Andrea bridge", coordination)
        self.assertIn("Stack Ops lane", coordination)
        self.assertIn("- Andrea bridge: [draft #26]", coordination)
        self.assertIsNone(re.search(r"(?m)^- fences:", coordination))
        for draft in DRAFTS:
            self.assertIn(draft["url"], readme)
            self.assertIn(draft["url"], coordination)
            self.assertIn(draft["sha"], readme)
            self.assertIn(draft["sha"], coordination)

    def test_index_maps_three_drafts_without_merging_them(self) -> None:
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("This is a map, not a merge.", index)
        self.assertIn("do not merge", index.casefold())
        self.assertIn("legacy", index.casefold())
        self.assertIn("cursor-openclaw-integration", index.casefold())
        self.assertIn("andrea", index.casefold())
        self.assertIn("gateway", index.casefold())
        self.assertIn("secrets", index.casefold())
        self.assertIn("not a stack", index.casefold())
        self.assertIn("alternative leftover drafts", index)
        self.assertIn("only hosted", index)
        self.assertIn("cross-link surface", index)
        self.assertIn("stops at the Andrea bridge", index)
        self.assertIn("| Andrea bridge |", index)
        self.assertIn("### #26 Andrea bridge", index)
        self.assertIsNone(re.search(r"\| fences \|", index))
        self.assertIn("repo-root `.env`", index)
        self.assertIn("cwd `.env`", index)
        self.assertIn("_SCRIPT_DIR.parent.parent", index)
        self.assertIn('Path.cwd() / ".env"', index)
        self.assertIn("override=False", index)
        self.assertNotIn("reads a local dotenv file", index)
        self.assertIn("Gateway and secrets fences are written on the #27 and #28 heads", index)
        self.assertIn("leaves that source-of-truth claim on the #27 head", index)
        self.assertIn("does not vendor that CLI", index)
        self.assertIn("scripts/cursor_openclaw.py", index)
        self.assertIn("BOB_OPENCLAW_INTEGRATION_ROOT", index)
        self.assertIsNone(
            re.search(r"does not contain\s+`cursor_openclaw\.py`", index),
        )
        self.assertIn("Stack Ops specialist lane", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/3", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/11", index)
        self.assertIn(_blob(DRAFTS[1]["sha"], "README.md"), index)
        self.assertIn(_blob(DRAFTS[2]["sha"], "README.md"), index)
        self.assertNotIn("CURSOR_API_KEY=", index)
        for draft in DRAFTS:
            self.assertIn(draft["url"], index)
            self.assertIn(draft["sha"], index)
            self.assertIn(draft["branch"], index)
            for path in draft["files"]:
                self.assertIn(_blob(draft["sha"], path), index)

    def test_this_checkout_does_not_vendor_the_other_draft_trees(self) -> None:
        for path in ABSENT_FROM_THIS_CHECKOUT:
            self.assertFalse(path.exists(), path)

    def test_index_stays_free_of_secrets_and_local_paths(self) -> None:
        for path in (INDEX, README, COORDINATION):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(SECRET_LIKE.search(text), path.name)
            self.assertIsNone(LOCAL_PATH.search(text), path.name)


if __name__ == "__main__":
    unittest.main()
