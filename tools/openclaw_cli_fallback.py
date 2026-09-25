#!/usr/bin/env python3
"""Thin Bob wrapper for optional OpenClaw CLI fallback.

This wrapper forwards safe operator commands to
Cursor-OpenClaw-Integration/scripts/cursor_openclaw.py when native Cloud Agent
tooling is unavailable.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ALLOWED_COMMANDS = {
    "diagnose",
    "whoami",
    "models",
    "list-agents",
    "agent-status",
    "conversation",
    "artifacts",
    "artifact-download-url",
    "artifact-index",
    "create-agent",
    "followup",
    "stop-agent",
    "stop-all-jobs",
    "delete-agent",
}


def _resolve_integration_script(root: str) -> Path:
    candidate = Path(root).expanduser().resolve() / "scripts" / "cursor_openclaw.py"
    if not candidate.is_file():
        raise ValueError(
            "Could not find scripts/cursor_openclaw.py under "
            "BOB_OPENCLAW_INTEGRATION_ROOT."
        )
    return candidate


def _validate_command(argv: list[str]) -> None:
    if not argv:
        raise ValueError("Usage: openclaw_cli_fallback.py <command> [args...]")
    if argv[0] not in ALLOWED_COMMANDS:
        raise ValueError(
            f"Unsupported command '{argv[0]}'. Allowed: {', '.join(sorted(ALLOWED_COMMANDS))}"
        )


def main() -> int:
    root = (os.getenv("BOB_OPENCLAW_INTEGRATION_ROOT") or "").strip()
    if not root:
        print(
            "BOB_OPENCLAW_INTEGRATION_ROOT is required. Point it to a local "
            "Cursor-OpenClaw-Integration checkout.",
            file=sys.stderr,
        )
        return 2

    try:
        _validate_command(sys.argv[1:])
        script_path = _resolve_integration_script(root)
    except ValueError as err:
        print(str(err), file=sys.stderr)
        return 2

    cmd = [sys.executable, str(script_path), *sys.argv[1:]]
    proc = subprocess.run(cmd, check=False)
    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
