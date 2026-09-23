# WebJam ↔ Logic Companion — Build Brief
Date: 2026-09-22 ~10:34 PM CT · Research → build plan (no repo patches until #149 green + lease free)

## Goals
1. Logic-ready handoff: stems (WAV/AIFF) + MIDI + tempo/map notes into a droppable folder.
2. Rehearse vs Record mode: mute WebJam local program when Logic is recording; unmute in Rehearse after Stop.
3. Local MIDI bridge: IAC + MMC/Mackie transport; MCU feedback LEDs drive mute; optional Ableton Link later.
4. Experience: session invite link, visual count-in, stem folders both ways, clean-take checklist.

## Non-goals (now)
- Phone-as-transport remote (**PARKED**)
- Logic Remote protocol reverse engineering
- NDA Control Surface Plug-in SDK
- BlackHole live capture as default (Phase 3 optional only)
- MATCH/squash of #145–#148 without Jeff **feel yes**
- Touching parked #37/#49; VFON/Che stems outreach

## Phasing

### Phase 1 — Logic-ready export (FIRST CODE after ship-wave)
- Export pack writer: Broadcast WAV/AIFF 24-bit @ project SR, SMF Type 1, `tempo.json` / README with SR, tempo, bar markers.
- Default folder: `~/Music/WebJam/LogicHandoff/<session>-<timestamp>/`
- Acceptance: drop folder into Logic; tracks import with matching length/tempo notes; no network required.

### Phase 2 — Rehearse/Record + MIDI bridge
- UI mode toggle: Rehearse | Record
- Mute state machine: REHEARSE → ARMED → COUNT_IN → RECORDING → PLAYBACK_REVIEW (see research §6)
- Bridge helper or in-process CoreMIDI: IAC `WebJam MCU Cmd` / `WebJam MCU Fb` / `WebJam Notes`
- Detect Record via MCU feedback (community map: Play≈94, Stop≈93, Record≈95 ch1) — verify with MIDI Monitor on Jeff’s Mac
- MMC Listen as command path; MCU feedback as truth for mute
- Acceptance (Gemini-aligned): WebJam playing; arm Logic track; press Record → WebJam local audio ceases immediately; Stop + Rehearse → returns

### Phase 3 — BlackHole (optional)
- Only if Jeff still wants live print-in; Aggregate Device checklist; latency badge
- Fail-closed: BlackHole feed off unless Record mode explicitly enables “print mix”

### Experience extras (with Phase 1–2)
- Session invite link (WebJam room; Logic stays host-only)
- Visual count-in cues (bar flash for remotes)
- Stem folders both ways (Logic export → WebJam play-along watch folder)
- Clean-take checklist UI before Record

## PR strategy
- Do **not** stack on #149 while red.
- After #145–#149 wave settled (or parallel **new branch from master** only if lease free and scope won’t collide): `feat/logic-handoff-phase1` then `feat/logic-companion-bridge`.
- Current lease: grok on #149 CI fix — Logic code waits for green tip + lease handoff.

## Mac setup checklist (Jeff)
1. Audio MIDI Setup → IAC online; ports: WebJam MCU Cmd, WebJam MCU Fb, WebJam Notes
2. Logic → Control Surfaces → Add Mackie Control (Cmd in / Fb out)
3. Filter MCU IAC from track MIDI inputs
4. Enable Listen to MMC Input
5. MIDI Monitor verify Record LED notes while recording

## Open questions for Jeff
1. Default Handoff folder path OK?
2. During Record, keep Jamulus to remotes ON while muting local speakers? (recommended default: yes)
3. Feel yes on #145–#148 before MATCH?
4. When #149 green: merge polish stack first, or start Phase 1 branch from current master in parallel?

## Critiques folded in
- Gemini: highest echo = WebJam local out mixing into Logic inputs; acceptance = Record must silence WebJam immediately
- MiniMax: BlackHole+room dual route is bleed vector; aggregate must isolate; preflight checklist before takes
