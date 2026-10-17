from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import openclaw_cli_fallback


class OpenClawCliFallbackTests(unittest.TestCase):
    def test_validate_command_rejects_empty_argv(self) -> None:
        with self.assertRaisesRegex(ValueError, "Usage:"):
            openclaw_cli_fallback._validate_command([])

    def test_validate_command_rejects_unknown_command(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported command"):
            openclaw_cli_fallback._validate_command(["not-a-command"])

    def test_validate_command_accepts_known_command(self) -> None:
        openclaw_cli_fallback._validate_command(["list-agents", "--limit", "5"])

    def test_validate_command_rejects_artifact_index(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported command 'artifact-index'"):
            openclaw_cli_fallback._validate_command(["artifact-index"])

    def test_main_forwards_mutating_commands_and_returns_exit_status(self) -> None:
        commands = (
            ["create-agent", "--prompt", "Inspect the repository"],
            ["followup", "--id", "agent-123", "--prompt", "Continue"],
            ["stop-agent", "--id", "agent-123"],
            ["stop-all-jobs"],
            ["delete-agent", "--id", "agent-123"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "scripts" / "cursor_openclaw.py"
            script.parent.mkdir(parents=True)
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            for argv in commands:
                with self.subTest(command=argv[0]):
                    with patch.dict(os.environ, {"BOB_OPENCLAW_INTEGRATION_ROOT": tmp}), patch.object(
                        sys, "argv", ["openclaw_cli_fallback.py", *argv]
                    ), patch.object(openclaw_cli_fallback.subprocess, "run") as run:
                        run.return_value.returncode = 7
                        self.assertEqual(openclaw_cli_fallback.main(), 7)
                        run.assert_called_once_with(
                            [sys.executable, str(script.resolve()), *argv], check=False
                        )

    def test_resolve_integration_script_requires_cursor_openclaw(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "Could not find"):
                openclaw_cli_fallback._resolve_integration_script(tmp)

    def test_resolve_integration_script_returns_expected_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "scripts" / "cursor_openclaw.py"
            script.parent.mkdir(parents=True, exist_ok=True)
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            resolved = openclaw_cli_fallback._resolve_integration_script(tmp)
            self.assertEqual(resolved, script.resolve())


if __name__ == "__main__":
    unittest.main()
