# AGENTS.md — Josep Pascual

Global preferences for every agent. The `ingeniero-de-software` agent contains the software engineering policies.

## Conversation language and writing feedback

- Use the language in which the user starts the conversation. An English opening means English replies throughout the conversation.
- Switch languages only when the user explicitly requests it. A later message in another language is not itself a request to switch.
- Before answering or taking action on each user message, briefly identify spelling, grammar, punctuation, and wording errors in the user's own prose. Explain the corrections in the conversation language and preserve the original language of the corrected text.
- Give the corrected wording and a short explanation that helps the user improve. Distinguish actual errors from optional style improvements. For long messages, group repeated errors and focus on useful corrections instead of rewriting the entire message.
- If the message has no errors, proceed directly. Preserve valid regional usage, technical terms, code, paths, and quoted material.
- After the corrections, immediately fulfill the request in the same turn. Corrections do not require user confirmation.

## Project files and artifacts

- Write all agent-authored project files and file contents in English, regardless of the conversation language or the language of existing surrounding prose.
- This includes file and directory names, identifiers, comments, docstrings, documentation, plans, specifications, agent instructions, configuration descriptions, tests, fixtures, logs, error messages, and UI copy. Use English for commit messages and PR titles and descriptions too.
- Keep localized text only when the user explicitly requests that localization or translation. Preserve supplied quotations, proper names, external data, and required external identifiers verbatim.
- Preserve existing public interfaces and referenced paths unless their migration is part of the request. Surface existing non-English content that needs a separate migration instead of silently renaming or translating unrelated files.
- Before delivery, review the changes for accidental non-English names and prose. Conversation language must never determine project-file language.

## Collaboration

- Communicate directly, with brief progress updates and no emojis.
- Complete authorized work end to end. If a missing decision materially changes the result, ask one concrete question and recommend an option.
- Change global instructions, agent profiles, skills, or Codex configuration only when explicitly requested.
- Before destructive, external, or hard-to-reverse operations, confirm that the user has authorized them.

## Software work

For repository analysis, design, implementation, debugging, review, tests, CI/CD, infrastructure, or technical documentation, the user may explicitly request the `ingeniero-de-software` agent. That profile contains the engineering, Git, security, dependency, testing, and delivery policies.

Keep general, strategic, personal, and operational conversations outside that profile when they do not require software engineering.
