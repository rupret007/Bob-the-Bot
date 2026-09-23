# WebJam + Logic Pro Companion — Excellence Research (OUTSIDE THE BOX)

**For:** Jeff Story · **Date:** 2026-09-22 ~10:40 PM CT  
**Status:** RESEARCH ONLY — no PRs, no `rupret007/webjam` product code changes  
**Builds on:** `webjam-logic-pro-companion-20260922.md`, `webjam-logic-companion-BUILD-BRIEF.md`, Gemini/MiniMax critiques, prior Logic/Bob handoff research  
**Planning note:** Use highest-tier reasoning for planning/review. Implementation later may use cheaper models once acceptance tests are locked.

---

## Explicit BUILD GATE (read first)

**Do not implement any enhancement in this doc until all of the following are true:**

1. Jeff has **reviewed this document** and marked items in / out / deferred.  
2. Each chosen enhancement has a **passing test plan** (Section 7) with evidence Jeff accepts.  
3. Jeff explicitly says **“quality product OK”** (or equivalent) for that slice.  
4. Ship-wave constraints still hold: **#149 CI elsewhere**; **no MATCH** of #145–#148 without Jeff **feel yes**; phone-as-transport-remote stays **PARKED**; **no Logic Remote reverse engineering**.  
5. Product phasing remains: **file-first → MCU mute → optional BlackHole**.

Until then: this file is a north-star backlog and test bible, not a build ticket.

---

## Constraints already decided (do not reopen casually)

| Decision | Implication for excellence |
|---|---|
| Phone-as-transport-remote **PARKED** | Phone may still show **visual-only** cues (count-in, bars, “Rolling”) — never transport control in v1 |
| No Logic Remote RE | MCU/MMC/IAC + files + Link only |
| Phase: file-first → MCU mute → optional BlackHole | Excellence in Phase 1 is *handoff feel*; Phase 2 is *clean takes*; Phase 3 is *print-in* |
| #149 CI elsewhere; no MATCH without feel yes | Logic work waits for green tip / lease; do not piggyback polish PRs |
| Logic is host-only | Guests rehearse in WebJam/Jamulus; Jeff tracks/arranges in Logic |

---

## 1. Excellence north star

**Excellence ≠ “it exports WAV.”**  
Excellence = Jeff can move through four journeys with **almost no conscious audio engineering**, and the band never hears a delayed ghost of WebJam in a take.

### Journey A — Rehearsal (band feel)

**Who:** Host + remote players  
**Goal:** Tight Jamulus feel, shared tempo, clear “where are we,” zero Logic capture risk.

**Excellent looks like:**
- One glance: mode badge **REHEARSE** (green).  
- WebJam local program ON for feel bus; BlackHole feed **OFF** by default.  
- Visual count-in / bar flash for remotes (desktop primary; phone visual-only later).  
- Optional Ableton Link shared BPM/phase with Logic if Jeff has Logic open for click/arrangement — but Link does **not** equal Record.  
- Preflight silent: no Aggregate Device required; no IAC required for pure rehearsal.

**Musician test:** “We can run the song twice without me opening Audio MIDI Setup.”

### Journey B — Tracking take (clean capture)

**Who:** Jeff hosting; band may stay on Jamulus for cue  
**Goal:** Record into Logic without delayed WebJam bleed, without dual beds, without “wait, which speakers are on?”

**Excellent looks like:**
- Mode → **RECORD** (red). Fail-closed: WebJam **local program muted immediately** (and stays muted while mode==Record).  
- Clean-take checklist must pass (or Jeff overrides with typed ACK).  
- MCU feedback Record LED is truth for mute; MMC/MCU commands optional.  
- Jamulus to remotes stays ON by default (policy flag); room/BlackHole program OFF.  
- Click/count-in prefer Logic headphones; WebJam click not on BlackHole.  
- After Stop: short mute hold (200–500 ms) → PLAYBACK_REVIEW → ARMED or REHEARSE.

**Musician test:** Arm track, hit Record with WebJam still “playing” in session UI — **speakers go quiet before the downbeat**; take waveform has no delayed bed.

### Journey C — Review (playback / decide keep)

**Who:** Jeff (+ band listening on call or later digest)  
**Goal:** Hear the take in Logic context without flipping WebJam back on too early.

**Excellent looks like:**
- Mode stays RECORD/ARMED until Jeff chooses Rehearse.  
- Play-only in Logic does **not** auto-unmute WebJam.  
- Optional: “Send listen digest” bounce path (rough mix → Drive/Samply) — already cultural fit.  
- Take markers / chat cue “keep verse 2” pinned to session log.

**Musician test:** “I can A/B take 3 vs take 4 without WebJam suddenly blasting speakers.”

### Journey D — Handoff (Logic-ready pack)

**Who:** Jeff after session  
**Goal:** Drag one folder into Logic; stems + MIDI + tempo notes just work.

**Excellent looks like:**
- Pack at `~/Music/WebJam/LogicHandoff/<session>-<timestamp>/` (confirm path with Jeff).  
- 24-bit WAV/AIFF @ project SR, SMF Type 1, `tempo.json` + README (SR, BPM, bar markers, sample-rate warning).  
- Naming that matches a **template `.logicx`** track list (see §5).  
- Offline, no network, no MCU required.  
- Reverse folder optional: Logic bounce → WebJam play-along watch folder.

**Musician test:** Cold Mac, no bridge: drop folder → tracks line up → play → “this is the take.”

### North-star one-liner

> After a WebJam night, Jeff has **clean Logic tracks and a calm brain** — not a second career as an Aggregate Device technician.

---

## 2. Edge cases & failure modes

These are the excellence killers. Each needs detect → message → safe default.

### 2.1 Logic mid-take conflict

| Scenario | Failure | Excellence response |
|---|---|---|
| Jeff hits Record in Logic while WebJam still in REHEARSE | Delayed program into room/mic | MCU Record LED → force ARMED mutes + banner “Logic recording — WebJam speakers muted” |
| Jeff presses Stop in Logic but WebJam thinks still recording | Stuck mute or early unmute | Prefer MCU feedback over last-command; unmute only on REHEARSE + Stop + hold |
| Jeff punches Record from Logic UI only (never sent MMC from WebJam) | Command-side mute misses | **MCU feedback is required truth**; command inference is fallback only |
| Two WebJam instances / orphan helper | Competing mute / MIDI storms | Single-owner lock; refuse second bridge; log PID |
| Take running + Jeff flips mode to Rehearse | Accidental unmute mid-take | Confirm dialog if MCU Record LED on; never silent unmute while LED on |

### 2.2 Version / path detect

| Scenario | Failure | Excellence response |
|---|---|---|
| Logic 10.x vs 11.x MCU quirks | Wrong LED map; mute never fires | Detect Logic version (bundle short version); store verified note map per version after MIDI Monitor calibration |
| Nonstandard install path / multiple Logic apps | Open wrong app / AppleScript miss | Prefer file handoff; if “Open template,” resolve via `mdfind`/`LSFindApplication` + user pick once |
| Logic not running | Bridge hangs | Status: “Logic offline — handoff still works; mute bridge idle” |
| Control surface deleted after Logic update | No MCU Fb | Preflight red: “Mackie Control missing”; fall back to manual Record mode mute only |

### 2.3 Offline / reconnect

| Scenario | Failure | Excellence response |
|---|---|---|
| IAC ports disappear (Audio MIDI Setup glitch) | Silent mute failure | Health heartbeat every N s; surface “IAC lost — fail-closed MUTE if mode==Record” |
| Network drop (Jamulus) during take | Band confusion; Jeff distracts | Keep Logic take going; show “guests reconnecting”; do **not** auto-Stop Logic |
| Host sleep / display sleep | MIDI ports stall | On wake: re-enumerate CoreMIDI; re-subscribe MCU Fb; re-assert mute from mode+LED |
| Laptop lid / interface unplug mid-session | Clock loss, Aggregate break | Hard banner + stop recommending BlackHole path until preflight green |

### 2.4 Sample-rate mismatch

| Scenario | Failure | Excellence response |
|---|---|---|
| WebJam/Jamulus 48 kHz, Logic project 44.1 | Import stretch / SR dialog / drift on live path | Handoff README declares SR; checklist compares Logic project SR vs export SR; refuse live BlackHole arm if mismatch |
| BlackHole stuck at different SR | Clicks, weird pitch | Preflight reads CoreAudio nominal SR for BH + interface; one-click “Set all to 48 kHz” guidance (user confirms in AMS) |
| Export 48k into 44.1 template | Jeff accepts convert without noticing | Template ships documented SR; pack warns in UI before write |

### 2.5 IAC missing / miswired

| Scenario | Failure | Excellence response |
|---|---|---|
| IAC Driver offline | No MCU | Setup wizard: enable IAC Device; create `WebJam MCU Cmd`, `WebJam MCU Fb`, `WebJam Notes` |
| Cmd/Fb swapped | Feedback on wrong port; mute never sees Record | Wizard “ping test”: send note, expect echo pattern; label ports clearly |
| MCU buses not filtered from track inputs | MIDI freeze / notes on instrument tracks | Checklist step + doc: filter MCU IAC from sequencer inputs |
| Extra MIDI clock on shared bus | Timing weirdness | Dedicated buses only; never share Notes bus with MCU |

### 2.6 MCU feedback loss

| Scenario | Failure | Excellence response |
|---|---|---|
| Feedback LED map wrong for Jeff’s build | False unmute | Calibration ritual: Record 2 s → capture note/vel → save profile `logic-mcu-map.json` |
| Logic 11.x surface regressions | Intermittent LEDs | Treat missing Record LED while mode==Record as **still muted**; never “assume stopped” |
| Surface bank shifted | Channel mute/arm wrong | Phase 2 only uses **transport** LEDs for mute; channel ops later |

### 2.7 Dual playback (same bed twice)

| Scenario | Failure | Excellence response |
|---|---|---|
| WebJam backing + Logic backing both audible | Comb filter / confusion / bleed | RECORD mode: WebJam local bed OFF; prefer Logic as sole bed OR WebJam network-only bed |
| Direct monitor + Logic software monitor | Hollow/phasey self | Checklist: pick one monitor path; disable the other |
| BlackHole print + room speakers | Echo into mics | MiniMax critique: BH exclusive or room off; fail closed |

### 2.8 Aggregate Device mis-clock

| Scenario | Failure | Excellence response |
|---|---|---|
| Built-in / AirPods as clock master | Drift, ticks, shredded audio | Preflight: hardware interface = clock source; BlackHole = secondary + drift correction |
| Drift correction on master | Subtle warble | Detect and warn |
| Device disconnects | Aggregate dies mid-take | Abort guidance; do not silently continue “recording” silence that looks like a take |
| Multi-output including Bluetooth | Huge latency | Block BlackHole Phase 3 if BT device in aggregate |

### 2.9 Other excellence-grade edges

- **Room mic open + WebJam speakers:** fail-closed mute in Record.  
- **Guest “I hear delay” vote:** host forces mute (social fail-safe).  
- **Permissions:** Accessibility/Automation only if later helper needs UI; Phase 1 needs none.  
- **Sandbox / App Store later:** CoreMIDI entitlements — stay GitHub desktop for now.  
- **Multiple aggregate recipes on Jeff’s Mini:** store last-known-good fingerprint (device UIDs + SR + clock).

---

## 3. Latency & monitoring matrix

Separate three buses. Never let a delayed bus pretend to be the feel bus.

### 3.1 Perception budgets (musician-practical)

| Round-trip feel | Musician experience | Use for |
|---|---|---|
| **&lt; ~6–10 ms** | “Immediate” | Feel bus / tracking self-monitor |
| **~10–20 ms** | Noticeable on tight rhythm | Borderline software monitor |
| **&gt; ~20–30 ms** | Fight the delay | Capture/print OK; **not** feel |
| **Virtual audio WebJam→BH→Logic→HP** | Often well into “noticeable” | Capture bus only |

Rule of thumb: sound ≈ 1 ft/ms; 10 ms ≈ standing 10 ft from an amp.

### 3.2 Bus matrix

| Bus | What it is | Latency target | Who hears it | When ON |
|---|---|---|---|---|
| **Feel bus** | Jamulus / WebJam low-latency monitor (interface direct or WebJam local) | As low as Jamulus path allows; no BH detour | Band + host while REHEARSE | REHEARSE; OFF local in RECORD |
| **Capture bus** | Dry mic/DI → Logic inputs (hardware); optional BH print-in | Irrelevance to *feel*; must be clean | Nobody “feels” it — it records | Always for armed tracks; BH feed only if explicit |
| **Logic software monitor** | Logic Input Monitoring / Low Latency Mode path | Prefer &lt;10 ms RTL or use **interface direct monitor** | Host headphones during RECORD | RECORD; mutually exclusive with dual direct+soft |

### 3.3 Mode × bus policy

| Mode | Feel (WebJam local) | Jamulus remote | BlackHole WebJam→Logic | Logic click/HP | Logic software monitor |
|---|---|---|---|---|---|
| REHEARSE | ON | ON | OFF (default) | Optional | Off / don’t care |
| ARMED | **MUTE** | ON (default) | OFF unless “print mix” | Ready | Prefer interface direct |
| COUNT_IN / RECORDING | **MUTE** | ON (default) | OFF unless explicit | ON | Per Jeff preference |
| PLAYBACK_REVIEW | MUTE until Rehearse | ON | OFF | Logic playback | n/a |

### 3.4 Measurement (what “feels solid” needs)

For any BlackHole / software-monitor claim:

1. Record click out → loop back in (or measure HP out with second input).  
2. Report **measured RTL ms** in UI badge (not buffer size alone).  
3. If RTL &gt; threshold (suggest **15 ms** warn, **25 ms** hard-warn for “feel”), label path **CAPTURE ONLY**.  
4. Evidence: screenshot of badge + short WAV of loopback click offset.

### 3.5 Anti-patterns

- Using BlackHole as the band’s primary monitor.  
- Dual monitoring (direct + Logic Input Monitoring) without muting one.  
- Expecting Logic PDC to fix WebJam↔BH round-trip.  
- Muting late / unmuting early around buffer edges — mute early (count-in), unmute late (Stop + margin).

---

## 4. Workflow friction map

Steps Jeff still does by hand today → eliminate / automate / acknowledge.

| # | Manual step today | Pain | Action | Phase |
|---|---|---|---|---|
| 1 | Bounce/export stems from WebJam/Studio by hand, rename, find folder | Easy to misplace take | **Eliminate:** one-click LogicHandoff pack | P0 / Ph1 |
| 2 | Remember sample rate / tempo for Logic import | SR dialog / wrong feel | **Automate:** `tempo.json` + README; UI warn | P0 / Ph1 |
| 3 | Create matching tracks / drag each stem | Slow after long night | **Automate partially:** naming ≡ template; optional later import helper | P1 / Ph1–2 |
| 4 | Mute WebJam speakers before Record | Echo if forgotten | **Eliminate:** Record mode + MCU mute | P0 / Ph2 |
| 5 | Watch Logic Record LED mentally | Cognitive load | **Automate:** MCU Fb → mute state machine | P0 / Ph2 |
| 6 | Enable IAC + add Mackie Control + filter MIDI | One-time but scary | **Automate:** setup wizard + ping test; **acknowledge** first-time 5 min | P1 / Ph2 |
| 7 | MIDI Monitor to verify note map | Expert-only | **Automate:** calibration capture → saved profile | P1 / Ph2 |
| 8 | Build Aggregate Device / set clock / drift | Easy to get wrong | **Acknowledge** until Ph3; then checklist + fingerprint | P2 / Ph3 |
| 9 | Choose direct vs software monitor | Dual-path comb filter | **Automate:** checklist forces exclusive choice | P1 / Ph2 |
| 10 | Tell band “rolling” / bar cues verbally | Misses on latency | **Automate:** visual count-in + “ROLLING” badge | P1 |
| 11 | Keep Jamulus up while muting local | Confusing toggle | **Automate:** split policies (local vs remote) | P0 / Ph2 |
| 12 | Post-take share rough mix | Context switch | **Acknowledge / light automate:** digest export button | P2 |
| 13 | Open correct Logic template | Wrong SR/track layout | **Automate:** “Open WebJam Tracking template” + path detect | P1 |
| 14 | Reconnect after sleep / cable yank | Mystery silence | **Automate:** wake re-enumerate + status | P2 |
| 15 | Phone transport across room | PARKED | **Acknowledge:** parked; visual cues only later | — |
| 16 | Match feel of polish PRs (#145–#148) | Premature MATCH | **Acknowledge:** feel yes required; CI #149 separate | — |

**Highest-leverage friction kills:** 1, 4, 5, 11, then 6–7, then 10, then 13.

---

## 5. New ideas (beyond prior research)

Prior research covered Rehearse/Record, MCU mute, Link, stem folders, clean-take checklist, latency badge. Below are **excellence deltas** and parked-adjacent ideas that stay inside constraints.

### 5.1 Auto-detect Logic version / path

- On bridge start: resolve Logic Pro bundle, short version, build.  
- Load MCU map profile for that version; if unknown → guided calibration.  
- Show in UI: `Logic 11.x · MCU map: jeff-mac-mini · last verified <date>`.  
- Never guess silently across major versions.

### 5.2 Template `.logicx` projects

Ship / document **WebJam Tracking** templates (folder-format project preferred for sidecars):

- Track list aligned to handoff names: `Kick`, `Snare`, `BassDI`, `Gvox`, `RefBed` (muted), `Click`.  
- Project SR locked (48 kHz recommended for Jamulus world).  
- Low Latency Mode friendly; Input Monitoring off by default; metronome count-in 1 bar.  
- Markers placeholders: Intro / Verse / Chorus from `structure.json` when present.  
- README in template: “Import Handoff folder → these track names.”  
- Optional: empty software instrument tracks pre-routed to `WebJam Notes` IAC for MIDI print.

### 5.3 Conflict handling mid-take (richer than mute SM)

- **Conflict ledger:** timestamped events (MCU Record on, mode flip attempted, IAC lost).  
- **Non-modal banner** with one primary action: “Keep recording (stay muted)” vs “Abort to Rehearse.”  
- **Take shield:** while Record LED on, disable WebJam local volume automation and BH enable.  
- **Orphan take detector:** if Record LED on but no audio peaks N seconds → warn “recording silence?”

### 5.4 Offline / reconnect excellence

- Handoff pack always works offline (gold).  
- Bridge: offline queue of mode intents; on reconnect re-assert mute from **mode ∧ LED**.  
- Guests: visual “host tracking — local program muted” even if chat blips.  
- Never auto-stop Logic because Jamulus dropped.

### 5.5 Accessibility (first-class, not afterthought)

- **VoiceOver** on WebJam mode badge, mute state, checklist failures (spoken “Record mode, speakers muted”).  
- Large Dynamic Type for count-in numerals (1…2…3…4).  
- Reduced-motion alternative: high-contrast bar counter, no strobe.  
- Don’t rely on color alone (red mode + text RECORDING).  
- Align with Logic’s own VO/controls-view reality: companion should be *more* accessible than plugging third-party AU UIs.  
- Keyboard-only: Mode toggle, Export Handoff, Focus checklist.

### 5.6 Mobile companion BEYOND parked transport remote

Phone-as-**transport** stays PARKED. Phone-as-**eyes** is fair game:

| Idea | What | Why excellent |
|---|---|---|
| Visual count-in only | Huge digits + flash, no Start/Stop/Record controls | Jeff’s phone on music stand while hands on guitar |
| “ROLLING / STOPPED / REHEARSE” status mirror | Read-only projection from host | Band / Jeff peripheral vision |
| Lyric / section teleprompter | Synced to WebJam bar clock | Pocket Stage adjacent |
| VoiceOver on phone status | Blind/low-vision friendly cues | Accessibility |
| Haptic tick optional | Light taps on beat during count-in only | Feel without audio click bleed |
| Guest delay vote button | “I hear echo” → host mute | Social fail-safe |
| Explicit non-goals on phone | No MMC/MCU send, no Logic Remote clone | Stay parked |

### 5.7 More outside-the-box (still practical)

- **Feel-yes gate UI:** before MATCH of polish stacks, a one-screen “play 30 s — feel OK?” with recording of Jeff’s verdict.  
- **Echo forensics pack:** one button dumps last 60 s of mute SM transitions + MCU notes (privacy-redacted) when Jeff reports bleed.  
- **RefBed discipline:** auto-place session bed into Logic as muted reference track via handoff naming — never live dual play.  
- **Pre-roll brain:** WebJam shows Logic count-in length if known; otherwise assumes 1 bar and mutes early.  
- **Session “clean take score”:** post-take: mute violations = 0, SR match = ok, dual-play = fail → green/yellow/red.  
- **Template drift check:** warn if Logic project SR ≠ last handoff SR.  
- **No-hero mode:** if MCU unhealthy, big Manual Mute still one click — excellence includes graceful degradation.

---

## 6. Prioritized backlog (P0–P3)

### P0 — Without these, not excellent (ship blockers for “quality product”)

| ID | Item | Why |
|---|---|---|
| P0-1 | LogicHandoff export pack (WAV/AIFF 24-bit, MIDI, tempo.json, README) | File-first; works offline; matches Jeff’s DAW habit |
| P0-2 | Rehearse \| Record mode UI + fail-closed local mute | Stops the #1 echo class (Gemini) |
| P0-3 | MCU feedback Record/Stop/Play → mute state machine | Auto mute must survive Record pressed *inside* Logic |
| P0-4 | Split mute: local speakers vs Jamulus remote (default remote ON) | Band still hears cues; capture stays clean |
| P0-5 | Mute hold after Stop; never auto-unmute in Record mode | Prevents buffer-tail bleed |
| P0-6 | BUILD GATE + #149 / feel-yes discipline | Prevents shipping fragile while CI red / unfelt MATCH |

### P1 — Makes it feel pro

| ID | Item | Why |
|---|---|---|
| P1-1 | Clean-take checklist (IAC, MCU ping, SR, monitor exclusive, BH off) | Prevents expert-only failure modes |
| P1-2 | IAC/Mackie setup wizard + port ping | Removes one-time fear |
| P1-3 | MCU map calibration → saved profile per Logic version | Survives version quirks |
| P1-4 | Visual count-in / bar flash (desktop) | Remote band excellence |
| P1-5 | WebJam Tracking `.logicx` template + naming contract | Drag-drop becomes instant |
| P1-6 | Logic version/path detect in status UI | Debuggability |
| P1-7 | Accessibility: VO labels, large count-in, no color-only | Excellence includes everyone |
| P1-8 | Mid-take conflict banners + take shield | Outside-the-box reliability |

### P2 — Strong differentiators

| ID | Item | Why |
|---|---|---|
| P2-1 | Ableton Link tempo peer | Shared BPM without claiming Record detect |
| P2-2 | Reverse stem watch folder (Logic → WebJam play-along) | Bidirectional rehearsal |
| P2-3 | Phone **visual-only** companion (count-in, ROLLING) | Parked transport, useful eyes |
| P2-4 | Latency badge + loopback measure (CAPTURE ONLY labeling) | Honest engineering |
| P2-5 | Offline/reconnect re-assert + wake MIDI refresh | Real Mac Mini life |
| P2-6 | Post-take listen digest export | Band review without friction |
| P2-7 | Echo forensics pack | Support without guesswork |
| P2-8 | Guest “I hear delay” vote | Social fail-safe |

### P3 — Later / optional / easy to get wrong

| ID | Item | Why later |
|---|---|---|
| P3-1 | BlackHole live print-in + Aggregate fingerprint | Phase 3; latency & mis-clock landmines |
| P3-2 | Auto-arm safe DI tracks via MCU channels | Wrong bank = wrong track |
| P3-3 | Punch/cycle region mirror to guests | Fragile MCU surface state |
| P3-4 | Deep AX/MCP track mutation from WebJam | Wrong product shape; Bob/MCP separate |
| P3-5 | Phone transport remote | **PARKED** |
| P3-6 | Logic Remote protocol | **Forbidden** |

---

## 7. Testing plan PER enhancement

Convention: each test lists **acceptance criteria**, **how to test**, **what “feels solid” means**, **evidence required**. No enhancement merges without evidence Jeff accepts.

### T-P0-1 LogicHandoff pack

- **AC:** Pack contains audio + MIDI + tempo/README; SR documented; drag into Logic yields aligned lengths.  
- **How:** Export after a 30 s session stub; import on clean project; play.  
- **Feels solid:** Jeff doesn’t rename files or hunt folders; “this is the take” in &lt;60 s.  
- **Evidence:** Folder listing screenshot + Logic arrange screenshot + `tempo.json` contents.

### T-P0-2/3/4/5 Mute state machine + MCU

- **AC (Gemini):** WebJam playing → arm Logic track → Record → **local audio ceases immediately**; Stop + Rehearse → returns; Jamulus remote still configurable ON.  
- **How:** MIDI Monitor confirms Record note; physical speakers / interface out observed; remote guest confirms still hearing network path if policy ON.  
- **Feels solid:** No ghost bed on waveform; no “I forgot to mute” stories; mute before downbeat.  
- **Evidence:** Screen recording of UI mode + waveform zoom of take start; MIDI Monitor log; mute SM log.

### T-P0-6 Build gate

- **AC:** No Logic companion PR opened while #149 red / lease blocked; no MATCH without feel yes note.  
- **How:** Process check against board.  
- **Feels solid:** Jeff never surprised by drive-by Logic code.  
- **Evidence:** PR links / non-existence recorded in status note.

### T-P1-1 Clean-take checklist

- **AC:** Record mode blocked (or warning+ACK) if IAC missing, MCU ping fail, SR mismatch, BH unexpectedly on, dual monitor.  
- **How:** Break each precondition deliberately; confirm checklist catches it.  
- **Feels solid:** Jeff trusts the green check like a pilot checklist.  
- **Evidence:** Screenshots per failure injection.

### T-P1-2 Setup wizard

- **AC:** From cold Mac settings, wizard creates/verifies three IAC ports + explains Mackie install; ping passes.  
- **How:** Disable IAC; run wizard; complete Logic surface add; ping.  
- **Feels solid:** Non-MIDI-expert can finish in one sitting.  
- **Evidence:** Before/after Audio MIDI Setup + Logic Control Surfaces screenshots.

### T-P1-3 MCU calibration

- **AC:** Captured map survives relaunch; wrong map fails closed (stay muted in Record).  
- **How:** Calibrate; relaunch; Record; corrupt map file and confirm safe mute.  
- **Feels solid:** “It just knows my Logic.”  
- **Evidence:** `logic-mcu-map.json` + MIDI Monitor capture.

### T-P1-4 Visual count-in

- **AC:** Guests see synchronized bar/beat flash for configured count-in; reduced-motion alt works.  
- **How:** Two machines; start count-in; film both screens.  
- **Feels solid:** Band hits together without audio click on capture bus.  
- **Evidence:** Side-by-side video.

### T-P1-5 Template project

- **AC:** Handoff names match template tracks; SR matches README; markers optional.  
- **How:** Open template; import pack; play.  
- **Feels solid:** Zero track creation busywork.  
- **Evidence:** Arrange screenshot with named tracks.

### T-P1-6 Version detect

- **AC:** UI shows correct Logic version or “Logic not found”; unknown version prompts calibrate.  
- **How:** With Logic closed/open; spoof unknown version string in test harness if available.  
- **Feels solid:** Status line trusted when debugging.  
- **Evidence:** Status UI screenshots.

### T-P1-7 Accessibility

- **AC:** VO announces mode/mute; count-in readable at large text; color not sole indicator.  
- **How:** VoiceOver walkthrough; large text screenshot.  
- **Feels solid:** Usable without sighted helper for mode awareness.  
- **Evidence:** VO recording or annotated screenshots.

### T-P1-8 Mid-take conflict

- **AC:** Attempted unmute / mode flip during Record LED on is blocked or confirmed; ledger entry written.  
- **How:** Record; try Rehearse; confirm dialog/block; Stop; then Rehearse works.  
- **Feels solid:** Impossible to accidentally blast speakers mid-take.  
- **Evidence:** Screen recording + ledger snippet.

### T-P2-1 Ableton Link

- **AC:** Tempo/phase align within Link tolerance; Record mute still MCU-driven (Link start ≠ Record).  
- **How:** Enable Link both sides; change BPM; verify; press Record only in Logic UI.  
- **Feels solid:** Click agrees; mute still correct.  
- **Evidence:** BPM screenshots + mute log during Link play.

### T-P2-2 Reverse stems

- **AC:** Drop Logic bounce into watch folder → appears in WebJam play-along.  
- **How:** Bounce; wait; play in WebJam.  
- **Feels solid:** No manual re-encode.  
- **Evidence:** Finder + WebJam UI screenshots.

### T-P2-3 Phone visual-only

- **AC:** Phone shows count-in/ROLLING; **no** transport controls send MIDI; killing phone app doesn’t Stop Logic.  
- **How:** Use phone during take; verify no MMC/MCU from phone path.  
- **Feels solid:** Eyes on stand, hands free, zero control risk.  
- **Evidence:** Phone video + MIDI Monitor showing no extra transport from phone.

### T-P2-4 Latency badge

- **AC:** Measured RTL shown; paths &gt; threshold marked CAPTURE ONLY.  
- **How:** Loopback measure vs known buffer; compare badge.  
- **Feels solid:** Jeff believes the number.  
- **Evidence:** Measurement WAV + badge screenshot.

### T-P2-5 Reconnect / wake

- **AC:** After sleep or IAC blip in Record mode, local stays muted; health recovers.  
- **How:** Sleep 1 min mid-ARMED; wake; verify mute + ports.  
- **Feels solid:** No surprise blast after lid open.  
- **Evidence:** Log with timestamps (CT).

### T-P2-6 Listen digest

- **AC:** One action produces shareable rough mix link/file.  
- **How:** After take; run digest; open on second device.  
- **Feels solid:** Band hears take tonight, not next week.  
- **Evidence:** Share link + file.

### T-P2-7 Forensics pack

- **AC:** Pack contains mute SM + MCU summary, no secrets.  
- **How:** Trigger echo report; inspect pack.  
- **Feels solid:** Debug without recreating from memory.  
- **Evidence:** Redacted pack sample.

### T-P2-8 Guest delay vote

- **AC:** Guest tap forces host local mute + banner.  
- **How:** Simulate guest vote during REHEARSE with speakers on.  
- **Feels solid:** Band can save a take socially.  
- **Evidence:** UI recording both sides.

### T-P3-1 BlackHole (only if Jeff still wants)

- **AC (MiniMax-aligned):** Aggregate clock = interface; BH secondary + drift; room not double-feeding; 30 s record with WebJam muted = clean waveform; unmute mapping doesn’t howl.  
- **How:** Full Aggregate recipe; deliberate mis-clock test must fail preflight.  
- **Feels solid:** Print-in without ticks/echo; badge says CAPTURE ONLY.  
- **Evidence:** AMS Aggregate screenshot, waveform, RTL badge, rollback note if failed.

### Regression battery (every Phase 2+ build)

1. REHEARSE speakers audible.  
2. RECORD mutes before audible downbeat.  
3. Stop alone does not unmute.  
4. Rehearse after Stop unmutes after hold.  
5. Handoff pack still imports.  
6. MCU unplugged → fail-closed in Record mode.  

---

## 8. Explicit BUILD GATE (restated)

```
NO IMPLEMENTATION until:
  [ ] Jeff reviews this excellence research doc
  [ ] Jeff selects P0/P1 items in / out / defer
  [ ] Each selected item has Section 7 evidence Jeff accepts
  [ ] Jeff says quality product OK (per slice or whole Phase)
  [ ] #149 CI / lease constraints respected
  [ ] No MATCH without feel yes
  [ ] Phone transport remains PARKED
  [ ] No Logic Remote reverse engineering
  [ ] Phase order: file-first → MCU mute → optional BlackHole
```

**Planning:** highest-tier reasoning.  
**Implementation (later):** cheaper models OK only against locked acceptance tests above.

---

## Appendix A — Mute state machine (canonical)

States: `REHEARSE` → `ARMED` → `COUNT_IN` → `RECORDING` → `PLAYBACK_REVIEW`

- Mute local program when `mode==Record` OR transport in {count-in, recording} OR MCU Record LED on.  
- Unmute only in `REHEARSE` after Stop + unmute delay.  
- Jamulus remote path independent flag (default ON).  
- Log every transition.

## Appendix B — Mac setup checklist (Jeff)

1. Audio MIDI Setup → IAC online; ports: `WebJam MCU Cmd`, `WebJam MCU Fb`, `WebJam Notes`  
2. Logic → Control Surfaces → Mackie Control (Cmd in / Fb out)  
3. Filter MCU IAC from track MIDI inputs  
4. Enable Listen to MMC Input  
5. MIDI Monitor: verify Record/Stop/Play LED notes; save calibration  
6. (Ph3 only) Aggregate: interface clock master; BlackHole drift correction; no BT clock  

Community MCU map to verify (ch1 note-on vel 127/0): Play≈94, Stop≈93, Record≈95 — **not gospel until calibrated on Jeff’s Logic**.

## Appendix C — Sources & prior art

- Prior: `/workspace/research/webjam-logic-pro-companion-20260922.md`, `webjam-logic-companion-BUILD-BRIEF.md`, critiques Gemini/MiniMax  
- Prior: `/workspace/logic-integration-research-aug22.md` (file handoff forever-primary)  
- Apple: Logic monitoring latency, metronome/count-in, control surfaces, IAC, Ableton Link, OSC paths  
- BlackHole Aggregate wiki; Apple Community drift correction guidance  
- MCU maps: EMATech/TouchMCU docs; rubenknol/logic-pro-mcp IAC MCU Cmd/Fb pattern  
- Latency perception literature: ~&lt;10 ms comfortable tracking; &gt;20 ms poor for feel; direct vs software monitor exclusivity  

---

*End of excellence research. Wait for Jeff review before any product code.*
