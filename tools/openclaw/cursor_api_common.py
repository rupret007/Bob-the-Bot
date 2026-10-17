"""Shared helpers for the vendored Cursor OpenClaw fallback CLI."""

from __future__ import annotations

import json
import re
from typing import Any

AGENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,255}$")
TRANSIENT_TRANSPORT_STATUS = 599
USER_AGENT_OPENCLAW = "cursor-openclaw-vendored/1.0"
TERMINAL_AGENT_STATUSES = frozenset({"FINISHED", "FAILED", "CANCELLED", "STOPPED", "EXPIRED"})


def validate_agent_id(agent_id: str, flag_name: str = "--id") -> None:
    aid = (agent_id or "").strip()
    if not aid:
        raise ValueError(f"{flag_name} cannot be empty.")
    if not AGENT_ID_PATTERN.fullmatch(aid):
        raise ValueError(
            f"Invalid {flag_name} format (use only letters, digits, and ._:-). "
            "If you pasted a URL, pass only the agent id."
        )


def encode_request_json(body: dict[str, Any]) -> bytes:
    try:
        return json.dumps(body, ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as err:
        raise ValueError(f"Request body is not JSON-serializable: {err}") from err


def parse_json_response_body(raw: str, max_preview: int = 2000) -> dict[str, Any]:
    if not raw.strip():
        return {}
    try:
        parsed: Any = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {"_value": parsed}
    except json.JSONDecodeError:
        return {"_non_json_response": True, "body_preview": raw[:max_preview]}


def argv_has_json_flag(argv: list[str] | None = None) -> bool:
    import sys

    argv = argv or sys.argv
    return "--json" in argv
