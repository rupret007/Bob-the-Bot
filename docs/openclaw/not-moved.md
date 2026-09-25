# Explicit leftovers not moved into Bob

The following remain outside Bob-the-Bot by design:

- `services/andrea_sync/**`
- OpenClaw local runtime state under `~/.openclaw/**`
- OpenClaw LaunchAgent gateway internals (plists, binary state, host wiring)
- BlueBubbles send engine paths and bridge implementation details
- Any credentials, tokens, secrets, or auth stores

These are intentional exclusions, not missing migration work.
