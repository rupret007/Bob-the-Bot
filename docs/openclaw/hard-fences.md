# OpenClaw hard fences for Bob consolidation

These fences are mandatory for OpenClaw-related consolidation into Bob-the-Bot.

## Allowed to consolidate into Bob

- Operator-facing documentation and decision rules.
- Thin wrappers that invoke reusable, external operator tooling.
- Coordination-safe guidance for Cloud Agent native-first and fallback behavior.

## Not allowed to consolidate into Bob

- `services/andrea_sync` code or runtime.
- Any `~/.openclaw` files, auth DBs, or local runtime state.
- LaunchAgent plists, gateway binaries, or local process state/config.
- BlueBubbles send engine or send-path implementation details.
- Credentials, tokens, or provider keys.

## Runtime boundary

- OpenClaw gateway remains a local operator runtime concern.
- Bob documents the boundary and fallback policy but does not host that runtime.
- Andrea keeps the bridge responsibilities for BlueBubbles and related send
  lanes.

## Security and maintenance boundary

- Bob must not become a second secret/runtime app.
- Reuse should happen through docs and thin wrappers, not by copying live local
  state or private operator infra into version control.
