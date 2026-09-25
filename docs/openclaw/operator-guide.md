# OpenClaw operator guide (Bob-the-Bot)

## Purpose

Define one operator decision model for Bob when coordinating Cursor Cloud Agent
work, while reusing OpenClaw integration patterns without importing restricted
runtime systems.

## Execution preference order

1. **Native Cloud Agent tools first** (preferred and primary).
2. **OpenClaw CLI fallback** only when native tools are unavailable or blocked.

Grok Bot already has native Cloud Agent tooling, so fallback should be rare
there. Bob keeps fallback docs and a thin wrapper for continuity.

## Native vs CLI fallback decision table

| Situation | Path |
|---|---|
| Native Cloud Agent create/list/followup works | Use native tools |
| Native path degraded or unavailable | Use `tools/openclaw_cli_fallback.py` |
| Need deep parity with Integration CLI options | Use fallback wrapper and pass through supported args |

## Optional fallback wrapper

Bob vendors a thin wrapper:

- `tools/openclaw_cli_fallback.py`

The wrapper does not reimplement `cursor_openclaw.py`; it forwards to an
operator-provided local clone of `Cursor-OpenClaw-Integration`.

Required env var:

```bash
export BOB_OPENCLAW_INTEGRATION_ROOT=/absolute/path/to/Cursor-OpenClaw-Integration
```

Example:

```bash
python3 tools/openclaw_cli_fallback.py diagnose --json
python3 tools/openclaw_cli_fallback.py list-agents --limit 20 --json
```

## Reused operator concepts from OpenClaw Integration

Adapted from the `cursor_handoff` and `cursor_openclaw.py` operator surface:

- Cloud Agent API is preferred over local CLI by default.
- Read-only/analysis intent should stay explicit where possible.
- Fallback mode is a product limitation path, not the default.
- Keep user-safe summaries separate from internal runtime troubleshooting detail.

## Coordination alignment

This guide augments `COORDINATION.md`; it does not replace lease protocol.

- Lease ownership, delta comments, and holds remain governed by
  `COORDINATION.md`.
- OpenClaw fallback usage must still follow the same coordination contract.
