Stamping the plan. No disk reads. 12 bullets, ruthless.

**(1) Affirm/challenge the P0 cut**

1. **Kill list is correct — affirm all three, hard.** Logic Remote RE (undocumented, Apple breaks it silently), remote plugin/AU UI control (no remotable UI surface exists), and phone transport (MIDI-over-network jitter is unbounded — fatal for anything transport-timed). Cutting these removes every dependency you don't control. Best decision in the plan.

2. **MCU-first is the right spine — affirm.** Mackie Control is bidirectional and Logic echoes button/LED state back over MIDI. That means "feedback truth" is *achievable natively*, not reverse-engineered. This is the one load-bearing assumption that's actually solid. Build on it.

3. **Challenge: "Rehearse/Record mute" is an app concept, not a Logic feature — say so in the plan.** Logic has no rehearse mode. What you're shipping is two app-side mute *presets* layered over Logic track mutes. If the plan implies Logic provides these states, it's wrong and will mislead implementation. Define it as: app owns the profile, Logic owns the mute.

4. **Challenge the P0 boundary: "split local vs Jamulus mute" cannot be fully P0 while BlackHole is phase 3.** The split is a *routing* problem, not a control problem — what Jamulus sends is decided by the audio graph, not by an MCU button. Without the virtual-device routing, P0 can only prove local mute; the "split" half is unprovable. Either promote a minimal BlackHole/aggregate route into P0, or explicitly scope P0 to *local mute only* and stop calling the split done.

5. **Handoff pack (file-first export) is the correct P0 anchor — but decouple it.** It's the zero-real-time-risk deliverable that proves value alone. Good. But it shares nothing with the mute/MCU workstream; don't let either gate the other. Ship them as independent tracks.

**(2) Top 3 excellence risks**

6. **Track-addressing fragility (the silent catastrophe).** MCU addresses the *currently banked 8 tracks by position*, not stable identity. Your "mute the Jamulus track" can land on the wrong track after a bank shift, reorder, or track add — and mute the wrong thing mid-performance with no error. This is the risk that turns a demo into a disaster. Needs a bank-position-to-identity reconciliation strategy before it's trustworthy.

7. **Optimistic UI lying about state.** The instant you assume mute state instead of waiting for the MCU echo, you drift — and "shows unmuted / actually muted" in a live jam destroys trust permanently. Logic must be the single source of truth; the app renders confirmed state only. Also must track *out-of-band* changes (someone mutes in Logic directly).

8. **The split-mute promise outrunning the routing reality.** Related to (4): "local vs Jamulus" is only excellent if a partner on the other Jamulus node *confirms silence*. Control-side mute that doesn't actually change the outbound stream is the kind of half-truth that reads as done in your UI and broken in the room.

**(3) What must be proven in feel tests before any code**

9. **Mute round-trip latency, felt not measured.** Press → Logic mutes → MCU echo → UI confirms. Must feel instant to a player (target ~<100ms, and the *confirm* has to arrive, not just the command). If the echo lags, players will double-press and fight the UI. Prove the loop feels tight before committing to it as the interaction model.

10. **Two-node silence confirmation.** A second Jamulus participant confirms they actually stop hearing the muted source. Prove the split is real at the ear, not the button.

11. **Mute hold across Stop/Start and across bank changes.** Logic track mutes hold through transport naturally — but confirm your *preset* mechanism does too, and that a bank switch doesn't silently repoint or reset it. This is where (6) shows up as a feel bug.

12. **Recovery: MIDI port drop, reconnect, out-of-band Logic edits.** Prove the app re-syncs to Logic's truth after a disconnect and after a human mutes inside Logic — without a stale UI. If recovery isn't proven by hand first, don't write the state machine yet.

Bottom line: kill list — ship it. MCU feedback truth — real, build it. Track addressing and the routing-dependent split — these are where "good" dies; prove them by hand before a line of code.
