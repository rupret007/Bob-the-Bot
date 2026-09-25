# WebJam + Logic Companion — Testing Plan (standalone)

**For:** Jeff Story · **Date:** 2026-09-22 ~10:40 PM CT  
**Extracted/refined from:** Excellence research §7 + Claude Opus feel-tests + MiniMax acid-tests  
**Status:** RESEARCH — no implementation; no merge without evidence Jeff accepts  
**Companion docs:** `webjam-logic-EXCELLENCE-SYNTHESIS.md`, `webjam-logic-EXCELLENCE-RESEARCH.md`

---

## How to use this plan

Each enhancement below has:

- **AC** — acceptance criteria (binary where possible)  
- **How** — procedure  
- **Feels solid** — musician-language bar  
- **Evidence** — what to keep  
- **Pass / Fail** — checkbox lines for Jeff

**Global rules**

1. No enhancement merges without evidence Jeff accepts.  
2. **Feel tests before mute SM code** (Claude): items under *Pre-code feel battery* must pass by hand first.  
3. UI must never claim mute/unmute without MCU-confirmed state (no optimistic lying).  
4. P0-4 is not DONE until two-node ear test passes.  
5. Times reported in America/Chicago (CT).

---

## Pre-code feel battery (Claude — before any mute state-machine code)

### FEEL-1 Mute round-trip, felt

- **AC:** Press → Logic mutes → MCU echo → UI confirms; confirm arrives (not command-only); feels ~&lt;100 ms to a player.  
- **How:** MIDI Monitor + WebJam UI + speakers; press Record path; watch confirm, not just send.  
- **Feels solid:** No double-press fights; confirm is trustworthy.  
- **Evidence:** Screen recording + MIDI Monitor log with CT timestamps.  
- Pass: [ ] · Fail: [ ]

### FEEL-2 Two-node silence confirmation

- **AC:** Second Jamulus participant confirms by ear that muted local source behavior matches policy (local silent / remote still or not per flag).  
- **How:** Two machines; one host, one guest; flip Record mode; guest reports what they hear.  
- **Feels solid:** Split is real in the room, not only on a button.  
- **Evidence:** Both-side notes or short video + guest quote.  
- Pass: [ ] · Fail: [ ]

### FEEL-3 Mute hold across Stop / bank

- **AC:** After Stop, local stays muted while still in Record mode; bank change does not silently unmute or repoint transport-LED mute.  
- **How:** Record → Stop (stay Record mode) → bank left/right → observe mute + UI.  
- **Feels solid:** No surprise blast; bank does not sabotage transport mute.  
- **Evidence:** Screen recording + log.  
- Pass: [ ] · Fail: [ ]

### FEEL-4 Recovery after MIDI drop + out-of-band Logic mute

- **AC:** After IAC blip or human mute inside Logic, app re-syncs to Logic truth; no stale unmuted UI.  
- **How:** Unplug/disable IAC briefly mid-ARMED; mute a track in Logic UI; wake/re-enable; compare UI vs reality.  
- **Feels solid:** Trust survives disconnects and hands-on Logic edits.  
- **Evidence:** Log with CT timestamps + screenshots before/after.  
- Pass: [ ] · Fail: [ ]

---

## P0

### P0-1 LogicHandoff pack

- **AC:** Pack contains audio + MIDI + tempo/README; SR documented; drag into Logic yields aligned lengths. **MiniMax acid-test:** stems do not drift on import (fail if audible/visible misalignment that needs manual nudge). **BWF/iXML:** when writer supports, timestamps anchor timeline without nudge; if not yet, track under P1-9 but acid-test still applies via tempo.json + equal lengths.  
- **How:** Export after a 30 s session stub; import on clean / template project; play; zoom arrange for alignment.  
- **Feels solid:** Jeff doesn’t rename files or hunt folders; “this is the take” in &lt;60 s.  
- **Evidence:** Folder listing + Logic arrange screenshot + `tempo.json` (+ BWF/iXML dump if present).  
- Pass: [ ] · Fail: [ ]

### P0-2 Rehearse | Record app mute profile + fail-closed local mute

- **AC:** Mode toggle drives app profile (not a Logic feature). Entering Record/ARMED mutes WebJam **local program immediately**. Play-only in Logic does not unmute while mode==Record.  
- **How:** WebJam playing → switch to Record → observe speakers before any Logic Record press; then arm + Record.  
- **Feels solid:** No “I forgot to mute”; speakers die before downbeat.  
- **Evidence:** Screen recording of mode badge + speaker observation notes.  
- Pass: [ ] · Fail: [ ]

### P0-3 MCU feedback → mute state machine

- **AC (Gemini):** WebJam playing → arm Logic track → Record (from Logic UI) → local audio ceases immediately; Stop + Rehearse → returns. MCU Record LED is truth; command inference alone is insufficient.  
- **How:** MIDI Monitor confirms Record note; press Record **only inside Logic**; observe mute; corrupt/ignore command-side path.  
- **Feels solid:** Mute survives Record pressed inside Logic; UI matches LED.  
- **Evidence:** MIDI Monitor log + UI recording + mute SM log.  
- Pass: [ ] · Fail: [ ]

### P0-4 Split policy (local mute / Jamulus remote ON)

- **AC:** Policy flag defaults remote ON while local muted. **DONE only if FEEL-2 passes** (guest still hears network path when policy ON; local speakers silent). Without FEEL-2: mark **Incomplete** — do not claim split shipped.  
- **How:** Host Record mode; guest on Jamulus confirms hearing; host speakers silent.  
- **Feels solid:** Band still gets cues; capture stays clean.  
- **Evidence:** Guest confirmation + host speaker proof.  
- Pass: [ ] · Fail: [ ] · Incomplete (no ear proof): [ ]

### P0-5 Mute hold after Stop

- **AC:** Stop alone does not unmute; unmute only after Rehearse + hold (200–500 ms); never auto-unmute in Record mode.  
- **How:** RECORDING → Stop → wait → confirm still muted → Rehearse → unmute after hold.  
- **Feels solid:** No buffer-tail bleed into next action.  
- **Evidence:** Waveform at stop boundary + SM log.  
- Pass: [ ] · Fail: [ ]

### P0-6 Build gate / process

- **AC:** No Logic companion PR while #149 red / lease blocked; no MATCH without feel-yes note; phone transport parked; no Logic Remote RE.  
- **How:** Process check against board + this synthesis.  
- **Feels solid:** Jeff never surprised by drive-by Logic code.  
- **Evidence:** Status note listing PR non-existence / links.  
- Pass: [ ] · Fail: [ ]

---

## P1

### P1-1 Clean-take checklist (+ capability probe)

- **AC:** Record mode blocked (or warning+ACK) if IAC missing, MCU ping fail, SR mismatch, BH unexpectedly on, dual monitor. Readiness panel names concrete fix (MiniMax probe).  
- **How:** Break each precondition deliberately; confirm catch.  
- **Feels solid:** Pilot checklist trust.  
- **Evidence:** Screenshots per failure injection.  
- Pass: [ ] · Fail: [ ]

### P1-2 IAC / Mackie setup wizard

- **AC:** From cold settings, wizard creates/verifies `WebJam MCU Cmd`, `WebJam MCU Fb`, `WebJam Notes`; explains Mackie install; ping passes.  
- **How:** Disable IAC; run wizard; add surface in Logic; ping.  
- **Feels solid:** Non-MIDI-expert finishes in one sitting.  
- **Evidence:** Before/after Audio MIDI Setup + Control Surfaces screenshots.  
- Pass: [ ] · Fail: [ ]

### P1-3 MCU map calibration

- **AC:** Captured map survives relaunch; wrong/corrupt map fails closed (stay muted in Record).  
- **How:** Calibrate; relaunch; Record; corrupt `logic-mcu-map.json`; confirm safe mute.  
- **Feels solid:** “It just knows my Logic.”  
- **Evidence:** Map file + MIDI Monitor capture.  
- Pass: [ ] · Fail: [ ]

### P1-4 Visual count-in (desktop)

- **AC:** Guests see synchronized bar/beat flash for configured count-in; reduced-motion alt works.  
- **How:** Two machines; start count-in; film both.  
- **Feels solid:** Band hits together without click on capture bus.  
- **Evidence:** Side-by-side video.  
- Pass: [ ] · Fail: [ ]

### P1-5 Template `.logicx`

- **AC:** Handoff names match template tracks; SR matches README; markers optional.  
- **How:** Open template; import pack; play.  
- **Feels solid:** Zero track-creation busywork.  
- **Evidence:** Arrange screenshot with named tracks.  
- Pass: [ ] · Fail: [ ]

### P1-6 Logic version / path detect

- **AC:** UI shows correct Logic version or “Logic not found”; unknown version prompts calibrate.  
- **How:** Logic closed/open; optional unknown-version harness.  
- **Feels solid:** Status line trusted when debugging.  
- **Evidence:** Status UI screenshots.  
- Pass: [ ] · Fail: [ ]

### P1-7 Accessibility

- **AC:** VO announces mode/mute; count-in readable at large text; color not sole indicator; keyboard can toggle mode / export handoff / focus checklist.  
- **How:** VoiceOver walkthrough; large text screenshot; keyboard-only path.  
- **Feels solid:** Mode awareness without sighted helper.  
- **Evidence:** VO recording or annotated screenshots.  
- Pass: [ ] · Fail: [ ]

### P1-8 Mid-take conflict / take shield

- **AC:** Attempted unmute / mode flip during Record LED on is blocked or confirmed; ledger entry written; BH enable / local volume automation disabled while LED on.  
- **How:** Record; try Rehearse; confirm dialog/block; Stop; then Rehearse works.  
- **Feels solid:** Impossible to accidentally blast speakers mid-take.  
- **Evidence:** Screen recording + ledger snippet.  
- Pass: [ ] · Fail: [ ]

### P1-9 BWF/iXML time-anchored exports (MiniMax)

- **AC:** WAV exports carry BWF/iXML time anchors derived from session clock; drop into Logic → tracks auto-position (or documented equivalent); acid-test vs manual nudge.  
- **How:** Export; inspect chunks; import; verify timeline position.  
- **Feels solid:** No scrubbing to line up takes.  
- **Evidence:** Chunk dump + arrange screenshot.  
- Pass: [ ] · Fail: [ ] · N/A (folded into P0-1): [ ]

### P1-10 Take-first, sync-later (MiniMax)

- **AC:** Killing WebJam/network mid-take does not destroy Logic capture; handoff/upload can complete after reconnect.  
- **How:** Start take; kill companion network; finish in Logic; reconnect; export/handoff.  
- **Feels solid:** Companion is control plane; take survives.  
- **Evidence:** Timeline of events (CT) + resulting take file.  
- Pass: [ ] · Fail: [ ]

### P1-11 Single-source transport owner (MiniMax)

- **AC:** Only designated owner (host/Jeff) sends MMC/MCU transport; secondary sender is refused or queued behind explicit override.  
- **How:** Attempt second sender while owner active; confirm no phantom Stop/Start.  
- **Feels solid:** No transport fights.  
- **Evidence:** MIDI Monitor showing single command source.  
- Pass: [ ] · Fail: [ ]

---

## P2

### P2-1 Ableton Link

- **AC:** Tempo/phase align within Link tolerance; Record mute still MCU-driven (Link start ≠ Record).  
- **How:** Enable Link both sides; change BPM; Record only in Logic UI.  
- **Feels solid:** Click agrees; mute still correct.  
- **Evidence:** BPM screenshots + mute log during Link play.  
- Pass: [ ] · Fail: [ ]

### P2-2 Reverse stems

- **AC:** Drop Logic bounce into watch folder → appears in WebJam play-along.  
- **How:** Bounce; wait; play in WebJam.  
- **Feels solid:** No manual re-encode.  
- **Evidence:** Finder + WebJam UI screenshots.  
- Pass: [ ] · Fail: [ ]

### P2-3 Phone visual-only

- **AC:** Phone shows count-in/ROLLING; **no** transport controls send MIDI; killing phone app doesn’t Stop Logic.  
- **How:** Use phone during take; MIDI Monitor shows no phone MMC/MCU.  
- **Feels solid:** Eyes on stand, hands free, zero control risk.  
- **Evidence:** Phone video + MIDI Monitor.  
- Pass: [ ] · Fail: [ ]

### P2-4 Latency badge + scoped visual latency nudge (Gemini adopt)

- **AC:** Measured RTL shown; paths &gt; threshold marked CAPTURE ONLY; optional dual visual marker/nudge on WebJam timeline for feel offset — **does not** claim sample-accurate BH monitoring.  
- **How:** Loopback measure vs known buffer; compare badge; exercise nudge UI if present.  
- **Feels solid:** Jeff believes the number; nudge is honest, not magical.  
- **Evidence:** Measurement WAV + badge (+ nudge) screenshot.  
- Pass: [ ] · Fail: [ ]

### P2-5 Reconnect / wake

- **AC:** After sleep or IAC blip in Record mode, local stays muted; health recovers; UI matches MCU.  
- **How:** Sleep 1 min mid-ARMED; wake; verify mute + ports.  
- **Feels solid:** No surprise blast after lid open.  
- **Evidence:** Log with CT timestamps.  
- Pass: [ ] · Fail: [ ]

### P2-6 Listen digest

- **AC:** One action produces shareable rough mix link/file.  
- **How:** After take; run digest; open on second device.  
- **Feels solid:** Band hears take tonight.  
- **Evidence:** Share link + file.  
- Pass: [ ] · Fail: [ ]

### P2-7 Echo forensics pack

- **AC:** Pack contains mute SM + MCU summary, no secrets.  
- **How:** Trigger echo report; inspect pack.  
- **Feels solid:** Debug without recreating from memory.  
- **Evidence:** Redacted pack sample.  
- Pass: [ ] · Fail: [ ]

### P2-8 Guest delay vote

- **AC:** Guest tap forces host local mute + banner.  
- **How:** Simulate guest vote during REHEARSE with speakers on.  
- **Feels solid:** Band can save a take socially.  
- **Evidence:** UI recording both sides.  
- Pass: [ ] · Fail: [ ]

---

## P3

### P3-1 BlackHole live print-in (optional; Jeff must still want)

- **AC (MiniMax-aligned):** Aggregate clock = interface; BH secondary + drift; room not double-feeding; 30 s record with WebJam muted = clean waveform; unmute mapping doesn’t howl; badge says CAPTURE ONLY. Deliberate mis-clock must fail preflight.  
- **How:** Full Aggregate recipe; mis-clock injection; 30 s take; rollback drill if echo.  
- **Feels solid:** Print-in without ticks/echo.  
- **Evidence:** AMS Aggregate screenshot, waveform, RTL badge, rollback note if failed.  
- Pass: [ ] · Fail: [ ] · Deferred (Jeff no): [ ]

---

## Regression battery (every Phase 2+ build)

1. [ ] REHEARSE speakers audible.  
2. [ ] RECORD mutes before audible downbeat.  
3. [ ] Stop alone does not unmute.  
4. [ ] Rehearse after Stop unmutes after hold.  
5. [ ] Handoff pack still imports (acid-test alignment).  
6. [ ] MCU unplugged → fail-closed in Record mode.  
7. [ ] UI mute state matches MCU LED (no optimistic lie).  
8. [ ] FEEL-2 still green if claiming P0-4 done.

---

## Sign-off

| Role | Name | Date (CT) | Notes |
|---|---|---|---|
| Jeff review | | | |
| Slice “quality product OK” | | | which IDs: |
| Evidence accepted | | | paths: |

*End of testing plan. No code until BUILD GATE + feel battery + per-ID evidence.*
