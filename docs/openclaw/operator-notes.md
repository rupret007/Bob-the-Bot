# OpenClaw Operator Notes

## Purpose

Bob vendors a reusable OpenClaw CLI fallback under `tools/openclaw/` so operators
have one consolidated, reviewable emergency path when native Cloud Agent tooling
is unavailable.

## Primary vs fallback

1. Prefer native Cloud Agent tooling for normal operation.
2. Use `tools/openclaw/cursor_openclaw.py` only as fallback.

## Safe usage

- Set `CURSOR_API_KEY` and run with `--json` for machine-readable output.
- Use `create-agent --dry-run` and `followup --dry-run` before any live POST.
- Keep `stop-all-jobs` in dry mode unless you intentionally pass `--yes`.

## Boundaries (intentionally out of scope)

- No `andrea_sync` automation paths.
- No gateway launch-agent workflows.
- No secret migration or runtime store copying.
- No auto-send behavior.
