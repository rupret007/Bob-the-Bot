# Conductor standing order

This standing order keeps the multi-LLM conductor lane honest while letting
work progress in parallel.

## Model lanes in scope

- `codex`
- `claude`
- `gemini`
- `minimax`
- `grok`

## Non-negotiable guardrails

1. GitHub coordination issues are the source of truth.
2. One open coordination issue per repo: `coord: rupret007/<repo>`.
3. One **live active lease** per repo at a time.
4. `rupret007/webjam` is explicitly single-lane: no dual active leases.
5. Every active lease must declare a bounded `claimed_scope`.
6. Comments remain delta-only; never rewrite history in comments.

## Safe concurrency loop

1. Run the audit snapshot command from `COORDINATION.md`.
2. Read the target `coord:` issue before starting.
3. If WebJam is actively leased by someone else, do one of:
   - pick another repo slice, or
   - wait for release/expiry.
4. Claim lease with exact SHA/branch/PR once known.
5. After a meaningful delta, update fields and post one delta comment.
6. Release lease (`agent: none`, clear `lease_until`) when done.

## Machine checks

`tools/coord_audit.py` enforces the contract for all supported agents and emits:

- `dual_active_lease` when two live active leases claim the same repo
- `webjam_dual_active_lease` for the WebJam-specific violation

These checks fail closed without echoing lease-body values.
