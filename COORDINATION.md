# Agent coordination

GitHub is the source of truth. Bob Ops only presents this state.

Bob-the-Bot holds the protocol and one open coordination issue per repository. Codex, Grok Bot, and Claude read that issue before touching a repo and post a delta-only comment afterward. Do not mix this lane into product pull requests.

## Issue

One open issue in `rupret007/Bob-the-Bot` titled exactly:

`coord: rupret007/<repo>`

Label: `coord`.

## Lease body

Keep these keys, one per line:

```
- repo: rupret007/<repo>
- agent: none | codex | grok | claude
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
- Dashboard refresh reads these issues and paints an active public-lane lease as `Codex lease` / `Grok lease` / `Claude lease`. CI still beats a lease. A lease is dead text, not a private-issue link.

## Must read / must write

Before working a repo:

1. Read `coord: rupret007/<repo>`.
2. If another agent holds an unexpired lease, do not start a second goal on that checkout.
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

## OpenClaw operator index

Operator map: [docs/openclaw-operator-index.md](docs/openclaw-operator-index.md).
That file links README and this protocol across three **unmerged** drafts
with exact SHAs and file-level blob links. It does not merge them, does
not lift owner gates, and does not treat #27/#28 as a stack.

- Native Cloud Agents first. `Cursor-OpenClaw-Integration` is **legacy**.
- Andrea, gateway, and secrets stay out of Bob-the-Bot.
- #26's fence text stops at the Andrea bridge. Gateway and secrets fences
  are written on the #27 and #28 heads. The index section "Fence scope by
  draft" is the map. This OpenClaw work is the Stack Ops lane.
- Stack Ops claims [coord: rupret007/Bob-the-Bot](https://github.com/rupret007/Bob-the-Bot/issues/22).
  Do not claim WebJam, Show Night, or Andrea for this map.
- The conductor standing order stays on unmerged [draft #25](https://github.com/rupret007/Bob-the-Bot/pull/25) `3939c3abf9a65225d9c40caa4737e23c1b85bd0c`. This PR does not stack it.
- Andrea bridge: [draft #26](https://github.com/rupret007/Bob-the-Bot/pull/26) `b1eec45a2e1693656520412ebfce52157706f353`
- docs + wrapper: [draft #27](https://github.com/rupret007/Bob-the-Bot/pull/27) `d200c1d7b648fae65dc090609f6c2c3d0cd2b13f`
- CLI vendor: [draft #28](https://github.com/rupret007/Bob-the-Bot/pull/28) `fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066`

