# Logic Companion Research — Sep 22, 2026

Docs-only research snapshot. No WebJam product code. No Logic integration implementation.

## Contents

| File | Purpose |
|------|---------|
| `webjam-logic-pro-companion-20260922.md` | Primary research — APIs, protocols, architecture |
| `webjam-logic-EXCELLENCE-RESEARCH.md` | Excellence north-star, edge cases, friction map, P0–P3 |
| `webjam-logic-EXCELLENCE-SYNTHESIS.md` | Executive cut, Adopt/Defer/Kill, locked P0/P1/P2 |
| `webjam-logic-TESTING-PLAN.md` | Per-enhancement acceptance tests |
| `webjam-logic-companion-BUILD-BRIEF.md` | Goals, non-goals, phasing, PR strategy |
| `codex-fast-mode-lightning-FINDINGS.md` | Fast mode toggle research (separate topic) |
| `sources/` | Raw input from ChatGPT, Claude Opus, Gemini, MiniMax |
| `critiques/` | Gemini and MiniMax critiques |

## BUILD GATE

**No Logic product code until:**
1. Jeff reviews this research
2. Jeff selects P0/P1 items in / out / defer
3. Each selected item has passing test evidence Jeff accepts
4. Jeff says "quality product OK" for that slice

## Explicit non-goals
- Do not touch `rupret007/webjam` (lease held for #149)
- Do not MATCH #145–#148 without feel yes
- Phone-as-transport remains PARKED
- No Logic Remote reverse engineering
