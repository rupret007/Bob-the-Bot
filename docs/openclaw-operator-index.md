# OpenClaw operator index

This is a map, not a merge.

`README.md` and `COORDINATION.md` stay the operator entry points. The OpenClaw
work already exists as three **separate unmerged drafts**. This file only
points at them. It does not fold their trees together, vendor their CLI, or
replace their fence text.

## Honesty

- Native Cloud Agent tools are the first implementation path.
- `rupret007/Cursor-OpenClaw-Integration` is a **legacy** fallback surface.
  It is not the destination and is not imported here.
- Andrea (`andrea_sync`, BlueBubbles send/bridge) stays out of Bob-the-Bot.
- OpenClaw gateway / LaunchAgent runtime stays out of Bob-the-Bot.
- Secrets, tokens, auth stores, and `~/.openclaw` state stay out of this
  repository. This index contains no credentials.

## Unmerged drafts (do not merge from this PR)

| Draft | Lane | What it covers | Status on this index |
| --- | --- | --- | --- |
| [#26](https://github.com/rupret007/Bob-the-Bot/pull/26) | fences | Native-first, Integration-CLI fallback only, Andrea keep-bridge | Linked only |
| [#27](https://github.com/rupret007/Bob-the-Bot/pull/27) | docs | Operator surface under `docs/openclaw/` plus thin wrapper notes | Linked only |
| [#28](https://github.com/rupret007/Bob-the-Bot/pull/28) | CLI vendor | Cleaned fallback CLI under `tools/openclaw/` | Linked only |

Those three drafts remain independent. Review or land them on their own
heads. This draft must not be used as a vehicle to squash them.

## Operator path

1. Read [COORDINATION.md](../COORDINATION.md) and claim the live `coord:`
   lease before work.
2. Prefer native Cloud Agent tools.
3. If a fallback is still required, use the **legacy** Integration CLI
   story documented in #27/#28. Do not treat that CLI as new product.
4. Stop at the fences in #26: Andrea, gateway, and secrets stay out.

## Out of scope here

- Merging or rebasing #26, #27, or #28
- Porting Andrea send/bridge code
- Copying gateway binaries, LaunchAgent plists, or host runtime
- Secret bootstrapping or runtime-store migration
- Auto-send behavior
