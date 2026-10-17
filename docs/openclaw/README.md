# OpenClaw operator surface for Bob-the-Bot

This folder consolidates only the OpenClaw operator surface that Bob needs to
coordinate Cloud Agent execution and fallback handling.

It intentionally excludes runtime services and host state that belong to other
lanes.

## Gap inventory (Bob before this consolidation)

Previously in Bob:

- `README.md` and `COORDINATION.md` with lease protocol and high-level fences.
- No dedicated OpenClaw runbook under `docs/`.
- No Bob-local wrapper for OpenClaw CLI fallback semantics.

Added here:

- `operator-guide.md`: when to use native Cloud Agent tools vs CLI fallback.
- `hard-fences.md`: strict import boundaries and do-not-port rules.
- `not-moved.md`: explicit leftovers that remain outside Bob by design.
- `tools/openclaw_cli_fallback.py`: thin optional wrapper around
  `Cursor-OpenClaw-Integration/scripts/cursor_openclaw.py`.

## Consolidation intent

OpenClaw investment is reused in Bob where it helps operators:

- Reuse decision logic and operational patterns from `cursor_handoff` docs.
- Reuse the `cursor_openclaw.py` surface through a thin wrapper when native
  Cloud Agent tools are unavailable.
- Keep one operator story across Bob and Grok Bot:
  - Grok Bot: native Cloud Agent tool path first.
  - Bob-the-Bot: same native-first policy, with CLI fallback documented here.

## Scope boundaries

Bob keeps **operator policy and wrappers**, not local runtime systems:

- Andrea keeps the BlueBubbles bridge and send engine.
- Local OpenClaw gateway runtime remains local-only host state.
- `andrea_sync` stays out of Bob.

Use this folder as the source of truth for Bob-side OpenClaw coordination
policy.
