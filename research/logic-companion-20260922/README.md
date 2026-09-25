# Logic companion research — conductor card (2026-09-22)

Research snapshot. No WebJam product code. No Logic implementation. Jeff has not accepted a slice.

P0 / P1 / P2 names in these files are a **research cut**. They are not a Jeff sign-off.

## Decision

Do not build a Logic Remote clone or a remote Arrange editor.

1. **Phase 1 — files.** A handoff folder (audio, MIDI, tempo notes) that drops into Logic with no network and no MCU.
2. **Phase 2 — local mute.** WebJam’s own Rehearse | Record profile. MCU feedback is the truth for “Logic is recording.” Mute local program before the downbeat. Stop alone does not unmute.
3. **Phase 3 — BlackHole.** Optional print-in. Not a P0. Easy to get echo wrong.

Phone transport stays parked. Guests do not run Logic. Jamulus “split mute” is not done until a second person confirms by ear.

## Read order

| Order | File | Use it for |
|---|---|---|
| 1 | `webjam-logic-EXCELLENCE-SYNTHESIS.md` | What to adopt, defer, or kill |
| 2 | `webjam-logic-TESTING-PLAN.md` | What must be shown before any slice is “done” |
| 3 | `webjam-logic-companion-BUILD-BRIEF.md` | Phasing and non-goals. Lease lines are that night, not the live board |
| 4 | `webjam-logic-EXCELLENCE-RESEARCH.md` | Edge cases when designing one slice |
| 5 | `webjam-logic-pro-companion-20260922.md` | Which Logic surfaces exist in public docs |
| — | `codex-fast-mode-lightning-FINDINGS.md` | Separate topic: ChatGPT Fast mode. Not a Logic design |

## BUILD GATE

No Logic product code until all of these are true:

1. Jeff reviews this research.
2. Jeff marks each item in, out, or deferred.
3. Each chosen item has evidence Jeff accepts (`webjam-logic-TESTING-PLAN.md`).
4. Jeff says the slice is a quality product.
5. The live `coord:` lease allows it. Do not piggyback on WebJam polish PRs.

Feel tests in the testing plan come before mute state-machine code.

## Source honesty

Raw files are partial. Do not quote them as a finished model answer.

| File | What you actually have |
|---|---|
| `sources/gemini-ideas.md` | Stops mid-sentence in Idea 4. The opener says 12 ideas. Those 12 are not in the file. |
| `sources/minimax-excellence.md` | Trimmed chain-of-thought. Starts mid-word. Numbering skips. |
| `sources/claude-opus-plan-stamp.md` | Twelve bullets. A stamp, not a full plan. |
| `sources/chatgpt-fast-mode-ax-excerpt.txt` | Shortcut AX lines only. Includes duplicate windows. |
| `critiques/gemini-logic-critique.md` | Eight bullets. |
| `critiques/minimax-logic-critique.md` | Six bullets. |
| Fast-mode findings | Cite local dumps that are **not** in this repo, except the excerpt above. The lightning-bolt glyph was not confirmed. |

Aug 2022 logic-integration research is cited as prior art. It is not in this repository.

## Board notes are frozen

`#145`–`#149`, “grok on #149,” and “#149 green” are 2026-09-22 notes inside the research. The open `coord:` issue is the lease. Do not steer from these files.

## What not to report

- Do not say Logic companion code exists.
- Do not say mute, handoff, or BlackHole was tested.
- Do not say Fast mode is the lightning bolt.
- Do not say CI is green. This change set does not prove Actions. Private Actions may be billing-blocked.
