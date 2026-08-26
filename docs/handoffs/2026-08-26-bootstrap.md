# Bob application handoff: private bootstrap

- Snapshot: 2026-08-26, America/Chicago
- Status: draft bootstrap; no merge or live runtime action authorized
- Audience: Grok Bot, Codex, and future Bob maintainers

## Completed

- Confirmed Bob-the-Bot is the private Bob application repository and Bob Ops is a
  separate public control plane.
- Replayed the six existing Bob identity and natural Telegram UX commits cleanly
  onto current Andrea main.
- Preserved the result as a pinned overlay instead of copying the Andrea engine.
- Added a versioned digest, file-scope, source-commit, base-commit, and result-tree contract.
- Added fail-closed example defaults with no credentials, recipients, or endpoints.
- Added deterministic contract, privacy, identity, delegation, and send-fence acceptance.
- Added read-only CI with pinned actions and no deploy, message, provider, or restart step.

## Verification record

- Engine base: f8655e2da59d1db8bd3777758ae8220ecb65d847
- Reconciled result tree: 6c193efa849e16392c4ba179c261cdcb6bc7aa17
- Overlay scope: 15 existing source, test, and guidance files
- Reconciliation: all six commits applied cleanly; no unrelated branch commit was needed
- Acceptance repair: aligned stale Bob natural-UX assertions and kept send approval
  explicit in short Telegram copy
- Local Bob contract tests: 6 of 6 passed
- Patched Andrea acceptance: 296 of 296 targeted tests passed
- Patched Andrea typecheck, full source formatting check, and build: passed
- Live messages, model calls, gateway restarts, settings changes, credentials, and deployments: zero

Re-run npm run check and the disposable-engine acceptance suite at the exact draft
head. Hosted status must come from the current GitHub check, not this snapshot.

## Still open

| Item | Classification | Next safe action | Gate |
| --- | --- | --- | --- |
| Draft review | Hosted pending until GitHub reports the exact head | Review the complete draft diff and CI | Exact-head merge approval |
| Andrea identity interface | Follow-up design | Consider upstreaming a tested configurable public identity | Separate Andrea draft and review |
| Live Bob runtime | Owner-only | Prepare a separate deployment and runtime runbook if wanted | Credentials, settings, restart, provider, send, and production approval |
| Bob Ops registration | Separate repository follow-up | Add a sanitized private Bob application lane in a source-only PR | Bob Ops exact-head merge approval and natural scheduled refresh |

## Risks and lessons

- A floating engine dependency would hide compatibility drift; the exact base and tree fail closed.
- Copying the engine would create two writable implementations; the overlay keeps one engine source of truth.
- Private visibility does not permit secrets or runtime state in source.
- Green offline tests do not prove a live provider, channel, deployment, or send.

## Privacy check

This handoff contains no credentials, contacts, recipients, message content,
provider endpoints, runtime state, private media, or machine paths.
