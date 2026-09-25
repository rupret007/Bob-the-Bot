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
CONDUCTOR_SHA = "3939c3abf9a65225d9c40caa4737e23c1b85bd0c"
CONDUCTOR_FILES = (
    "docs/conductor-standing-order.md",
    "tools/coord_audit.py",
    "tests/test_coord_audit.py",
    "COORDINATION.md",
    "README.md",
    ".github/ISSUE_TEMPLATE/coord.md",
)
ABSENT_FROM_THIS_CHECKOUT = (
    ROOT / "docs" / "openclaw",
    ROOT / "docs" / "conductor-standing-order.md",
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
        self.assertIn("coord: rupret007/Bob-the-Bot", readme)
        self.assertIn("3939c3abf9a65225d9c40caa4737e23c1b85bd0c", readme)
        self.assertIn("This checkout's", readme)
        self.assertIn("auditor does not", readme)
        self.assertIn("are not written on the #25 standing order", readme)
        self.assertIn("- agent: none | codex | grok | claude", coordination)
        self.assertIsNone(re.search(r"(?m)^- fences:", readme))
        self.assertIn("not treat #27/#28 as a stack", coordination)
        self.assertIn("stops at the Andrea bridge", coordination)
        self.assertIn("Stack Ops lane", coordination)
        self.assertIn("- Andrea bridge: [draft #26]", coordination)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/22", coordination)
        self.assertIn("3939c3abf9a65225d9c40caa4737e23c1b85bd0c", coordination)
        self.assertIn("This PR does not stack it.", coordination)
        self.assertIn("This checkout's auditor does not.", coordination)
        self.assertIn("dual_active_lease", coordination)
        self.assertIn("webjam_dual_active_lease", coordination)
        self.assertIn("are not written on the #25 standing order", coordination)
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
        self.assertIn("command check reads `sys.argv[1:]`", index)
        self.assertIn("An empty argument list is rejected.", index)
        self.assertIn("first of those tokens must be in `ALLOWED_COMMANDS`", index)
        self.assertIn("The full argument list is forwarded unchanged.", index)
        self.assertIn("`artifact-index` is in that allowlist.", index)
        self.assertIn(
            "does not register an `artifact-index` subcommand",
            index,
        )
        self.assertIn(
            "missing or blank `CURSOR_API_KEY` makes every #28 subcommand except `diagnose` raise `CURSOR_API_KEY is required.`",
            index,
        )
        self.assertIn("`diagnose` still runs without that key.", index)
        self.assertIn(
            "sole `--version` or `-V` returns before the key check.",
            index,
        )
        self.assertIn("The #27 wrapper does not read `CURSOR_API_KEY`.", index)
        self.assertIn(
            "A sole `--version` or `-V` is rejected because those tokens are not in `ALLOWED_COMMANDS`.",
            index,
        )
        self.assertIn("The wrapper has no dry-run of its own.", index)
        self.assertIn(
            "A missing or blank `BOB_OPENCLAW_INTEGRATION_ROOT` prints to stderr and",
            index,
        )
        self.assertIn("returns exit status 2.", index)
        self.assertIn("The wrapper does not load dotenv files.", index)
        self.assertIn(
            "The #28 CLI does not read `BOB_OPENCLAW_INTEGRATION_ROOT`.",
            index,
        )
        self.assertIn(
            "`create-agent --dry-run` and `followup --dry-run` return `would_send: False` and do not POST.",
            index,
        )
        self.assertIn(
            "`stop-all-jobs` stays dry-run unless `--yes` is present (`dry_run = bool(args.dry_run) or not bool(args.yes)`).",
            index,
        )
        self.assertIn(
            "returns HTTP-style status `409` and does not POST stops.",
            index,
        )
        self.assertIn("`diagnose --show-key` previews the first two and last two characters of", index)
        self.assertIn("the preview is `***`.", index)
        self.assertIsNone(
            re.search(r"does not contain\s+`cursor_openclaw\.py`", index),
        )
        self.assertIn("Stack Ops specialist lane", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/22", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/3", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/11", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/issues/6", index)
        self.assertIn("https://github.com/rupret007/Bob-the-Bot/pull/25", index)
        self.assertIn("3939c3abf9a65225d9c40caa4737e23c1b85bd0c", index)
        self.assertIn(
            "still allows only `none`, `codex`, `grok`, and `claude`",
            index,
        )
        self.assertIn("`gemini` and `minimax` appear only on that unmerged #25 head.", index)
        self.assertIn("does not merge, rebase, or vendor that tree", index)
        self.assertNotIn("| Conductor", index)
        for path in CONDUCTOR_FILES:
            self.assertIn(_blob(CONDUCTOR_SHA, path), index)
        self.assertIn(
            '`CONDUCTOR_AGENTS = frozenset({"codex", "claude", "gemini", "minimax", "grok"})`',
            index,
        )
        self.assertIn(
            '`ALLOWED_AGENTS = frozenset({"none"}) | CONDUCTOR_AGENTS`',
            index,
        )
        self.assertIn('`WEBJAM_REPO = "rupret007/webjam"`', index)
        self.assertIn("`dual_active_lease`", index)
        self.assertIn("`webjam_dual_active_lease`", index)
        self.assertIn(
            '`ALLOWED_AGENTS = frozenset({"none", "codex", "grok", "claude"})`',
            index,
        )
        self.assertIn("It does not define `CONDUCTOR_AGENTS` or `WEBJAM_REPO`.", index)
        self.assertIn(
            "It does not emit `dual_active_lease` or `webjam_dual_active_lease`.",
            index,
        )
        self.assertIn(
            "They are not written on the #25 standing order.",
            index,
        )
        self.assertIn("does not mention Band", index)
        self.assertIn("Thin Front Door + Silent Parallel Specialists", index)
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

    def test_this_checkout_auditor_does_not_vendor_the_25_conductor_contract(
        self,
    ) -> None:
        audit = (ROOT / "tools" / "coord_audit.py").read_text(encoding="utf-8")
        self.assertIn(
            'ALLOWED_AGENTS = frozenset({"none", "codex", "grok", "claude"})',
            audit,
        )
        self.assertNotIn("CONDUCTOR_AGENTS", audit)
        self.assertNotIn("WEBJAM_REPO", audit)
        self.assertNotIn("dual_active_lease", audit)
        self.assertNotIn("webjam_dual_active_lease", audit)
        template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "coord.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("gemini", template)
        self.assertNotIn("minimax", template)
        self.assertNotIn("webjam", template.casefold())

    def test_index_stays_free_of_secrets_and_local_paths(self) -> None:
        for path in (INDEX, README, COORDINATION):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(SECRET_LIKE.search(text), path.name)
            self.assertIsNone(LOCAL_PATH.search(text), path.name)


if __name__ == "__main__":
    unittest.main()
