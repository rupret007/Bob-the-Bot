#!/usr/bin/env python3
"""Validate a Bob-the-Bot coordination-issue JSON snapshot without trusting it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

SCHEMA = "bob.coordination-audit/v1"
REQUIRED_FIELDS = frozenset(
    {
        "repo",
        "agent",
        "sha",
        "claimed_scope",
        "completed_scope",
        "holds",
        "evidence",
        "next_action",
        "updated",
        "lease_until",
    }
)
ALLOWED_FIELDS = REQUIRED_FIELDS | {"branch", "pr", "hosted_status"}
ALLOWED_AGENTS = frozenset({"none", "codex", "grok", "claude"})

_FIELD_LINE = re.compile(r"^- ([a-z][a-z0-9_]*):(?: (.*))?$")
_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_LOCAL_PATH = re.compile(
    r"(?:/Users/|/home/|/var/folders/|/tmp/|file://|[A-Za-z]:[\\/]Users[\\/])",
    re.IGNORECASE,
)


def _parse_timestamp(value: str) -> datetime | None:
    candidate = value.strip()
    if not candidate:
        return None
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _parse_body(body: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    errors: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        match = _FIELD_LINE.fullmatch(line)
        if match is None:
            errors.append("unstructured_body_line")
            continue
        key, value = match.group(1), match.group(2) or ""
        if key in fields:
            errors.append("duplicate_field")
            continue
        fields[key] = value.strip()
        if key not in ALLOWED_FIELDS:
            errors.append("unknown_field")
    return fields, errors


def _label_names(raw_labels: Any) -> set[str]:
    if not isinstance(raw_labels, list):
        return set()
    names: set[str] = set()
    for label in raw_labels:
        if isinstance(label, str):
            names.add(label)
        elif isinstance(label, dict) and isinstance(label.get("name"), str):
            names.add(label["name"])
    return names


def _issue_number(issue: dict[str, Any]) -> int | None:
    number = issue.get("number")
    return number if isinstance(number, int) and number > 0 else None


def _error(issue: dict[str, Any], code: str) -> dict[str, int | str | None]:
    return {"issue": _issue_number(issue), "code": code}


def audit_snapshot(
    snapshot: Any,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return a value-redacted contract receipt for one issue-list snapshot."""
    checked_at = now or datetime.now(timezone.utc)
    if checked_at.tzinfo is None or checked_at.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    errors: list[dict[str, int | str | None]] = []
    if not isinstance(snapshot, list):
        return {
            "schema": SCHEMA,
            "passed": False,
            "issue_count": 0,
            "error_count": 1,
            "errors": [{"issue": None, "code": "snapshot_not_array"}],
        }

    seen_numbers: set[int] = set()
    seen_repos: set[str] = set()
    for item in snapshot:
        if not isinstance(item, dict):
            errors.append({"issue": None, "code": "issue_not_object"})
            continue
        issue = item
        number = _issue_number(issue)
        if number is None:
            errors.append(_error(issue, "invalid_issue_number"))
        elif number in seen_numbers:
            errors.append(_error(issue, "duplicate_issue_number"))
        else:
            seen_numbers.add(number)

        if issue.get("state") != "OPEN":
            errors.append(_error(issue, "issue_not_open"))
        if "coord" not in _label_names(issue.get("labels")):
            errors.append(_error(issue, "coord_label_missing"))

        body = issue.get("body")
        if not isinstance(body, str):
            errors.append(_error(issue, "body_missing"))
            continue
        fields, body_errors = _parse_body(body)
        errors.extend(_error(issue, code) for code in body_errors)
        for field in sorted(REQUIRED_FIELDS - fields.keys()):
            errors.append(_error(issue, f"missing_field:{field}"))

        repo = fields.get("repo", "")
        if not _REPO.fullmatch(repo):
            errors.append(_error(issue, "invalid_repo"))
        else:
            repo_key = repo.casefold()
            if repo_key in seen_repos:
                errors.append(_error(issue, "duplicate_repo"))
            else:
                seen_repos.add(repo_key)
            if issue.get("title") != f"coord: {repo}":
                errors.append(_error(issue, "title_repo_mismatch"))

        sha = fields.get("sha", "")
        if sha and not _SHA.fullmatch(sha):
            errors.append(_error(issue, "invalid_sha"))
        if _LOCAL_PATH.search(body):
            errors.append(_error(issue, "local_path_disclosure"))

        updated = _parse_timestamp(fields.get("updated", ""))
        if updated is None:
            errors.append(_error(issue, "invalid_updated"))

        agent = fields.get("agent", "")
        lease_text = fields.get("lease_until", "")
        if agent not in ALLOWED_AGENTS:
            errors.append(_error(issue, "invalid_agent"))
        elif agent == "none":
            if lease_text:
                errors.append(_error(issue, "released_agent_has_lease"))
        else:
            claimed_scope = fields.get("claimed_scope", "").casefold()
            if not claimed_scope or claimed_scope == "none":
                errors.append(_error(issue, "active_agent_missing_scope"))
            lease_until = _parse_timestamp(lease_text)
            if lease_until is None:
                errors.append(_error(issue, "active_agent_missing_or_invalid_lease"))
            else:
                if lease_until <= checked_at:
                    errors.append(_error(issue, "expired_active_lease"))
                if updated is not None and lease_until <= updated:
                    errors.append(_error(issue, "lease_not_after_update"))

    errors.sort(key=lambda item: (item["issue"] is None, item["issue"] or 0, item["code"]))
    return {
        "schema": SCHEMA,
        "passed": not errors,
        "issue_count": len(snapshot),
        "error_count": len(errors),
        "errors": errors,
    }


def _load_snapshot(path: Path | None, stdin: TextIO) -> Any:
    if path is None:
        return json.load(stdin)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        help="Read a gh issue list JSON snapshot from this file instead of stdin.",
    )
    parser.add_argument(
        "--now",
        help="Timezone-aware ISO-8601 audit time (mainly for deterministic tests).",
    )
    args = parser.parse_args(argv)
    now = _parse_timestamp(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        print(
            "BOB_COORD_AUDIT_INPUT_ERROR "
            + json.dumps({"schema": SCHEMA, "code": "invalid_now"}, sort_keys=True)
        )
        return 1
    try:
        snapshot = _load_snapshot(args.input, sys.stdin)
    except (OSError, UnicodeError, json.JSONDecodeError):
        print(
            "BOB_COORD_AUDIT_INPUT_ERROR "
            + json.dumps({"schema": SCHEMA, "code": "invalid_input"}, sort_keys=True)
        )
        return 1
    receipt = audit_snapshot(snapshot, now=now)
    marker = "BOB_COORD_AUDIT_OK" if receipt["passed"] else "BOB_COORD_AUDIT_FAIL"
    print(marker + " " + json.dumps(receipt, sort_keys=True))
    return 0 if receipt["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
