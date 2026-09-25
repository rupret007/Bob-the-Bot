from __future__ import annotations

import argparse
import unittest

from tools.openclaw import cursor_openclaw


def _cfg() -> cursor_openclaw.Config:
    return cursor_openclaw.Config(
        base_url="https://api.cursor.com",
        api_key="test-key",
        auth_mode="auto",
        timeout_seconds=5,
        retries=0,
        retry_backoff_seconds=0.01,
        output_json=True,
    )


class OpenClawCliTests(unittest.TestCase):
    def test_parse_bool_accepts_expected_values(self) -> None:
        self.assertTrue(cursor_openclaw.parse_bool("true"))
        self.assertTrue(cursor_openclaw.parse_bool("YES"))
        self.assertFalse(cursor_openclaw.parse_bool("false"))
        self.assertFalse(cursor_openclaw.parse_bool("0"))
        with self.assertRaisesRegex(ValueError, "Invalid boolean value"):
            cursor_openclaw.parse_bool("maybe")

    def test_normalize_base_url_rejects_non_http(self) -> None:
        with self.assertRaisesRegex(ValueError, "must start with http"):
            cursor_openclaw.normalize_base_url("ftp://example.com")
        self.assertEqual(
            cursor_openclaw.normalize_base_url("https://api.cursor.com/"),
            "https://api.cursor.com",
        )

    def test_require_one_of(self) -> None:
        with self.assertRaisesRegex(ValueError, "Provide --repository or --pr-url"):
            cursor_openclaw.require_one_of("", "")
        with self.assertRaisesRegex(ValueError, "only one"):
            cursor_openclaw.require_one_of("a/b", "https://github.com/a/b/pull/1")
        cursor_openclaw.require_one_of("a/b", "")
        cursor_openclaw.require_one_of("", "https://github.com/a/b/pull/1")

    def test_create_agent_dry_run_never_posts(self) -> None:
        args = argparse.Namespace(
            command="create-agent",
            prompt="ship it",
            repository="rupret007/Bob-the-Bot",
            ref="main",
            pr_url="",
            model="default",
            branch_name="cursor/test",
            auto_create_pr=False,
            open_as_cursor_github_app=False,
            skip_reviewer_request=False,
            dry_run=True,
        )
        status, payload = cursor_openclaw.handle(_cfg(), args)
        self.assertEqual(status, 0)
        self.assertTrue(payload["dry_run"])
        self.assertFalse(payload["would_send"])
        self.assertEqual(payload["payload"]["target"]["branchName"], "cursor/test")

    def test_followup_dry_run_never_posts(self) -> None:
        args = argparse.Namespace(
            command="followup",
            id="abc123",
            prompt="status?",
            dry_run=True,
        )
        status, payload = cursor_openclaw.handle(_cfg(), args)
        self.assertEqual(status, 0)
        self.assertTrue(payload["dry_run"])
        self.assertFalse(payload["would_send"])
        self.assertEqual(payload["agent_id"], "abc123")

    def test_diagnose_reports_policy_fences(self) -> None:
        args = argparse.Namespace(command="diagnose", show_key=False)
        status, payload = cursor_openclaw.handle(_cfg(), args)
        self.assertEqual(status, 0)
        self.assertTrue(payload["policy"]["native_cloud_agents_preferred"])
        self.assertTrue(payload["policy"]["no_andrea_sync"])
        self.assertTrue(payload["policy"]["no_secret_bootstrapping"])
        self.assertTrue(payload["policy"]["no_auto_send"])


if __name__ == "__main__":
    unittest.main()
