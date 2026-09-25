# Bob-the-Bot

Private application lane. Coordination protocol: [COORDINATION.md](COORDINATION.md).
One `coord: rupret007/<repo>` issue per repository is the live lease. GitHub is authoritative. Bob Ops only presents that state.

## OpenClaw operator surface

Bob keeps OpenClaw operator policy and optional CLI fallback docs under
[`docs/openclaw/`](docs/openclaw/), with native Cloud Agent tools as the
default path. Local runtime/gateway state, `andrea_sync`, and BlueBubbles send
engine internals remain outside Bob.
