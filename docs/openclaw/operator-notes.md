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
- Configuration comes from the process environment and the repository-root `.env` only; existing environment variables take precedence. Running from another directory does not load that directory's `.env`.
- The API origin is pinned to `https://api.cursor.com`. `CURSOR_BASE_URL` and `--base-url` may specify that URL, optionally with one trailing slash; other values and redirects are rejected.
- Use `create-agent --dry-run` and `followup --dry-run` to preview requests. Dry runs do not require `--yes`, and `--dry-run` takes precedence when both flags are present.
- Pass `--yes` explicitly for live `create-agent`, `followup`, `stop-agent`, and `delete-agent` commands. Without it, the command fails before sending a request.
- `stop-all-jobs` previews matches with read-only requests unless `--yes` is supplied. Explicit `--dry-run` always prevents stops, even with `--yes`.

## Boundaries (intentionally out of scope)

- No `andrea_sync` automation paths.
- No gateway launch-agent workflows.
- No secret migration or runtime store copying.
- No auto-send behavior.
