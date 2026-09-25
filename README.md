# Bob-the-Bot

Private application lane. Coordination protocol: [COORDINATION.md](COORDINATION.md).
One `coord: rupret007/<repo>` issue per repository is the live lease. GitHub is authoritative. Bob Ops only presents that state.

## OpenClaw operator index

Native Cloud Agent tools are first. `Cursor-OpenClaw-Integration` is a
**legacy** fallback, not the destination. Andrea, gateway, and secrets stay
out of Bob.

The current OpenClaw work lives in three **separate unmerged drafts**. This
repo indexes their exact heads and operator files; it does not merge them.
#27 and #28 overlap (`docs/openclaw/` plus two leftover CLI stories) and
are **not a stack**. #26's fence text stops at the Andrea bridge. Gateway
and secrets fences are written on the #27 and #28 heads. This OpenClaw map
is the Stack Ops lane. WebJam and Show Night stay on their own coord issues.

- [OpenClaw operator index](docs/openclaw-operator-index.md) (exact SHAs + file links)
- fences: [draft #26](https://github.com/rupret007/Bob-the-Bot/pull/26) `b1eec45a2e1693656520412ebfce52157706f353`
- docs + wrapper: [draft #27](https://github.com/rupret007/Bob-the-Bot/pull/27) `d200c1d7b648fae65dc090609f6c2c3d0cd2b13f`
- CLI vendor: [draft #28](https://github.com/rupret007/Bob-the-Bot/pull/28) `fa4f41a1a8eb5e1d57eb7ffb24b24528b4a7c066`

