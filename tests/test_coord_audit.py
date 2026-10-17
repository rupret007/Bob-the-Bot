from __future__ import annotations

import json
import unittest
from datetime import datetime

from tools import coord_audit

NOW = datetime.fromisoformat("2026-09-03T17:30:00-05:00")


def _issue(
    *,
    number: int = 3,
    repo: str = "rupret007/example",
    agent: str = "none",
    lease_until: str = "",
    claimed_scope: str = "none",
    extra_lines: tuple[str, ...] = (),
) -> dict[str, object]:
    body_lines = [
        f"- repo: {repo}",
        f"- agent: {agent}",
        "- sha: 0123456789abcdef0123456789abcdef01234567",
        "- branch:",
        "- pr:",
        f"- claimed_scope: {claimed_scope}",
        "- completed_scope: none",
        "- holds: no merge",
        "- evidence: exact current SHA",
        "- next_action: inspect safely",
        "- updated: 2026-09-03T17:20:00-05:00",
        f"- lease_until: {lease_until}",
        *extra_lines,
    ]
    return {
        "number": number,
        "title": f"coord: {repo}",
        "body": "\n".join(body_lines),
        "state": "OPEN",
        "labels": [{"name": "coord"}],
    }


def _codes(receipt: dict[str, object]) -> set[str]:
    return {str(item["code"]) for item in receipt["errors"]}  # type: ignore[index]


class CoordinationAuditTests(unittest.TestCase):
    def test_released_issue_passes_without_a_lease(self) -> None:
        receipt = coord_audit.audit_snapshot([_issue()], now=NOW)
        self.assertEqual(
            receipt,
            {
                "schema": "bob.coordination-audit/v1",
                "passed": True,
                "issue_count": 1,
                "error_count": 0,
                "errors": [],
            },
        )

    def test_active_issue_requires_a_future_lease_and_scope(self) -> None:
        active = _issue(
            agent="codex",
            lease_until="2026-09-03T21:20:00-05:00",
            claimed_scope="one bounded improvement",
        )
        receipt = coord_audit.audit_snapshot([active], now=NOW)
        self.assertTrue(receipt["passed"])

        active["body"] = str(active["body"]).replace(
            "2026-09-03T21:20:00-05:00", "2026-09-03T17:00:00-05:00"
        )
        self.assertIn(
            "expired_active_lease",
            _codes(coord_audit.audit_snapshot([active], now=NOW)),
        )

    def test_all_conductor_agents_are_supported(self) -> None:
        for agent in sorted(coord_audit.CONDUCTOR_AGENTS):
            with self.subTest(agent=agent):
                receipt = coord_audit.audit_snapshot(
                    [
                        _issue(
                            agent=agent,
                            lease_until="2026-09-03T21:20:00-05:00",
                            claimed_scope="one bounded improvement",
                        )
                    ],
                    now=NOW,
                )
                self.assertTrue(receipt["passed"], receipt)

    def test_released_issue_cannot_retain_a_lease(self) -> None:
        receipt = coord_audit.audit_snapshot(
            [_issue(lease_until="2026-09-03T21:20:00-05:00")], now=NOW
        )
        self.assertEqual(_codes(receipt), {"released_agent_has_lease"})

    def test_unknown_duplicate_and_missing_fields_fail_closed(self) -> None:
        issue = _issue(extra_lines=("- mystery: value", "- agent: claude"))
        issue["body"] = str(issue["body"]).replace(
            "- evidence: exact current SHA\n", ""
        )
        codes = _codes(coord_audit.audit_snapshot([issue], now=NOW))
        self.assertEqual(
            codes,
            {"duplicate_field", "missing_field:evidence", "unknown_field"},
        )

    def test_title_label_state_and_repo_identity_are_checked(self) -> None:
        issue = _issue()
        issue.update(
            {"title": "coord: rupret007/other", "labels": [], "state": "CLOSED"}
        )
        self.assertEqual(
            _codes(coord_audit.audit_snapshot([issue], now=NOW)),
            {"coord_label_missing", "issue_not_open", "title_repo_mismatch"},
        )

    def test_duplicate_repo_and_issue_number_are_rejected(self) -> None:
        receipt = coord_audit.audit_snapshot([_issue(), _issue()], now=NOW)
        self.assertEqual(
            _codes(receipt), {"duplicate_issue_number", "duplicate_repo"}
        )

    def test_webjam_cannot_have_two_live_active_leases(self) -> None:
        first = _issue(
            number=3,
            repo="rupret007/webjam",
            agent="codex",
            lease_until="2026-09-03T21:20:00-05:00",
            claimed_scope="stability pass",
        )
        second = _issue(
            number=4,
            repo="rupret007/webjam",
            agent="gemini",
            lease_until="2026-09-03T22:20:00-05:00",
            claimed_scope="edge-case pass",
        )
        codes = _codes(coord_audit.audit_snapshot([first, second], now=NOW))
        self.assertIn("dual_active_lease", codes)
        self.assertIn("webjam_dual_active_lease", codes)

    def test_body_values_are_never_echoed_in_failure_receipt(self) -> None:
        private_path = "/Users/private-name/secret/project"
        issue = _issue(extra_lines=(f"- hosted_status: {private_path}",))
        receipt = coord_audit.audit_snapshot([issue], now=NOW)
        encoded = json.dumps(receipt)
        self.assertEqual(_codes(receipt), {"local_path_disclosure"})
        self.assertNotIn(private_path, encoded)
        self.assertNotIn("private-name", encoded)

    def test_invalid_snapshot_shape_is_safe_and_deterministic(self) -> None:
        receipt = coord_audit.audit_snapshot({"body": "not an array"}, now=NOW)
        self.assertFalse(receipt["passed"])
        self.assertEqual(
            receipt["errors"], [{"issue": None, "code": "snapshot_not_array"}]
        )

    def test_naive_audit_clock_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "now must be timezone-aware"):
            coord_audit.audit_snapshot([_issue()], now=datetime(2026, 9, 3))


if __name__ == "__main__":
    unittest.main()
