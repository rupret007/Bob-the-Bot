from __future__ import annotations

import argparse
import contextlib
import email.message
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import urllib.request
import urllib.response

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


class OpenClawSafetyTests(unittest.TestCase):
    MUTATIONS = (
        (["create-agent", "--prompt", "test", "--repository", "a/b", "--branch-name", "cursor/test"], "POST", "/v0/agents"),
        (["followup", "--id", "abc123", "--prompt", "test"], "POST", "/v0/agents/abc123/followup"),
        (["stop-agent", "--id", "abc123"], "POST", "/v0/agents/abc123/stop"),
        (["delete-agent", "--id", "abc123"], "DELETE", "/v0/agents/abc123"),
    )

    def parse(self, argv: list[str]) -> argparse.Namespace:
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(sys, "argv", ["cursor_openclaw.py", *argv]):
            return cursor_openclaw.parse_args()

    def test_dotenv_loads_only_repository_root_and_preserves_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            script_dir = root / "tools" / "openclaw"
            script_dir.mkdir(parents=True)
            cwd = Path(temporary) / "unrelated"
            cwd.mkdir()
            (root / ".env").write_text("CURSOR_AUTH_MODE=bearer\nCURSOR_API_KEY=repo\n", encoding="utf-8")
            (cwd / ".env").write_text("CWD_ONLY=unsafe\nCURSOR_AUTH_MODE=basic\nCURSOR_API_KEY=cwd\n", encoding="utf-8")
            with (
                mock.patch.object(cursor_openclaw, "_SCRIPT_DIR", script_dir),
                mock.patch.object(Path, "cwd", return_value=cwd),
                mock.patch.dict(os.environ, {"CURSOR_API_KEY": "process"}, clear=True),
            ):
                cursor_openclaw._load_repo_dotenv()
                self.assertEqual(os.environ["CURSOR_AUTH_MODE"], "bearer")
                self.assertEqual(os.environ["CURSOR_API_KEY"], "process")
                self.assertNotIn("CWD_ONLY", os.environ)

    def test_missing_repository_dotenv_does_not_fall_back_to_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script_dir = root / "repo" / "tools" / "openclaw"
            script_dir.mkdir(parents=True)
            (root / ".env").write_text("CWD_ONLY=unsafe\n", encoding="utf-8")
            with (
                mock.patch.object(cursor_openclaw, "_SCRIPT_DIR", script_dir),
                mock.patch.object(Path, "cwd", return_value=root),
                mock.patch.dict(os.environ, {}, clear=True),
            ):
                cursor_openclaw._load_repo_dotenv()
                self.assertNotIn("CWD_ONLY", os.environ)

    def test_base_url_is_pinned_to_cursor_https_origin(self) -> None:
        for value in (None, "", "https://api.cursor.com", "https://api.cursor.com/"):
            with self.subTest(allowed=value):
                self.assertEqual(cursor_openclaw.normalize_base_url(value), "https://api.cursor.com")
        for value in (
            "http://api.cursor.com", "https://untrusted.invalid", "https://api.cursor.com.untrusted.invalid",
            "https://api.cursor.com@untrusted.invalid", "https://user@api.cursor.com", "https://api.cursor.com:443",
            "https://api.cursor.com/v0", "https://api.cursor.com?target=other", "https://api.cursor.com#fragment",
            "https://api.cursor.com/?target=other", "https://api.cursor.com/#fragment", "//api.cursor.com",
        ):
            with self.subTest(rejected=value), self.assertRaises(ValueError):
                cursor_openclaw.normalize_base_url(value)

    def test_unsafe_environment_and_cli_base_urls_fail_before_request(self) -> None:
        for source in ("environment", "flag"):
            with self.subTest(source=source):
                argv = ["cursor_openclaw.py", "--json"]
                env = {"CURSOR_API_KEY": "test-key"}
                if source == "environment":
                    env["CURSOR_BASE_URL"] = "https://untrusted.invalid"
                else:
                    argv.extend(["--base-url", "https://untrusted.invalid"])
                argv.append("whoami")
                output = io.StringIO()
                with (
                    mock.patch.dict(os.environ, env, clear=True),
                    mock.patch.object(sys, "argv", argv),
                    mock.patch.object(cursor_openclaw, "_load_repo_dotenv"),
                    mock.patch.object(cursor_openclaw.CursorApiClient, "request") as request,
                    contextlib.redirect_stdout(output),
                ):
                    self.assertEqual(cursor_openclaw.main(), 2)
                self.assertIn("other endpoints are not allowed", json.loads(output.getvalue())["error"])
                request.assert_not_called()

    def test_client_rejects_unapproved_origin_before_transport(self) -> None:
        cfg = _cfg()
        cfg.base_url = "https://untrusted.invalid"
        with mock.patch.object(urllib.request, "build_opener") as transport, self.assertRaises(ValueError):
            cursor_openclaw.CursorApiClient(cfg)
        transport.assert_not_called()

    def test_redirects_cannot_forward_authorization_to_another_origin(self) -> None:
        for status in (301, 302, 303, 307, 308):
            with self.subTest(status=status):
                headers = email.message.Message()
                headers["Location"] = "https://untrusted.invalid/collect"
                reply = urllib.response.addinfourl(io.BytesIO(b""), headers, "https://api.cursor.com/v0/me", code=status)
                reply.msg = "Redirect"
                with mock.patch.object(urllib.request.HTTPSHandler, "https_open", return_value=reply) as transport:
                    client = cursor_openclaw.CursorApiClient(_cfg())
                    with self.assertRaisesRegex(ValueError, "redirects are not allowed"):
                        client.request("GET", "/v0/me")
                transport.assert_called_once()
                self.assertEqual(transport.call_args.args[0].full_url, "https://api.cursor.com/v0/me")

    def test_mutations_require_yes_before_any_request(self) -> None:
        for argv, _method, _path in self.MUTATIONS:
            with self.subTest(command=argv[0]):
                args = self.parse(argv)
                with mock.patch.object(cursor_openclaw.CursorApiClient, "request") as request:
                    with self.assertRaisesRegex(ValueError, "requires --yes"):
                        cursor_openclaw.handle(_cfg(), args)
                request.assert_not_called()

    def test_yes_allows_each_confirmed_mutation(self) -> None:
        for argv, method, path in self.MUTATIONS:
            with self.subTest(command=argv[0]):
                args = self.parse([*argv, "--yes"])
                with mock.patch.object(cursor_openclaw.CursorApiClient, "request", return_value=(200, {"id": "abc123"}, "", "bearer")) as request:
                    status, _payload = cursor_openclaw.handle(_cfg(), args)
                self.assertEqual(status, 200)
                request.assert_called_once()
                self.assertEqual(request.call_args.args, (method, path))

    def test_create_and_followup_dry_runs_never_request_even_with_yes(self) -> None:
        for argv, _method, _path in self.MUTATIONS[:2]:
            for confirmation in ([], ["--yes"]):
                with self.subTest(command=argv[0], confirmation=confirmation):
                    args = self.parse([*argv, "--dry-run", *confirmation])
                    with mock.patch.object(cursor_openclaw.CursorApiClient, "request") as request:
                        status, payload = cursor_openclaw.handle(_cfg(), args)
                    self.assertEqual(status, 0)
                    self.assertTrue(payload["dry_run"])
                    self.assertFalse(payload["would_send"])
                    request.assert_not_called()

    def test_stop_all_requires_yes_and_respects_explicit_dry_run(self) -> None:
        listing = {"agents": [{"id": "abc123", "status": "RUNNING", "source": {"repository": "https://github.com/a/b"}}]}
        for flags, should_stop in (([], False), (["--dry-run"], False), (["--yes", "--dry-run"], False), (["--yes"], True)):
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as repo:
                args = self.parse(["stop-all-jobs", "--repo", repo, *flags])
                responses = [(200, listing, "", "bearer"), (200, {}, "", "bearer")]
                with (
                    mock.patch.object(cursor_openclaw, "_detect_repo_origin_url", return_value="https://github.com/a/b"),
                    mock.patch.object(cursor_openclaw.CursorApiClient, "request", side_effect=responses) as request,
                ):
                    status, payload = cursor_openclaw.handle(_cfg(), args)
                self.assertEqual(status, 0)
                self.assertEqual(payload["dry_run"], not should_stop)
                self.assertEqual(payload["eligible_to_stop"], 1)
                self.assertEqual(payload["attempted"], int(should_stop))
                expected = [mock.call("GET", "/v0/agents", query={"limit": "100"})]
                if should_stop:
                    expected.append(mock.call("POST", "/v0/agents/abc123/stop"))
                self.assertEqual(request.call_args_list, expected)

    def test_read_only_commands_do_not_require_yes(self) -> None:
        commands = (
            ["whoami"], ["models"], ["list-agents"], ["agent-status", "--id", "abc123"],
            ["conversation", "--id", "abc123"], ["artifacts", "--id", "abc123"],
            ["artifact-download-url", "--id", "abc123", "--path", "result.txt"],
        )
        for argv in commands:
            with self.subTest(command=argv[0]):
                args = self.parse(argv)
                with mock.patch.object(cursor_openclaw.CursorApiClient, "request", return_value=(200, {}, "", "bearer")) as request:
                    status, _payload = cursor_openclaw.handle(_cfg(), args)
                self.assertEqual(status, 200)
                request.assert_called_once()
                self.assertEqual(request.call_args.args[0], "GET")


if __name__ == "__main__":
    unittest.main()
