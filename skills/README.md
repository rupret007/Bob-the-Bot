# Bob skills snapshot — conductor card (2026-09-22)

Pinned skill texts from about 2026-09-22. This folder is the copy in git. It is not Bob’s live skill store, and nothing in this pull request re-ran these workflows.

`sand-workflow:` links are workflow IDs. They are not paths in this repo.

## Fences

1. **Send.** The first “text them” is a draft. Only Jeff’s separate yes in Bob chat authorizes Andrea. A yes in QA chat does not. Routines never send. If Andrea is down, keep the draft.
2. **Privacy.** Same thread only. Do not read other chats, do not read `chat.db`, and do not put phone numbers in summaries.
3. **Booking.** Research and packages until Jeff says yes. For Rad Dad, Travis owns contact. Do not pitch as Travis or as the band.
4. **One coding lease** on a checkout. Do not put Codex and Cloud on the same tree.
5. **WebJam door.** Use the ten-second gate before calling Art or Music UX ready. Jeff owns merge and feel. The skill does not merge.
6. **Logic.** These skills do not implement the Logic companion. That work stays behind the BUILD GATE in [`research/logic-companion-20260922/`](../research/logic-companion-20260922/README.md).

## Which file

| Folder | Open it when |
|---|---|
| `andrea-band-front-door` | Someone in a band thread writes `@andrea` or replies to NanoBot. Same-thread privacy, then draft. |
| `band-music-ops-desk` | Stalemate, Rad Dad, or another Jeff band needs a digest, show brief, or booking assist. |
| `find-a-show-and-assist-booking` | The job is rooms, one-sheets, or a pitch draft. No outreach yet. |
| `draft-and-send-a-text` | Jeff wants one text sent. Draft here, second yes in Bob chat, Andrea only. |
| `texts-via-andrea` | Jeff wants a redacted summary, or the send path above. |
| `codex-goal-mastery` | You are writing or judging a Codex Goal. Six-part contract. |
| `bob-codex-queue-inject` | You must inject into a watched Mini thread, including Cmd+N when the project changes. |
| `bob-codex-queue-inject-2` | Same inject lane, with the queued `→ Steer` target called out. |
| `multi-llm-stack-mastery` | You are choosing Codex, Claude, Grok, Gemini, or MiniMax. |
| `webjam-ten-second-ux-gate` | You are judging the WebJam Art or Music first screen. |

## Two inject notes

Both inject files are pinned. This snapshot does not retire either one.

- `bob-codex-queue-inject` includes Cmd+N when switching projects, so an in-flight Goal is not hijacked.
- `bob-codex-queue-inject-2` spells the queued Steer control: the `→ Steer` row, not Stop, not the progress-row play control, and not idle Send.

OCR coordinates and the Mini `machineId` inside those files are Sep 22 observations. Re-check the live machine before clicking from memory.

## Referenced, not copied here

| Workflow ID | What the skills expect from it | In this PR |
|---|---|---|
| `codex-prompt-audit` | Prove an inject landed | No |
| `best-llm-for-the-job` | Spend routing | No |
| `claude-code-mastery` | Claude craft | No |
| `multi-llm-stack-smoke-test` | Prove each model resource still answers | No |

If a skill says “pair with” one of those, do not invent the missing text from this folder.

## What this pull request does not prove

These texts were not re-executed here. An empty GitHub check list is not a green run. Private Actions may be billing-blocked. Do not tell Jeff that CI passed.
