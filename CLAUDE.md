# PehlaHarness

A personal agent harness. The plan for the current phase is in
Artifcats/phase-1-agent-loop.html.

## Layout
- channels/  how messages get in and out (Telegram)
- agents/    one folder per agent; each owns its prompts, tools and tables
- core/      shared machinery: gateway, loop, tools, policy, events
- tests/     pytest
- docs/      decision records and write-ups

## Rules
- core never imports from agents or channels. Agents never import each other.
- Every model call goes through core/gateway. Nothing else talks to a model.
- Every tool run goes through core/policy first.
- Secrets come from keyring only. Never print, log or commit them.
- Database/ (ea.db and my queries), allowed_id.txt and private/ are never committed.

## How we work
- One step per session. Do only the step I name.
- Write or update the tests first. Tests never call the network.
- Keep it small and plain: functions over classes, no new dependencies
  unless I agree.
- When done, show me the diff and the pytest output, then stop. I commit.
- If the step is unclear or needs a decision, ask before writing code.

## How to reply
- Blunt and direct. No emojis, filler, hype, praise or softening.
- Do not mirror my tone or wording.
- No offers, suggestions or "next steps" sections I did not ask for.
- When unsure what I mean or want, ask. Never fill gaps with assumptions.
- Stop when the information is delivered. No closing lines.
- Explain the why when it helps me reason it out myself.