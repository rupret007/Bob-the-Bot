# Bob application handoff: private bootstrap

- Snapshot: 2026-08-26, America/Chicago
- Status: draft bootstrap; no merge or live runtime action authorized
- Audience: Grok Bot, Codex, and future Bob maintainers

## Completed

- Confirmed Bob-the-Bot is the private Bob application repository and Bob Ops is a
  separate public control plane.
- Reconciled six local historical Bob identity and natural Telegram UX change sets
  cleanly onto current Andrea main without publishing their raw local objects.
- Preserved the result as a pinned overlay instead of copying the Andrea engine.
- Added a versioned digest, derived patch ID, file-scope, public base-commit, and
  result-tree contract; local history is sanitized, non-authoritative provenance.
- Added fail-closed example defaults with no credentials, recipients, or endpoints.
- Added deterministic contract, privacy, identity, delegation, and send-fence acceptance.
- Added read-only CI with pinned actions and no deploy, message, provider, or restart step.
- Repaired a review-blocking natural-UX path that could restore denied completion
  text, and added a focused regression proving the original claim never reaches send.
- Restored explicit @openclaw addressing under the Bob default trigger and aligned
  four stale cross-surface identity assertions found by the complete offline suite.

## Verification record

- Engine base: f8655e2da59d1db8bd3777758ae8220ecb65d847
- Reconciled result tree: 58f3e0a88ddd0d60a613331f0bc266aea5d51d04
- Overlay SHA-256: e129cc36c3599000014b359bbf5a1ebce04ded373e2cce61fb5824f8a32ac85f
- Derived stable patch ID: f6f1d4cb4e238485f5cd96b672c5bb30d2c73b16
- Overlay scope: 21 existing source, test, and guidance files
- Historical provenance: six local unpublished change sets; remote reachability is
  not asserted, raw object IDs are omitted, and replay does not depend on them
- Acceptance repair: aligned stale Bob natural-UX assertions and kept send approval
  explicit in short Telegram copy
- Local Bob contract tests: 8/8 passed
- Patched Andrea targeted acceptance: 443/443 passed across the exact 12-file CI set
- Patched Andrea complete offline suite: 3,867/3,867 passed across 296 files
- Patched Andrea typecheck, full source formatting check, and build: passed
- Live messages, model calls, gateway restarts, settings changes, credentials, and deployments: zero

Re-run npm run check and the disposable-engine acceptance suite after any change to
the contract or overlay. Hosted status must come from the current GitHub check, not
this snapshot.

## Still open

| Item | Classification | Next safe action | Gate |
| --- | --- | --- | --- |
| Draft review | Hosted billing-blocked; prior head superseded | Review the repaired exact head and local proof; rerun hosted CI only after billing is fixed | Billing owner action, then exact-head merge approval |
| Andrea identity interface | Follow-up design | Consider upstreaming a tested configurable public identity | Separate Andrea draft and review |
| Live Bob runtime | Owner-only | Prepare a separate deployment and runtime runbook if wanted | Credentials, settings, restart, provider, send, and production approval |
| Bob Ops registration | Separate repository follow-up | Add a sanitized private Bob application lane in a source-only PR | Bob Ops exact-head merge approval and natural scheduled refresh |

## Risks and lessons

- A floating engine dependency would hide compatibility drift; the exact base and tree fail closed.
- Copying the engine would create two writable implementations; the overlay keeps one engine source of truth.
- Private visibility does not permit secrets or runtime state in source.
- Green offline tests do not prove a live provider, channel, deployment, or send.
- A presentation-layer rewrite after authorization can invalidate a safe fallback;
  denied payload selection must remain inside the fail-closed resolver.

## Privacy check

This handoff contains no credentials, contacts, recipients, message content,
provider endpoints, runtime state, private media, or machine paths.
It also contains no raw unpublished Andrea commit IDs or local author metadata.
