# Agent coordination

GitHub is the source of truth. Bob Ops only presents this state.

Bob-the-Bot holds the protocol and one open coordination issue per repository. Codex, Claude, Gemini, MiniMax, and Grok read that issue before touching a repo and post a delta-only comment afterward. Do not mix this lane into product pull requests.

## Issue

One open issue in `rupret007/Bob-the-Bot` titled exactly:

`coord: rupret007/<repo>`

Label: `coord`.

## Lease body

Keep these keys, one per line:

```
- repo: rupret007/<repo>
- agent: none | codex | claude | gemini | minimax | grok
- sha:
- branch:
- pr:
- claimed_scope:
- completed_scope:
- holds:
- evidence:
- next_action:
- updated: 2026-08-28T22:40:00-05:00
- lease_until:
```

Rules:

- Claim a lease before work. Set `agent` and `lease_until` (default 4 hours).
- Exact SHA, branch, and PR when known. No guessed heads.
- `claimed_scope` is one leftover or one dedicated task. Not a product dump.
- `completed_scope` says what actually changed, or `none`; it is not a plan.
- `holds` lists parked PRs and Jeff-only gates. Do not touch them.
- `evidence` is hosted SHA, local command, or honest no-PR.
- `next_action` is the next safe step, not a wish list.
- Expire the lease on handoff (`agent: none`, clear `lease_until`) or when the clock passes `lease_until`.
- Comments are delta-only. Do not rewrite history in a comment.
- Private lanes stay high-level in any public presentment. No CSOne, customer rows, secrets, or local paths on the public board.
- Dashboard refresh reads these issues and paints an active public-lane lease (for Codex/Claude/Gemini/MiniMax/Grok). CI still beats a lease. A lease is dead text, not a private-issue link.

## Conductor standing order (multi-LLM)

- Keep all five conductor agents moving in parallel where safe: `codex`, `claude`, `gemini`, `minimax`, `grok`.
- Concurrency is repo-scoped. Every active lease must map to one repo and one bounded `claimed_scope`.
- `rupret007/webjam` is single-lane: never allow two live active leases at once.
- If WebJam is already leased by another active agent, pick a different repo or wait for release/expiry.
- The machine audit now emits `webjam_dual_active_lease` if two live WebJam leases appear in the same snapshot.

## Must read / must write

Before working a repo:

1. Read `coord: rupret007/<repo>`.
2. If another agent holds an unexpired lease, do not start a second goal on that checkout. For `rupret007/webjam`, this is absolute.
3. Claim or wait.

After a meaningful delta (draft PR, honest no-PR, merge, handoff):

1. Update the body fields.
2. Comment one delta.
3. Release the lease if you are done.

## Machine audit

Before claiming work or handing it to another agent, audit the current issue
snapshot with the dependency-free validator. The body is treated as untrusted
data and is never executed or echoed in a failure receipt:

```bash
gh issue list --repo rupret007/Bob-the-Bot --state open --label coord \
  --limit 100 --json number,title,body,state,labels \
  | python3 tools/coord_audit.py
```

`BOB_COORD_AUDIT_OK` means every issue has the required fields, a matching
title/repository, a supported agent, a valid exact SHA when present, no local
path disclosure, and a coherent lease. An active agent must have a non-empty
scope and a future timezone-aware lease; `agent: none` must have an empty
`lease_until`. The receipt reports only issue numbers and error codes, never
body values. Exit status `2` means contract violations; `1` means the input
snapshot or audit clock could not be parsed.

The pull-request workflow tests the deterministic parser and safety contract.
It intentionally does not query live issues, so a mutable board cannot turn an
unchanged code revision red after its review. Agents run the command above for
the current live-board receipt.

## Owner gates

Jeff still owns feel, send, spend, live Cisco, Che pull, Logic keys/WAVs, and merge when not leftover-green. Karen remains leftover + security ship-gate. Andrea send fence is unchanged.
