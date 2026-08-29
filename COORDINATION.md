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

## Owner gates

Jeff still owns feel, send, spend, live Cisco, Che pull, Logic keys/WAVs, and merge when not leftover-green. Karen remains leftover + security ship-gate. Andrea send fence is unchanged.
