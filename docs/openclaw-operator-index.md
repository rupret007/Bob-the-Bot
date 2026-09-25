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
- Those boundaries are this index's policy. Which unmerged draft writes
  each fence is in [Fence scope by draft](#fence-scope-by-draft).
- Drafts #27 and #28 both invent an OpenClaw docs/README surface and a
  fallback CLI story. They **overlap**. They are **not a stack**. Do not
  merge them together from this PR.

## Pinned unmerged drafts (do not merge from this PR)

Recorded 2026-09-25. Re-read the pull request if a head moves. This draft
must not be used as a vehicle to squash them.

| Draft | Lane | Branch | Exact SHA | Status on this index |
| --- | --- | --- | --- | --- |
| [#26](https://github.com/rupret007/Bob-the-Bot/pull/26) | Andrea bridge | `cursor/openclaw-consolidation-fences-f6bd` | `b1eec45a2e1693656520412ebfce52157706f353` | Linked only |
| [#27](https://github.com/rupret007/Bob-the-Bot/pull/27) | docs + wrapper | `cursor/openclaw-operator-docs-7588` | `d200c1d7b648fae65dc090609f6c2c3d0cd2b13f` | Linked only |
| [#28](https://github.com/rupret007/Bob-the-Bot/pull/28) | CLI vendor | `cursor/vendor-openclaw-cli-6baa` | `fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066` | Linked only |

Those three drafts remain independent. Review or land them on their own
heads.

## File-level cross-links

Blob links are pinned to the exact SHAs above. They are read-only pointers.
This checkout does not contain those files.

### #26 Andrea bridge

[#26](https://github.com/rupret007/Bob-the-Bot/pull/26) only adds a
COORDINATION section. Its short lane is the Andrea bridge, not the
gateway or secrets fences. Read it first for the native-first / Andrea
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
- [tests/test_openclaw_cli_fallback.py](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/tests/test_openclaw_cli_fallback.py)

### #28 CLI vendor

[#28](https://github.com/rupret007/Bob-the-Bot/pull/28) vendors a cleaned
fallback CLI in-repo. That is a different leftover from the #27 wrapper.

- [docs/openclaw/operator-notes.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/docs/openclaw/operator-notes.md)
- [tools/openclaw/README.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/README.md)
- [tools/openclaw/cursor_openclaw.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/cursor_openclaw.py)
- [tools/openclaw/cursor_api_common.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/cursor_api_common.py)
- [tools/openclaw/env_loader.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/env_loader.py)
- [tools/openclaw/__init__.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/__init__.py) (package marker only)
- [tests/test_openclaw_cli.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tests/test_openclaw_cli.py)

## Overlap / do-not-stack

#27 and #28 both edit `README.md` and both create `docs/openclaw/`. #27
adds `tools/openclaw_cli_fallback.py`. #28 adds `tools/openclaw/`. Treat
them as **alternative leftover drafts**, not sequential steps. This index
does not pick a winner.

The two README edits are different sections on the same path:

- [#27 README.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/README.md) adds "OpenClaw operator surface" and points at `docs/openclaw/`.
- [#28 README.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/README.md) adds "OpenClaw fallback" and points at the vendored CLI.

## Fence scope by draft

Pinned heads only. This index does not rewrite those files.

- **#26** writes four bullets: native Cloud Agents first; Integration CLI
  only when native coverage is not sufficient; do not port `andrea_sync`;
  Andrea NanoBot keeps the bridge. #26's fence text stops at the Andrea bridge.
- **#27** writes the gateway and secrets fences in
  [hard-fences.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/hard-fences.md)
  and
  [not-moved.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/not-moved.md):
  `services/andrea_sync`, `~/.openclaw`, LaunchAgent/gateway, BlueBubbles
  send/bridge, and credentials. Its
  [operator-guide.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/operator-guide.md)
  calls the forwarder a vendored wrapper.
  [tools/openclaw_cli_fallback.py](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/tools/openclaw_cli_fallback.py)
  does not vendor that CLI. It shells out to `scripts/cursor_openclaw.py`
  inside the checkout named by `BOB_OPENCLAW_INTEGRATION_ROOT`.
  [docs/openclaw/README.md](https://github.com/rupret007/Bob-the-Bot/blob/d200c1d7b648fae65dc090609f6c2c3d0cd2b13f/docs/openclaw/README.md)
  calls that folder the source of truth for Bob-side OpenClaw policy. This
  index keeps `README.md` and `COORDINATION.md` as the entry points while
  #27 is unmerged, and leaves that source-of-truth claim on the #27 head.
- **#28** writes exclusions in
  [operator-notes.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/docs/openclaw/operator-notes.md)
  and
  [tools/openclaw/README.md](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/README.md):
  no `andrea_sync`, no gateway launch-agent copy, no secret migration, no
  auto-send. The entrypoint imports
  [cursor_api_common.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/cursor_api_common.py)
  and
  [env_loader.py](https://github.com/rupret007/Bob-the-Bot/blob/fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066/tools/openclaw/env_loader.py).
  When that unmerged CLI starts, `cursor_openclaw.py` loads the repo-root
  `.env` and the cwd `.env` through `env_loader.merge_dotenv_paths`
  (`override=False`). The repo-root path is `_SCRIPT_DIR.parent.parent / ".env"`
  (`_SCRIPT_DIR` is the script directory, `tools/openclaw` on this head). The
  cwd path is `Path.cwd() / ".env"`. A path that is not a file is skipped.
  Keys already in the environment stay put, so the repo-root file wins over
  the cwd file when both set the same key.
  Credential values, including any `CURSOR_API_KEY` value, stay out of this
  repository and out of coord comments.

## Stack Ops lane

This index is the Stack Ops specialist lane for OpenClaw operator docs.
Work on other specialist lanes stays on their own coordination issues:

- WebJam: [coord: rupret007/webjam](https://github.com/rupret007/Bob-the-Bot/issues/3)
- Show Night: [coord: rupret007/rad-dad-show-night](https://github.com/rupret007/Bob-the-Bot/issues/11)

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
4. Read [Fence scope by draft](#fence-scope-by-draft). Gateway and secrets fences are written on the #27 and #28 heads. #26 stops at the Andrea bridge. Stay on the Stack Ops lane.

## Out of scope here

- Merging or rebasing #26, #27, or #28
- Porting Andrea send/bridge code
- Copying gateway binaries, LaunchAgent plists, or host runtime
- Secret bootstrapping or runtime-store migration
- Auto-send behavior
- WebJam coding and Show Night (those lanes stay on their coord issues)
