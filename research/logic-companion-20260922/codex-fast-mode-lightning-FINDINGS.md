# Codex “lightning bolt” / Fast mode — search findings

**Date:** 2026-09-22 ~10:45 PM CT  
**Method:** filesystem + OCR/AX dumps + memory + skills + voice transcript. No guessing beyond labeled evidence.

## 1) Lightning bolt toggle — what was found

### Found (concrete)
- ChatGPT desktop **Keyboard shortcuts** lists:
  - **Toggle Fast mode** — “Turn Fast mode on or off in the current composer”
  - Shortcut binding: **Unassigned** (as of dump `20260914-1009-llm-usage/chatgpt-ax-usage2.txt` lines 325–327)
- Live composer AX dumps repeatedly show status text **`Fast mode off`** next to the model / Auto controls (examples: `20260910-2324-llm-usage/chatgpt-ax-usage.txt`, `20260922-2149-llm-usage/chatgpt-ax-usage.txt`).
- Settings sidebar includes a **Speed** row (OCR/AX in multiple usage-pulse folders). That is a settings *category label*, not a documented bolt control.

### Not found
- No AX/OCR string naming a control **“lightning bolt”**, **“Lightning mode”**, or **“Astra Ultra Lightning”** as a UI product toggle.
- No saved note documenting a **1.5×** (or “1.5 percent”) speed factor for any Codex control.
- No Jeff-sent screenshot in Bob attachments / Mini Documents whose OCR describes a lightning-bolt button UI.
- Folder `~/Documents/bob-overnight-inject/20260922-0005-webjam-lightning/` is **overnight WebJam Goal inject evidence**. OCR there shows the **CONTINUE prompt text** “Use Astra Ultra Lightning. Make it amazing.” — wording Bob put in a Goal steer, **not** a UI toggle screenshot guide.

### How to toggle what we *did* find (Fast mode)
Evidence-backed steps only:
1. Open ChatGPT Codex on the Mini with a composer focused.
2. Look near the composer model controls for status **Fast mode off** / on (AX places it beside Auto / model popups).
3. Or open **Settings → Keyboard shortcuts**, search **Toggle Fast mode**, and assign a shortcut if you want one (currently Unassigned in the 2026-09-14 dump).
4. Clicking whatever composer control flips that Fast mode state is the toggle — we did **not** capture a screenshot that proves the control’s glyph is a lightning bolt; that match to Jeff’s description is **unconfirmed visually**.

### Config already set (separate from Fast mode)
`~/.codex/config.toml`: `model = "gpt-6-astra"`, `model_reasoning_effort = "ultra"`, `service_tier = "priority"`. That is Astra Ultra + priority tier, **not** the Fast mode toggle.

## 2) Prior deep-dive notes on using Codex effectively

| Resource | Path / id | What it covers |
|---|---|---|
| Codex Goal mastery | `sand-workflow:codex-goal-mastery` → `/home/box/agent-data/workflows/codex-goal-mastery/SKILL.md` | Six-part Goal contract, lifecycle, Astra Ultra / Extra High, when not to Goal |
| Bob Codex queue inject | `sand-workflow:bob-codex-queue-inject` (+ `-2`) | Mini GUI inject, `/goal`, Steer vs Send, Cmd+N fresh chat, send-arrow PASS checks |
| Multi-LLM stack mastery | `sand-workflow:multi-llm-stack-mastery` | When to use Astra vs Claude vs Grok vs Gemini; lease rules |
| Memory (profile/log) | RecallMemory “Codex” / “Astra Ultra” | Send-arrow coords ~(590,1317) at 2560×1440; Steer only while Pursuing+queued; Ultra when slice earns it |

## 3) Screenshots that exist (and what they show)
- **`20260922-0005-webjam-lightning/*.png`**: ChatGPT Codex overnight WebJam session — Goal stalled / CONTINUE paste / GPT-6 Astra Ultra chip. **Not** a Fast-mode/bolt tutorial.
- **`20260914-1009-llm-usage/chatgpt-usage-live.png`**: Usage & billing settings (Pro $200, Spark meters). **No** lightning toggle visible in that pane.
- Mode/effort chips appear in various inject OCR as **GPT-6 Astra Ultra** / **Extra High** — model/effort pickers, not Fast mode.

## 4) Open gap
To confirm Jeff’s lightning-bolt glyph === Fast mode, need one fresh screenshot of the composer with the control labeled or highlighted. Until then: **Fast mode is the only documented speed toggle**; bolt identity remains Jeff’s description without a matching saved screenshot.
