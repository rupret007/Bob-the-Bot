# WebJam ↔ Logic Pro companion research (2026-09-22 CT)
Research-only. No code or PRs. Jeff’s Mac + Logic Pro primary DAW.

Note: WebJam today is a **desktop Qt/PySide6** collab app (Jamulus, Studio, Art Paint along), not a pure browser SPA. That helps: native CoreMIDI/CoreAudio is available without WebMIDI sandbox limits. Browser-only guests would still need a local helper.

## Bottom line (simplest path that works)

**Do not chase a deep official “Logic plugin API” for remote arrangement control — it does not exist publicly.**

**Phase 1 (ship first): Logic-ready handoff**
- WebJam exports stems/MIDI/charts as WAV/AIFF/MIDI to a watched folder or drag-drop into Logic.
- Optional AppleScript/Shortcuts only to *open* Logic or a template — not for deep project mutation.
- Matches Jeff’s existing preference for Logic-ready files.

**Phase 2: Local MIDI companion bridge**
- WebJam (or a tiny Mac helper) ↔ **IAC Driver** buses ↔ Logic.
- Transport: **MMC** (“Listen to MMC Input”) and/or emulate **Mackie Control (MCU)** over dedicated IAC ports.
- Notes/CC: stream to instrument tracks via IAC; MIDI Learn / controller assignments for UI binds.
- Optional tempo/beat sync: **Ableton Link** (official in Logic) if WebJam joins Link; no audio routing via Link.

**Phase 3 (optional live audio): Virtual audio**
- **BlackHole** (or Loopback) + Aggregate Device so WebJam/Jamulus monitor can feed Logic inputs.
- Expect latency tradeoffs; not for “zero-latency band feel” unless carefully engineered.

**Avoid first:** reverse-engineering Logic Remote / Multipeer Connectivity; NDA Control Surface Plug-in SDK unless Apple grants it; treating WebMIDI-in-Chrome as the Mac-side spine (WebJam already has native desktop).

---

## 1) Official APIs / protocols Logic exposes

### What exists (documented)

| Channel | What it is | Useful for WebJam? |
|---|---|---|
| **MIDI (CoreMIDI) + IAC Driver** | macOS inter-app MIDI buses | **Yes — primary integration spine** |
| **MMC (MIDI Machine Control)** | Play/Stop/Record etc. | **Yes — transport** (enable Listen to MMC) |
| **MIDI Clock / MTC** | Tempo/time sync | Possible; Link often cleaner for tempo peers |
| **Ableton Link** | Official in Logic Pro for Mac — shared beat/phase/tempo on LAN | **Yes — tempo sync with jam session** (no audio) |
| **Control surfaces: MDP / MDS (Lua)** | Built-in MIDI Device Plug-ins + Lua MIDI Device Scripts; auto-assign USB controllers | **Yes — emulate MCU/HUI-like surface over IAC** |
| **Controller Assignments / MIDI Learn** | Map CCs to Logic functions | Yes for custom mappings |
| **Scripter (JavaScript MIDI FX)** | In-track MIDI processing API | Logic-side only; not an external remote API |
| **AU / AUv3** | Host plugins *inside* Logic | WebJam-as-AU is wrong product shape; Logic hosts AUs |
| **External Instrument / I/O utility** | Route to/from other apps/hardware | Useful for audio/MIDI device routing inside Logic |
| **Import/Export** | Standard MIDI files, audio export/bounce, AAF, FCP XML, MusicXML | **Yes — Phase 1** |
| **Logic Remote (iPad/iPhone)** | Official Apple companion app | **No public API** for third parties |

Sources:
- https://support.apple.com/guide/logicpro/ctls718dd5b2/mac (control surfaces MDP/MDS)
- https://help.apple.com/pdf/logicpromac-css/en_US/logic-pro-mac-control-surfaces-support-guide.pdf
- https://support.apple.com/guide/logicpro/ctlsbfee6d57/mac (Lua auto-assign USB controllers)
- https://support.apple.com/guide/logicpro/ableton-link-in-logic-pro-for-mac-lgcp528602e4/mac
- https://support.apple.com/guide/logicpro/use-the-javascript-midi-object-lgcebee22a60/mac (Scripter)

### What does *not* exist publicly

- **No public general-purpose Control Surface Plug-in SDK** without Apple NDA / TSI request (Developer Forums: SDK under NDA).
- **No rich AppleScript dictionary** for tracks/regions/mix the way many Mac apps expose. Forums consistently report Logic as poorly scriptable; UI scripting is fragile.
- **Logic Remote protocol is not a documented integration API.** Connectivity uses Apple Multipeer Connectivity (undocumented). Reverse-engineering exists for MPC generally (e.g. evilsocket/mpcfw research) but building a product on RE’d Logic Remote is brittle and high risk.
- **ReWire** is obsolete / not a modern Logic integration path.
- **No public “open this Arrange page and mutate regions” HTTP/SDK.**

Apple Developer Forums (control surface SDK NDA): https://developer.apple.com/forums/thread/25976

---

## 2) Third-party bridges / OSS

| Project / tech | Role |
|---|---|
| **IAC Driver** (Audio MIDI Setup) | Built-in Mac virtual MIDI buses between apps |
| **rtmidi / python-rtmidi / node-midi** | Cross-platform MIDI I/O libraries for a helper |
| **WebMIDI / webmidi.js** | Browser MIDI to *existing* ports — cannot create system virtual ports |
| **WebMIDIKit** (Swift CoreMIDI wrapper) | Native macOS MIDI incl. virtual ports |
| **JSMidi** (aaronats/jsmidi) | WebMIDI live-coding → DAW; tested historically with Logic via IAC |
| **logic-pro-mcp** (rubenknol/logic-pro-mcp) | Practical modern stack: MCU over IAC + MMC + SMF round-trip; explicitly documents Logic’s lack of AppleScript/project SDK |
| **LinkPulse** (EranGrin/linkpulse) | Ableton Link → MIDI Clock CoreMIDI bridge |
| **BlackHole** / **Loopback** | Virtual audio devices for app→Logic audio |
| **TouchOSC / Lemur / Companion** | OSC/MIDI controller surfaces; Logic mainly wants MIDI (OSC paths exist in Controller Assignments Expert view for some setups) |
| **MIDI Monitor / ShowMIDI** | Debug tools |

logic-pro-mcp README framing (useful architecture proof): Mackie Control over IAC for background transport/mixer; MMC fallback; SMF + IAC for region note data — https://github.com/rubenknol/logic-pro-mcp

WebMIDI cannot create virtual devices (djipco/webmidi discussion #402).

---

## 3) Realistic WebJam architecture

```
[Band members] --Jamulus/Webex--> [WebJam host Mac]
                                      |
                    +-----------------+------------------+
                    |                                    |
             WebJam UI/session                    Logic Pro
             (jam, play-along, Art)                      |
                    |                                    |
                    v                                    v
            Companion helper (optional)  <----IAC MIDI---->
            CoreMIDI + optional Link         MMC / MCU / notes
                    |
                    +----BlackHole/Aggregate----> Logic audio ins
                    |
                    +----folder watch WAV/MIDI----> Logic import
```

Flows:
- **(a) Transport sync:** WebJam play/stop → helper sends MMC and/or MCU; optional Ableton Link for shared tempo with jam tools.
- **(b) MIDI send:** WebJam MIDI from Pocket Stage / arrangement → IAC → Logic software instrument tracks.
- **(c) Stem/MIDI import:** Bounce/export from WebJam Reference Studio → `~/Music/WebJam/LogicInbox/` → user (or helper) imports; gold standard reliability.
- **(d) Live audio into Logic:** WebJam/Jamulus output → BlackHole → Aggregate Device → Logic audio tracks (monitoring latency).
- **(e) Play-along video vs Logic playhead:** Keep video clock in WebJam; drive Logic via Link/MMC rather than trying to slave YouTube to Logic’s playhead pixel-perfect. Two clocks with Link/tempo is honest; frame-accurate video↔DAW needs LTC/MTC and is a later phase.

Because WebJam is already native desktop, prefer **in-process CoreMIDI** or a small helper app over “browser WebSocket → WebMIDI”.

---

## 4) Feasibility, limits, gotchas

- **Logic is the least scriptable major DAW** for deep project mutation — plan around MIDI + files, not AppleScript object graphs.
- **Control Surface Plug-in SDK is NDA** — Lua MDS or MCU-over-IAC is the open path.
- **Apple silicon:** third-party MDP plug-ins limited; prefer Lua MDS / MIDI protocols.
- **Latency:** live virtual audio into Logic is never as tight as Jamulus’s own path; use for capture/overdub, not as the band’s primary feel bus.
- **Sample rate / buffer:** Aggregate Device clock source must be the interface; BlackHole drift correction needed.
- **Permissions:** Automation (if UI scripting), Microphone, Local Network (for Link), Accessibility.
- **Multi-user:** Only the host Mac runs Logic; guests stay in WebJam/Jamulus. Logic is single-operator companion, not shared DAW.
- **Logic Remote RE:** research curiosity only — do not productize.
- **Sandbox:** if WebJam ever ships Mac App Store, CoreMIDI/virtual audio entitlements get harder; current GitHub desktop distribution is freer.

---

## 5) Recommendation (phased)

1. **Now:** Phase 1 Logic-ready export pack (stems + MIDI + tempo/map notes) — already aligned with Jeff’s DAW preference. Zero fragile APIs.
2. **Next:** Phase 2 companion bridge — IAC buses named `WebJam MCU` / `WebJam Notes`; MMC listen + Mackie Control install in Logic; optional Ableton Link peer in WebJam for tempo.
3. **Later:** Phase 3 BlackHole capture path for “record the jam into Logic.”
4. **Skip for now:** Logic Remote protocol, NDA MDP SDK, browser-only WebMIDI as the Mac host spine, deep AppleScript track editing.

Success metric: “After a WebJam rehearsal, Jeff has Logic tracks populated with MIDI/stems and can press play in sync” — not “WebJam is a remote Arrange editor.”

---

## Sources (primary)

- Apple: Control surfaces supported — https://support.apple.com/guide/logicpro/ctls718dd5b2/mac
- Apple: Control Surfaces Support Guide PDF — https://help.apple.com/pdf/logicpromac-css/en_US/logic-pro-mac-control-surfaces-support-guide.pdf
- Apple: USB MIDI Lua auto-assignment — https://support.apple.com/guide/logicpro/ctlsbfee6d57/mac
- Apple: Ableton Link in Logic — https://support.apple.com/guide/logicpro/ableton-link-in-logic-pro-for-mac-lgcp528602e4/mac
- Apple: Scripter JS MIDI — https://support.apple.com/guide/logicpro/use-the-javascript-midi-object-lgcebee22a60/mac
- Apple Dev Forums: Control Surface SDK under NDA — https://developer.apple.com/forums/thread/25976
- Ableton Link FAQ — https://help.ableton.com/hc/en-us/articles/209776125-Link-features-and-functions-FAQ
- rubenknol/logic-pro-mcp — https://github.com/rubenknol/logic-pro-mcp
- djipco/webmidi discussion (no virtual ports) — https://github.com/djipco/webmidi/discussions/402
- WebMIDIKit — https://github.com/adamnemecek/WebMIDIKit/
- JSMidi — https://github.com/aaronats/jsmidi
- LinkPulse — https://github.com/EranGrin/linkpulse
- BlackHole browser→Logic routing discussion — https://gearspace.com/threads/audio-routing-blackhole-browser-to-logic-pro.1381541/
- Multipeer Connectivity RE (Logic Remote transport layer context) — https://www.evilsocket.net/2022/10/20/Reverse-Engineering-the-Apple-MultiPeer-Connectivity-Framework/

---

## 6) Audio routing & mute logic (WebJam ↔ Logic)

Jeff’s lived problem: virtual-audio / shared-monitor paths add delay. If WebJam keeps playing the same program into speakers (or into a path that re-enters Logic) while Logic is recording, you get echo, feedback, or a dirty take with delayed WebJam bleed.

### Design principle
Separate three buses conceptually:

1. **Band feel bus** — Jamulus / WebJam low-latency monitor for players (primary while rehearsing remotely).
2. **Logic capture bus** — dry mics / DI / instrument inputs into Logic (what gets recorded).
3. **Logic monitor bus** — Logic’s software monitoring / headphone mix (what the host hears while tracking).

Rule: **never let delayed WebJam program material share the Logic capture bus.** Mute or divert WebJam’s *local speaker/program out* when Logic is in a take that could record that path.

### When WebJam should mute its own playback audio

Mute WebJam **local program / speaker / BlackHole-bound output** when any of:

| Condition | Why |
|---|---|
| Logic **Record** engaged (transport recording) | Prevent delayed WebJam → speakers → mic → Logic, or WebJam → BlackHole → Logic if that path is live |
| Logic **count-in** or pre-roll before record | Same bleed risk during bars before punch |
| Mode = **Record take** / **Overdub** (even if user hasn’t hit Record yet but WebJam is feeding BlackHole) | Fail-closed: treat “armed record session” as mute-program |
| Host enables **Input monitoring** on tracks that can hear room mics while WebJam is audible in the room | Room-mic feedback |

What *not* to mute blindly:
- **Jamulus send to remote bandmates** can stay up if they are *not* feeding Logic’s inputs (separate path). Mute is about **local delayed program into the capture chain**, not necessarily killing the whole session for guests.
- Prefer muting **WebJam → room / BlackHole program**, not killing MIDI click that Logic itself generates.

### When WebJam should unmute

Unmute local program when:

| Condition | Why |
|---|---|
| Logic **Stop** (not recording) and mode = **Rehearse / Play-along** | Band wants WebJam click, backing, Paint-along audio again |
| Logic **Play** only (playback review) *and* capture path cannot hear speakers | Safe if no open mics into Logic; still careful with room mics |
| Mode switch to **Rehearse** explicitly | User intent overrides auto if they accept risk |
| After take: short **hold mute 200–500 ms** past Stop | Avoid tail of delayed buffer spilling into next action |

### How the bridge detects Logic record / play / stop

Best → worst for automation:

1. **Mackie Control feedback MIDI (recommended)**  
   Install Logic Mackie Control with IAC `MCU Cmd` → Logic and `MCU Fb` ← Logic. Logic sends transport LED / status on the feedback port (Play, Stop, Record illuminate). Bridge listens on `MCU Fb` and maps Record LED / transport bytes → mute state. Proven pattern in control-surface and logic-pro-mcp setups. Filter MCU buses out of Logic track MIDI inputs to avoid MIDI feedback freezes.

2. **Command-side inference (weaker)**  
   If WebJam/bridge *sent* the Record MMC/MCU command, enter MUTE_PROGRAM immediately; unmute on Stop command. Misses Record presses done only inside Logic UI unless feedback (1) is present.

3. **Ableton Link start/stop**  
   Syncs play/stop among Link peers; **does not reliably equal “Logic is recording.”** Use for tempo/play-along, not as sole record detector.

4. **MMC listen alone**  
   Good for commanding Logic; Logic does not give a rich public “I am recording” AppleScript. Prefer MCU feedback.

5. **Manual / mode switch fallback (required)**  
   Big **Rehearse | Record** toggle in WebJam. Manual always wins for fail-safe. Auto mute can engage under Record mode even before transport moves.

6. **Do not rely on** Logic Remote Multipeer RE or AppleScript transport polling as the primary detector.

### Other routing concerns

- **Monitoring:** Host should monitor through Logic (or interface mixer) during Record mode; WebJam local speakers off or very low.
- **Click track:** Prefer Logic’s metronome into headphones during Record; if WebJam click stays for remote players, keep it **network-only** (Jamulus), not into BlackHole/room.
- **Backing track bleed:** Export backing into Logic as a muted/ref track, or play backing only from Logic during Record mode. Avoid dual playback (WebJam + Logic) of the same bed.
- **Latency compensation:** DAW PDC compensates plug-in delay inside Logic, **not** round-trip virtual-audio delay from WebJam. Don’t expect WebJam mute timing to sample-align with Logic without measuring buffer. Practical approach: mute early (on count-in), unmute late (after Stop + margin).
- **Aggregate Device:** Clock from hardware interface; BlackHole as secondary with drift correction.
- **MIDI feedback loops:** Filter IAC MCU ports from sequencer inputs (Logic MIDI settings).

### Recommended mute state machine

States: `REHEARSE`, `ARMED`, `COUNT_IN`, `RECORDING`, `PLAYBACK_REVIEW`.

```
REHEARSE:
  WebJam local program = ON (feel bus)
  Jamulus = ON
  BlackHole feed from WebJam = OFF (default)
  on user→Record mode → ARMED

ARMED:
  WebJam local program = MUTE (fail-closed)
  BlackHole feed = OFF unless explicit “route stems to Logic”
  show “Logic record mode — WebJam speakers muted”
  on MCU/MMC Record or count-in → COUNT_IN / RECORDING
  on user→Rehearse → REHEARSE

COUNT_IN:
  same mutes as RECORDING
  on Record engage → RECORDING
  on Stop → ARMED or REHEARSE (policy: return ARMED)

RECORDING:
  WebJam local program = MUTE
  room/BlackHole program = MUTE
  remote Jamulus may stay ON for band (optional policy flag)
  Logic click/headphones = ON
  on Stop → PLAYBACK_REVIEW (keep mute briefly) then ARMED or REHEARSE

PLAYBACK_REVIEW:
  mute hold timer then:
    if still Record mode → ARMED (program stays muted)
    if Rehearse → REHEARSE (unmute)
```

**Developer ruleset (short):**
1. Mute WebJam local program whenever `mode==Record` OR transport in {count-in, recording}.
2. Drive transport from MCU feedback; fall back to last command we sent; always allow manual Rehearse/Record.
3. Never auto-unmute while `mode==Record`.
4. Unmute only in `REHEARSE` after Stop + unmute delay.
5. Keep Jamulus remote path configurable separately from local speaker mute.
6. Log state transitions for debugging echo reports.

Sources for detection/routing: Apple Mackie Control transport docs; Logic control surfaces guide; IAC MCU Cmd/Fb pattern (logic-pro-mcp); Ableton Link docs (tempo ≠ record).

---

## 7) Experience enhancements (beyond API + mute)

Creative but practical ideas for a compelling WebJam + Logic companion. Feasibility: **Easy / Medium / Hard**.

| Enhancement | What it is | Feasibility | Notes |
|---|---|---|---|
| **Rehearse vs Record mode** | One-click mode switch driving mute state machine + UI chrome | **Easy** | Highest leverage; ship with Phase 1/2 |
| **Shared session link** | Invite URL opens WebJam room; host flag “Logic companion armed” | **Easy–Medium** | Auto-connect guests to Jamulus/WebJam; Logic stays host-only |
| **Auto tempo sync** | Ableton Link between WebJam and Logic | **Medium** | Official in Logic; WebJam must implement Link peer |
| **Visual click / cue strip** | On-screen bar flash, “come in at bar 5”, count-in lights for remote players | **Medium** | Driven by WebJam clock or Link beat; huge for remote bands |
| **Phone as controller** | Start/Stop/Record Logic from phone across room | **Medium** | WebJam mobile/Pocket Stage → host bridge → MCU/MMC; better than RE Logic Remote |
| **Take markers / chat cues** | “Rolling”, “again from chorus”, pinned lyric line during take | **Easy–Medium** | Fits existing band Messages ops + in-room chat |
| **Stem export Logic → WebJam play-along** | Bounce stems from Logic, drop into WebJam Reference / Paint-along style play-along | **Medium** | Folder watch or drag-drop; reverse of Phase 1 |
| **Stem export WebJam → Logic** | After jam, pack multitrack for Logic arrange | **Easy** | Already recommended Phase 1 |
| **Host “clean take” checklist** | Preflight: mute WebJam speakers, check Aggregate, armed tracks, sample rate | **Easy** | Prevents Jeff’s echo class of bugs |
| **Latency badge** | Show estimated WebJam↔Logic audio delay when BlackHole path enabled | **Medium** | Measure round-trip; warn if > X ms |
| **Dual mute policy** | Toggle “mute local only” vs “mute local + pause Jamulus bed” | **Easy** | Different for overdub vs full-band track |
| **Section teleprompter** | Shared set-list / arrangement markers synced to bars | **Medium** | Ties to Pocket Stage / stage lyrics skill |
| **Auto-arm safe tracks** | Bridge arms only DI tracks, never ambient room bed | **Hard** | Needs MCU channel feedback + careful mapping |
| **Punch / cycle sync** | WebJam shows Logic cycle region to guests | **Hard** | MCU can expose some modes; fragile |
| **Paint-along + Logic** | Art users follow video while host tracks audio in Logic | **Medium** | Keep video clock in WebJam; Link for tempo only |
| **Post-take “send listen link”** | Bounce rough mix → Drive/Samply → band digest | **Easy** | Matches current Stalemate mixer digest workflow |
| **Controller surface presets** | Saved IAC + Mackie install recipe for Jeff’s Mac Mini | **Easy** | Docs + one-click helper validation |
| **Guest “I hear delay” vote** | Guests flag echo; host UI forces mute | **Easy** | Social fail-safe |

### Highest-ROI bundle for Jeff
1. Rehearse/Record mode + mute state machine  
2. Session link + visual count-in cues  
3. Ableton Link tempo  
4. Bidirectional stem folder (WebJam ↔ Logic)  
5. Phone transport controller via existing WebJam mobile path  
6. Post-take band listen digest  

Skip early: full remote Arrange editing, Logic Remote protocol clone, auto-arming every track.


---

## Addendum (deeper research pass ~10:29 PM CT)

### MCU transport LED notes (community Mackie map — verify with MIDI Monitor)
Logic → IAC MCU Feedback typically uses channel 1 note-on velocity 127 = on, 0 = off:
- Play ≈ note 94
- Stop ≈ note 93
- Record ≈ note 95
- Rec-arm per channel ≈ notes 0–7

Use these as the primary automatic mute triggers. Treat maps as community truth until confirmed on Jeff’s Logic build.

### Official OSC path (additional)
Logic Controller Assignments support OSC message paths (UDP/IPv4). TouchOSC uses Zeroconf names like LogicPad/LogicTouch. Useful for phone/tablet surfaces; still not a full arrangement API.
- https://support.apple.com/guide/logicpro/osc-message-paths-ctlsf67f4bdc/mac
- https://hexler.net/touchosc/manual/setup-logic

### Extra primary sources
- Mackie Control overview: https://support.apple.com/guide/logicpro-css/mackie-control-overview-ctls7222820e/mac
- IAC Driver: https://support.apple.com/guide/audio-midi-setup/transfer-midi-information-between-apps-ams1013/mac
- Network MIDI: https://support.apple.com/guide/audio-midi-setup/share-midi-information-over-a-network-ams1012/mac
- Bounce / export tracks: Apple Logic User Guide bounce + export-tracks pages
- BlackHole: https://github.com/ExistentialAudio/BlackHole
- Ableton Link SDK: https://github.com/Ableton/link
- MCU protocol community docs: https://github.com/EMATech/TouchMCU/blob/main/doc/mackie_control_protocol.md

### Architecture note
Prefer a small `webjam-logic-bridge` helper (CoreMIDI + optional MCU) talking to WebJam over localhost WebSocket/IPC, rather than Web MIDI inside Qt WebEngine.
