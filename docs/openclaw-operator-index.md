# OpenClaw operator index

This is a map, not a merge.

`README.md` and `COORDINATION.md` stay the operator entry points. The OpenClaw
work already exists as three **separate unmerged drafts**. This file only
points at their exact heads and operator files. It does not fold their trees
together, vendor their CLI, or replace their fence text.

## Honesty

- Native Cloud Agent tools are the first implementation path.
- `rupret007/Cursor-OpenClaw-Integration` is a **legacy** fallback surface.
  It is not the destination and is not imported here.
- Andrea (`andrea_sync`, BlueBubbles send/bridge) stays out of Bob-the-Bot.
- OpenClaw gateway / LaunchAgent runtime stays out of Bob-the-Bot.
- Secrets, tokens, auth stores, and `~/.openclaw` state stay out of this
  repository. This index contains no credentials.
- Drafts #27 and #28 both invent an OpenClaw docs/README surface and a
  fallback CLI story. They **overlap**. They are **not a stack**. Do not
  merge them together from this PR.

## Pinned unmerged drafts (do not merge from this PR)

Recorded 2026-09-25. Re-read the pull request if a head moves. This draft
must not be used as a vehicle to squash them.

| Draft | Lane | Branch | Exact SHA | Status on this index |
| --- | --- | --- | --- | --- |
| [#26](https://github.com/rupret007/Bob-the-Bot/pull/26) | fences | `cursor/openclaw-consolidation-fences-f6bd` | `b1eec45a2e1693656520412ebfce52157706f353` | Linked only |
| [#27](https://github.com/rupret007/Bob-the-Bot/pull/27) | docs + wrapper | `cursor/openclaw-operator-docs-7588` | `d200c1d7b648fae65dc090609f6c2c3d0cd2b13f` | Linked only |
| [#28](https://github.com/rupret007/Bob-the-Bot/pull/28) | CLI vendor | `cursor/vendor-openclaw-cli-6baa` | `fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066` | Linked only |

Those three drafts remain independent. Review or land them on their own
heads.

## File-level cross-links

Blob links are pinned to the exact SHAs above. They are read-only pointers.
This checkout does not contain those files.

### #26 fences

[#26](https://github.com/rupret007/Bob-the-Bot/pull/26) only adds a
COORDINATION section. Read it first for the native-first / Andrea
keep-bridge fence:

- [COORDINATION.md](https://github.com/rupret007/Bob-the-Bot/blob/b1eec45a2e1693656520412ebfce52157706f353/COORDINATION.md) (`OpenClaw consolidation fences`)

### #27 docs + wrapper

[#27](https://github.com/rupret007/Bob-the-Bot/pull/27) adds a Bob-local
`docs/openclaw/` operator surface and a thin forwarder. The wrapper is not
a vendored CLI; it expects an operator-provided Integration checkout.

- [docs/openclaw/README.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/README.md)
- [docs/openclaw/operator-guide.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/operator-guide.md)
- [docs/openclaw/hard-fences.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/hard-fences.md)
- [docs/openclaw/not-moved.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/not-moved.md)
- [tools/openclaw_cli_fallback.py](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/tools/openclaw_cli_fallback.py)

### #28 CLI vendor

[#28](https://github.com/rupret007/Bob-the-Bot/pull/28) vendors a cleaned
fallback CLI in-repo. That is a different leftover from the #27 wrapper.

- [docs/openclaw/operator-notes.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/docs/openclaw/operator-notes.md)
- [tools/openclaw/README.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/README.md)
- [tools/openclaw/cursor_openclaw.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/cursor_openclaw.py)

## Overlap / do-not-stack

#27 and #28 both edit `README.md` and both create `docs/openclaw/`. #27
adds `tools/openclaw_cli_fallback.py`. #28 adds `tools/openclaw/`. Treat
them as **alternative leftover drafts**, not sequential steps. This index
does not pick a winner.

## Backlinks

#26, #27, and #28 do not point at this index. This file is the only hosted
cross-link surface for those three drafts.

## Operator path

1. Read [COORDINATION.md](../COORDINATION.md) and claim the live `coord:`
   lease before work.
2. Prefer native Cloud Agent tools.
3. If a fallback is still required, review the **legacy** Integration CLI
   stories on the exact #27 and #28 heads above. They overlap; do not treat
   either CLI as new product and do not stack them.
4. Stop at the fences in #26: Andrea, gateway, and secrets stay out.

## Out of scope here

- Merging or rebasing #26, #27, or #28
- Porting Andrea send/bridge code
- Copying gateway binaries, LaunchAgent plists, or host runtime
- Secret bootstrapping or runtime-store migration
- Auto-send behavior
