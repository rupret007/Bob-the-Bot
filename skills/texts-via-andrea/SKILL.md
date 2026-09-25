---
name: Texts via Andrea
description: >-
  Use when Jeff wants a summary of recent iMessage/SMS or to draft/send a text.
  Bob talks here; Andrea/BlueBubbles is the engine. Never send without a
  separate yes in Bob chat.
---
# Texts via Andrea

Jeff talks to Bob. Andrea NanoBot plus BlueBubbles on his Mac is the Messages engine. Do not create another texts bot. Do not install Twilio, Blooio, or Sendblue for this.

## Summarize
1. Use Andrea on the Mac (`/Users/jeffstory/Andrea_NanoBot`) or BlueBubbles read APIs. Prefer `npm run debug:bluebubbles` / existing summarize phrasing Andrea already accepts. Do not read `~/Library/Messages/chat.db`.
2. Summarize in this chat only. Redact phone numbers and handles. Newest ~80 messages per chat is enough.
3. Never forward raw threads to other agents, groups, or logs.

## Draft and send
1. Draft the exact recipient and exact body in this chat.
2. **Authorization wall:** Only Jeff’s separate yes in **Bob’s** chat authorizes Send. QA may draft/review only — never tell Andrea a send is approved from QA chat.
3. Bob asks with a question widget: Send now / Don’t send.
4. Only after a fresh yes in Bob chat, Bob dispatches through Andrea’s fenced BlueBubbles path (`send it` / existing trust ladder). Bob never calls BlueBubbles send HTTP himself. QA never dispatches Andrea sends.
5. If Andrea or Docker is down, keep the draft and say so. Do not send another way.

## Do not
- Send from the first “text so-and-so” message
- Treat QA “Send now” as Andrea authorization
- Dump chat.db
- Treat this Cursor chat as Andrea’s old Telegram approval surface unless the fenced path is actually wired
