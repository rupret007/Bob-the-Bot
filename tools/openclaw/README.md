# OpenClaw CLI Fallback (Vendored)

This folder vendors a cleaned copy of `scripts/cursor_openclaw.py` for Bob.

## Operator stance

- **Preferred path:** use native Cursor Cloud Agent tools first.
- **Fallback path:** use this CLI only when native tools are unavailable or blocked.
- **Dry-run support:** `create-agent` and `followup` support `--dry-run` and do not POST in dry-run mode.
- **Confirmation:** live `create-agent`, `followup`, `stop-agent`, `stop-all-jobs`, and `delete-agent` operations require `--yes`. `stop-all-jobs` previews matches without `--yes`; explicit `--dry-run` always prevents changes.
- **Configuration:** only `CURSOR_API_KEY` and `CURSOR_AUTH_MODE` are loaded from the repository-root `.env`; every other file key is ignored, and existing environment variables take precedence. Symlinked `.env` files are rejected. A `.env` in the current working directory is ignored unless it is the repository root.
- **Transport:** proxies and TLS overrides from the environment are ignored, including `HTTPS_PROXY`, `SSL_CERT_FILE`, `SSL_CERT_DIR`, and `SSLKEYLOGFILE`. HTTPS uses the system's compiled-in CA paths with certificate and hostname verification. Diagnostics report only key presence and length, including with `--show-key`.
- **API destination:** `CURSOR_BASE_URL` and `--base-url` accept only `https://api.cursor.com` (an optional trailing slash is allowed). HTTP, other origins, URL credentials, ports, paths, queries, and fragments are rejected. Redirects are refused before credentials can be forwarded.

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
