# MiniMax excellence (trimmed CoT)

> **Partial capture.** Trimmed chain-of-thought, not a finished memo. The body starts mid-word. Numbering skips. The synthesis adopted only items it names. Do not backfill missing bullets.

ording in Logic). The companion never relies on network for audio. WebJam is a control plane, not a media plane. Stems upload after. If WebJam dies, the take survives.

4. **Safe-Take Recovery Sentinel**: A lightweight Logic AUv3 plug-in that pings CoreHeart's transport state over localhost OSC. If the plug-in detects Logic freeze or plug-in silence for N seconds, it auto-saves a "last good" take marker and broadcasts a "Logic is dying" warning to other session members so they can pause.

5. **Universal A11y Layer**: Full keyboard transport (R/J/B = record/play/stop, Space = punch in), screen-reader announcements ("Take 7 starting, count-in 4 beats"), high-contrast stage mode (huge meters, white-on-black), reduced-motion preference honored. Captions on the visual count-in describing tempo/feel.

6. **Tablet-First Touch Mixer with Pencil Annotations**: iPad/Surface as a real control surface — touch faders for monitor mix return to each musician, large record-arm buttons, Apple Pencil to scribble bar annotations ("fix this bar", "vamp from here") that surface in everyone's UI.

7. **Per-User Latency Budget UI**: Show every musician's round-trip transport latency live (e.g., "Your stop arrived at Sam's Logic in 38 ms; Sam's stop arrived at yours in 41 ms"). One-time calibration ritual where each musician taps a click at beat 1; the system computes offset and bakes it into the session.

8. **BWF/iXML Time-Anchored Exports**: Embed BWF timestamps and iXML chunks in every WAV export, derived from the shared session clock. Drop the WebJam export folder into Logic and the tracks auto-position on the timeline — no manual nudge. Sample-accurate.

Now the **Top 5 failure modes that would make the product feel cheap**:

I want these to be things that would make a musician say "this is a toy, not a tool":

1. **Transport latency > 80 ms one-way** — when you hit stop and it visibly doesn't stop, or stop arrives at a different beat than the click played. This is the single biggest "pro-tool" vs "toy" tell. Budget ≤ 30 ms one-way; > 80 ms and pros walk.

2. **Stems that drift out of sync on playback** — you record, you export, you drag into Logic, and the tracks are off by 20 ms because each machine had a different clock. Pro = sample-accurate. Anything sloppy here = "kid's toy."

4. **Audio dropouts/glitches during collaborative monitoring** — if users are routing audio between machines (via BlackHole later or similar), any glitch = "Zoom call quality."

5. **"Works on my machine" first-run failures** — if a user has to google, open Audio MIDI Setup manually, restart Logic, and grant 4 permissions before their first take, that's friction. Anything > 2 clicks/permissions before first record = cheap.

6. **Visual polish failure under stage lighting** — UI that looks fine in a dim studio but washes out under stage lights, or that flashes distractingly during a take = unprofessional. Same for: animations that don't respect prefers-reduced-motion.

7. **Generic consumer-grade auth (Google sign-in popup, password reset via email)** — pros expect magic link or passkey, not a SaaS login screen.

Hmm, 5. Let me pick the 5 worst:

Actually a key one: **MMC commands clashing with DAW's own transport controls** — if Logic's transport is also being driven by someone hitting spacebar, two sources fight, MMC overrules or vice versa, and you get stuck transport. This is a failure mode.

Let me prioritize the 5 worst "this feels cheap" failure modes:

1. **Transport latency or jitter perceptible to musicians** (>40ms variable, >80ms fixed = death)
2. **Stems out of sync on import into Logic** (anything > 1ms = cheap; this is the acid test)
3. **First-run requires manual sysadmin steps** (open Audio MIDI Setup, restart Logic, fight macOS permissions)
5. **Transport control fights between Logic native + WebJam** (stuck MMC, phantom stop/start)
4. **UI fails accessibility/visibility checks** (unusable under stage lights, can't keyboard-control)

Or another big one:
6. **Sample-rate or bit-depth mismatches causing audible conversion artifacts** — if WebJam records at 16/44.1 and Logic at 24/48, you get SRC artifacts.

Final 5:
1. Transport latency/jitter perceptible (musician can feel it)
2. Stems drift out of sync on Logic import (the acid test)
3. First-run > 2 setup steps (manual sysadmin)
4. Transport control contention (MMC stomped by DAW or vice versa, phantom stops)
5. UI unusable under stage lighting / can't be keyboard-driven

Now **P0/P1/P2 cut line for v1**:

P0 (ship blockers):
- Folder export that drops into Logic with tracks auto-aligned (no manual nudge)
- Rehearse/Record/Mute via MCU/IAC with <30ms latency
- Single-source transport arbitration (no two musicians fighting MMC)
- BWF/iXML timestamps baked into exports
- Visual count-in (already planned)
- Magic-link auth (no passwords)

P1 (must-have for pro feel, but can ship without for early access):
- Take-first-sync-later (DAW records anyway, just uploads after)
- DAW capability probe + readiness panel
- Tablet/touch mixer
- Calibration ritual for latency offset
- A11y: keyboard control, screen reader, high contrast
- Stems both ways (already planned)
- Clean-take checklist (already planned)

P2 (post-v1):
- Ableton Link (optional, already marked optional)
- BlackHole routing (already "later")
- Apple Pencil annotations
- Per-user live latency display
- Auto-IAC setup helper app
- BWF/iXML (wait, is this P0? I said P0. Yes.)

Hmm, let me redo:

P0 = the bare minimum to ship without looking like a toy:
- Logic-ready folder export with BWF/iXML time-stamping (sample-accurate alignment on drag-in)
- Rehearse/Record/Mute via MCU/IAC at <30ms one-way
- Single-source-of-truth transport arbitration
- Visual count-in (already in scope)
- Magic-link auth (no SaaS-style password flow)
- Clean-take checklist (already in scope)
- Stems both ways (already in scope)

P1 = pro polish:
- DAW/browser capability probe with readiness panel
- Take-first-sync-later
</think>

