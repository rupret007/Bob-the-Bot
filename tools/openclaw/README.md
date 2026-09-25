# OpenClaw CLI Fallback (Vendored)

This folder vendors a cleaned copy of `scripts/cursor_openclaw.py` for Bob.

## Operator stance

- **Preferred path:** use native Cursor Cloud Agent tools first.
- **Fallback path:** use this CLI only when native tools are unavailable or blocked.
- **Dry-run support:** `create-agent` and `followup` support `--dry-run` and do not POST in dry-run mode.

## Explicit exclusions

This vendored fallback intentionally does **not** include:

- `andrea_sync` runtime integration
- gateway launch-agent binaries/plists/state workflows
- secret bootstrapping/copying from local runtime stores
- any auto-send side channel behavior

## File map

- `cursor_openclaw.py`: fallback CLI entrypoint
- `cursor_api_common.py`: minimal request and validation helpers
- `env_loader.py`: `.env` parsing and merge helper
