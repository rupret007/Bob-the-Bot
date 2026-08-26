# Security and privacy

Bob-the-Bot is private, but private visibility is not a substitute for safe source
control.

## Repository boundary

Allowed:

- public repository identifiers and exact source commits
- non-secret feature flags with fail-closed values
- source overlays, deterministic tests, and sanitized documentation

Never commit:

- API keys, tokens, passwords, cookies, certificates, or private keys
- phone numbers, contacts, recipients, message contents, or account identifiers
- provider endpoints, webhook URLs, device identifiers, or private network details
- runtime databases, transcripts, logs, backups, media, or generated builds
- active OpenClaw, Telegram, Messages, or Andrea configuration
- machine-specific paths

scripts/privacy-check.mjs enforces a conservative subset of this policy. A passing
scan is necessary but not sufficient; review the full diff.

## Authority boundary

The example configuration disables outbound Messages, the BlueBubbles control API,
and the Andrea OpenAI backend. CI supplies no credentials, loads Andrea's network
guard, and runs no communication smoke. Engine tests may enable mocked adapters
inside their own isolated fixtures; they cannot reach a live service.

No repository action implicitly authorizes:

- a message or external action
- a live model or provider call
- a gateway or service restart
- a credential, account, permission, or settings change
- a production deployment or publication
- spending or use of private media

Those actions require a separate, explicit owner decision for the exact target.

## Dependency and overlay review

Engine updates are reviewed as source changes, not floating dependencies. The
contract pins the exact base and exact patched tree. Action dependencies in CI are
pinned to full commit identifiers and workflow permissions are read-only.

Report a suspected leak or unsafe behavior in a private repository issue. Do not
paste sensitive material into a public issue, dashboard, pull request, or handoff.
