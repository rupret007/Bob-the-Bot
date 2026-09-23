# WebJam + Logic Pro Companion — Excellence Synthesis (FINAL)

**For:** Jeff Story · **Date:** 2026-09-22 ~10:40 PM CT  
**Status:** SYNTHESIS ONLY — no PRs, no `rupret007/webjam` product code, no Logic implementation  
**Primary spine:** `webjam-logic-EXCELLENCE-RESEARCH.md`  
**This file:** one-page executive cut + Adopt/Defer/Kill + locked P0/P1/P2 + BUILD GATE

---

## Executive answer — what excellence means

Excellence is **not** “WebJam exports a WAV.” Excellence is Jeff moving through four journeys — **Rehearse → Track → Review → Handoff** — with almost no conscious audio engineering, while the band never hears a delayed ghost of WebJam in a take. Concretely: one glance shows REHEARSE (green) or RECORD (red); Record mode **fail-closed mutes WebJam local program before the downbeat** using **MCU feedback as truth** (not optimistic guesses); after Stop, mute holds until Jeff chooses Rehearse; and cold-Mac drag of one `LogicHandoff` folder into Logic yields aligned stems + MIDI + tempo notes with a calm brain — not a second career as an Aggregate Device technician. Logic stays **host-only**; guests rehearse in WebJam/Jamulus; phone-as-transport stays **PARKED**; no Logic Remote reverse engineering.

---

## Sources used

| Source | Path / role |
|---|---|
| **Excellence research (primary)** | `/workspace/research/webjam-logic-EXCELLENCE-RESEARCH.md` — journeys, edge cases, latency matrix, friction map, P0–P3, §7 tests |
| **Prior companion research** | `webjam-logic-pro-companion-20260922.md` — APIs, MCU/MMC/IAC, mute SM, phasing |
| **Build brief** | `webjam-logic-companion-BUILD-BRIEF.md` — goals, non-goals, PR strategy |
| **Gemini ideas** | `sources/gemini-ideas.md` (truncated after Idea 4) — session sync, MIDI re-voice, plugin control, visual latency nudge |
| **Gemini critique** | `critiques/gemini-logic-critique.md` — Record must silence WebJam immediately; BlackHole optional; phone parked |
| **MiniMax critique** | `critiques/minimax-logic-critique.md` — BH exclusive aggregate; MCU mute; phone PARKED; 30 s clean waveform; preflight; rollback |
| **MiniMax excellence** | `sources/minimax-excellence.md` — BWF/iXML, take-first sync-later, transport owner, capability probe, stems-drift acid-test; **do not** adopt magic-link as P0 |
| **Claude Opus plan stamp** | `sources/claude-opus-plan-stamp.md` — affirm kill list + MCU truth; Rehearse/Record = app mute profile; split-mute P0 challenge; bank/UI/ear risks; feel-tests-before-code |
| **This synthesis** | Cuts, gates, and deltas below |

---

## Explicit BUILD GATE (restated — do not skip)

```
NO IMPLEMENTATION until:
  [ ] Jeff reviews excellence research + this synthesis
  [ ] Jeff selects P0/P1 items in / out / defer
  [ ] Each selected item has TESTING-PLAN evidence Jeff accepts
  [ ] Jeff says “quality product OK” (per slice or whole Phase)
  [ ] #149 CI elsewhere; lease respected — no Logic piggyback on red CI
  [ ] No MATCH of #145–#148 without Jeff feel yes
  [ ] Phone transport remains PARKED
  [ ] No Logic Remote reverse engineering
  [ ] Phase order: file-first → MCU mute → optional BlackHole
  [ ] Feel tests in Claude stamp (§ below) proven by hand before mute SM code
```

Until then: north-star backlog + test bible — **not** a build ticket.

**Planning:** highest-tier reasoning. **Implementation (later):** cheaper models OK only against locked acceptance tests.

---

## Constraints already decided (do not reopen casually)

| Decision | Implication |
|---|---|
| Phone-as-transport **PARKED** | Phone may show visual-only cues later — never MMC/MCU send in v1 |
| No Logic Remote RE | MCU/MMC/IAC + files + Link only |
| Phase: file-first → MCU mute → optional BlackHole | Ph1 = handoff feel; Ph2 = clean takes; Ph3 = print-in |
| #149 CI elsewhere; no MATCH without feel yes | Logic waits for green tip / lease |
| Logic is **host-only** | Guests in WebJam/Jamulus; Jeff tracks in Logic |

---

## Claude Opus challenges (folded — mandatory)

### Affirm (ship these decisions)

1. **Kill list is correct, hard:** Logic Remote RE; remote plugin/AU UI control; phone transport.  
2. **MCU feedback truth is the spine:** Mackie Control is bidirectional; Logic echoes LED/state — build mute on **confirmed** feedback, not command inference alone.

### Challenge A — name the product truth

**Rehearse | Record is an APP mute profile, not a Logic feature.**  
Logic has no “Rehearse mode.” WebJam owns the profile (REHEARSE / ARMED / COUNT_IN / RECORDING / PLAYBACK_REVIEW). Logic owns track/transport mute reality as observed via MCU feedback (and Jeff’s ears). Never imply Logic ships these states.

### Challenge B — P0 split-mute boundary (cut-line clarification)

**“Split local vs Jamulus mute” is only excellent when a second Jamulus node confirms by ear.**  
Without that, P0 can only honestly claim **local program mute**.  

**Resolution (forced by Claude; IDs unchanged):**

- **P0-2 / P0-3 / P0-5:** local mute + MCU truth + hold — ship blockers.  
- **P0-4:** keep as *policy + UI* (“remote ON by default while local muted”) but **P0-4 is not DONE** until TESTING-PLAN two-node ear test passes.  
- Do **not** promote BlackHole / Aggregate into P0 (phase order holds).  
- Do **not** market “split done” from button state alone.

Handoff pack (P0-1) and mute/MCU (P0-2+) are **independent tracks** — neither gates the other.

### Top 3 excellence risks (Claude)

| # | Risk | Mitigation |
|---|---|---|
| 1 | **MCU bank addressing fragility** — mute lands on wrong track after bank/reorder | Phase 2 mute uses **transport LEDs** for program mute, not channel bank mute; channel ops later; bank-hold feel test before channel features |
| 2 | **Optimistic UI lying** — shows unmuted / actually muted | UI renders **MCU-confirmed** state only; resync after out-of-band Logic mutes |
| 3 | **Split promise vs ear truth** | Two-node silence/hear confirmation required for P0-4 done |

### Feel tests before any mute SM code (Claude)

1. Mute RTT felt (press → Logic → MCU echo → UI) — target ~&lt;100 ms *confirm*, with echo confirm.  
2. Two-node silence confirmation (partner ear, not button).  
3. Mute hold across Stop/Start and across bank changes.  
4. Recovery after MIDI drop + out-of-band Logic mute — UI re-syncs to Logic truth.

---

## Gemini ideas — Adopt / Defer / Kill

Ruthless filter: **host-only Logic**, **no RE**, **phone transport PARKED**, file-first → MCU → optional BH.

| Idea | Verdict | Why |
|---|---|---|
| **1. Logic Pro Session-Aware Sync** (tempo map, markers, cycle → all companions’ Logic) | **DEFER** | Guests do not run Logic; producer-led *WebJam UI* markers/tempo via Link + `tempo.json` is enough later. Deep multi-Logic sync fights host-only. |
| **2. MIDI Stream Re-Voice** (MIDI → each user’s Logic VI) | **DEFER** | Same host-only conflict. Host-side Notes IAC print remains Phase 2 scope; guest re-voice in their DAW is out of v1 shape. |
| **3. Delegated Plugin Control** (remote AU UI / params) | **KILL** | No remotable AU UI surface; fights host-only; adjacent to forbidden RE / wrong product shape. |
| **4. Visual Latency Nudge & Compensation Markers** (dual playheads / feel offset) | **ADOPT (scoped)** | Scope to **P2-4 adjacent**: show measured RTL / CAPTURE ONLY labeling + optional visual offset marker on WebJam timeline — **not** a claim of sample-accurate BH feel. No dual-DAW playhead fantasy. |
| Phone transport / Logic Remote clone (implied by constraints) | **KILL / PARKED** | Explicit non-goals. |
| Anything requiring guests’ Logic projects | **KILL** | Host-only. |

---

## MiniMax excellence — adoptables & rejects

| Item | Verdict | Where it lands |
|---|---|---|
| **BWF/iXML time-anchored exports** | **ADOPT** | Enrich **P0-1** AC when writer can emit; else **P1-9** hard follow-on. Acid-test: stems land aligned without manual nudge. |
| **Take-first, sync-later** | **ADOPT** | **P1-10** — Logic/WebJam local capture survives network death; companion is control/handoff plane. |
| **Single-source transport owner** | **ADOPT** | **P1-11** (host/Jeff is owner in host-only world); prevents MMC stomps if multi-sender ever appears. |
| **Capability probe** (Logic/OS/IAC readiness panel) | **ADOPT** | Fold into / extend **P1-1 checklist** + **P1-6 version detect**. |
| **Stems drift as acid-test** | **ADOPT** | Hard AC on **P0-1** / T-P0-1 — &gt;~1 ms visible misalignment = fail (“toy”). |
| **Magic-link auth as P0** | **REJECT for P0** | Auth is orthogonal to Logic companion excellence; do not block mute/handoff on SaaS auth shape. |

**MiniMax critique (already in spine):** BH exclusive or room off; MCU Record→mute; phone PARKED; 30 s muted record = clean waveform; preflight; rollback on echo/doubling.

---

## Final P0 / P1 / P2 cut line

**Must agree with excellence research unless Claude/MiniMax forced a change.** Changes noted.

### P0 — without these, not excellent

| ID | Item | Notes / deltas |
|---|---|---|
| P0-1 | LogicHandoff export pack (24-bit WAV/AIFF, SMF Type 1, tempo.json, README) | **MiniMax:** add BWF/iXML timestamps when feasible; **stems-drift acid-test** is pass/fail. Independent of mute track. |
| P0-2 | Rehearse \| Record **app** mute profile + fail-closed local mute | **Claude:** name as app profile, not Logic feature. |
| P0-3 | MCU feedback Record/Stop/Play → mute SM (feedback = truth) | **Claude affirm.** No optimistic UI. |
| P0-4 | Split policy: mute local / Jamulus remote ON (default) | **Claude challenge:** NOT DONE until two-node ear test; no BH promotion into P0. |
| P0-5 | Mute hold after Stop; never auto-unmute in Record mode | Unchanged. |
| P0-6 | BUILD GATE + #149 / feel-yes discipline | Unchanged. |

**Cut-line delta vs excellence research:** none of the P0 *IDs* removed; P0-2 wording clarified (app profile); P0-4 completion criteria tightened (ear proof); P0-1 AC enriched (BWF/iXML + drift acid-test). **No BlackHole in P0.**

### P1 — feels pro

| ID | Item | Notes |
|---|---|---|
| P1-1 | Clean-take checklist (+ capability probe readiness) | MiniMax probe folded here |
| P1-2 | IAC/Mackie setup wizard + port ping | |
| P1-3 | MCU map calibration → saved profile per Logic version | |
| P1-4 | Visual count-in / bar flash (desktop) | |
| P1-5 | WebJam Tracking `.logicx` template + naming contract | |
| P1-6 | Logic version/path detect in status UI | |
| P1-7 | Accessibility: VO, large count-in, no color-only | |
| P1-8 | Mid-take conflict banners + take shield | |
| P1-9 | BWF/iXML hard guarantee (if not finished under P0-1) | **MiniMax delta** |
| P1-10 | Take-first sync-later (control plane resilience) | **MiniMax delta** |
| P1-11 | Single-source transport owner (host) | **MiniMax delta** |

### P2 — differentiators

| ID | Item | Notes |
|---|---|---|
| P2-1 | Ableton Link tempo peer | Link ≠ Record detect |
| P2-2 | Reverse stem watch folder | |
| P2-3 | Phone **visual-only** companion | Transport stays PARKED |
| P2-4 | Latency badge + loopback measure + **scoped visual latency nudge** | **Gemini ADOPT scoped** |
| P2-5 | Offline/reconnect re-assert + wake MIDI refresh | |
| P2-6 | Post-take listen digest | |
| P2-7 | Echo forensics pack | |
| P2-8 | Guest “I hear delay” vote | |

### P3 / killed / parked (do not build)

| ID | Item |
|---|---|
| P3-1 | BlackHole live print-in + Aggregate fingerprint (optional later) |
| P3-2+ | Auto-arm MCU channels, punch/cycle mirror, deep AX/MCP mutation |
| PARKED | Phone transport remote |
| FORBIDDEN | Logic Remote protocol RE |
| KILL | Delegated plugin control (Gemini Idea 3) |
| DEFER | Session-aware multi-Logic sync; guest MIDI re-voice |

---

## Astra Ultra Lightning note

**Product name “Astra Ultra Lightning” does not exist.**  
Closest configured tier: **Astra Ultra** (already in Jeff’s ChatGPT / overnight tooling).  
**Astra Light** is the faster/lighter opposite — not a “Lightning” SKU. Do not plan or prompt against a non-existent Lightning model name.

---

## Canonical mute state machine (short)

States: `REHEARSE` → `ARMED` → `COUNT_IN` → `RECORDING` → `PLAYBACK_REVIEW`

- Mute **local program** when `mode==Record` OR transport in {count-in, recording} OR MCU Record LED on.  
- Unmute only in `REHEARSE` after Stop + unmute delay (200–500 ms).  
- Jamulus remote path = independent flag (default ON); **ear-proven** before calling P0-4 done.  
- UI shows **confirmed** MCU state only.  
- Log every transition.

---

## Phase reminder

1. **Phase 1:** LogicHandoff pack (P0-1) — offline gold.  
2. **Phase 2:** App mute profile + MCU truth (P0-2…5) + P1 checklist/wizard.  
3. **Phase 3:** Optional BlackHole (P3-1) only if Jeff still wants print-in.

---

## Open questions for Jeff (unchanged + one)

1. Default Handoff folder `~/Music/WebJam/LogicHandoff/...` OK?  
2. During Record, keep Jamulus to remotes ON while muting local? (recommended yes — subject to two-node proof)  
3. Feel yes on #145–#148 before MATCH?  
4. When #149 green: polish merge first, or Phase 1 branch from master in parallel?  
5. **New:** Accept P0-4 “done only after two-node ear test,” or prefer renaming P0-4 to “local mute + remote policy (ear proof = P1)”?

---

*End of synthesis. Wait for Jeff review before any product code. Testing plan: `webjam-logic-TESTING-PLAN.md`.*
