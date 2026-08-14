---
name: pr-brief
description: Use when the user asks to be briefed on, understand, or review a colleague's GitHub PR — especially code areas the user has not touched — or pastes a PR URL asking "what's going on here / why is this done this way". Not for Dependabot PRs (use carto-ps-dependabot-review) and not for the user's own branches, working tree, or own PRs (use carto-ps-pr-review directly).
---

# PR Brief — orient, review, escalate, triage

Brief the user on an unfamiliar PR **before** any findings appear, run the team review pipeline, escalate each finding to its long-term fix, then step through findings one at a time in the terminal. Nothing reaches GitHub before the single final confirmation in stage 6.

**REQUIRED SUB-SKILL:** `carto-ps-core-team:carto-ps-pr-review` (stage 3). This skill never re-implements that pipeline.

## Stage 1 — Resolve and checkout

1. Check that the `carto-ps-core-team:carto-ps-pr-review` skill is available in this session. If it is not, tell the user immediately and ask whether to proceed briefing-only (stages 1–2) or stop.
2. Parse owner/repo/number from the PR URL. `gh pr view <n> -R <owner>/<repo> --json title,body,baseRefName,headRefName,commits,files,url` (`-R` works without a clone), plus linked issues/Shortcut tickets referenced in the body or branch name.
3. Find the local clone. Check the cwd first; otherwise `find ~ -maxdepth 3 -type d -name <repo> -not -path '*/.*/*' 2>/dev/null`. A name match is not a clone match: verify with `git remote -v` that the candidate references `<owner>/<repo>` — a fork or stale copy silently poisons everything downstream. Multiple verified matches → ask which. None → STOP and ask the user where it lives (or whether to clone it, and where to) — never guess a path.
4. In the clone: pre-flight `git status` and record the current branch. Stop and surface uncommitted changes before `gh pr checkout <n>`. Then `git fetch origin <baseRefName> --depth=100` and set `$BASE=origin/<baseRefName>` — stage 3 declares target resolution satisfied, so it must actually be true here. After the whole flow ends (posted or not), return to the recorded branch; the checkout's local PR branch may stay, mention it in the recap.

## Stage 2 — Deep-dive briefing (before any findings)

Fan out parallel Explore agents in a single message — one **Surroundings** agent per touched area (an area = the team skill's reviewer routing buckets: frontend / api / functions / db-data, falling back to top-level directory; cap at 4, merge small areas) plus one **History** agent:
- **Surroundings** — for each touched area, read the modules around the changed files (callers, the subsystem's entry points, its README section) so the briefing explains the code as it exists, not just the diff.
- **History** — `git log` of the touched files, recent merged PRs on the same paths (`gh pr list --search`), the linked ticket content, and the PR's own discussion so far.

Synthesize and print the briefing in chat, written for a reviewer who has never touched this code:

1. **What it changes** — grouped by concern, not by file.
2. **Why** — the stated intent (ticket, description) and the evidence in history/discussion. Mark inference as inference.
3. **How it fits** — where the touched subsystems sit in the architecture, what depends on them.
4. **Where to look** — the 2–4 spots that deserve the reviewer's attention and why.

Do not mention findings yet. The briefing is orientation, not judgment.

## Stage 3 — Findings via the team pipeline

Print a one-line status first so the user knows briefing → findings is in progress. Then invoke `carto-ps-core-team:carto-ps-pr-review` — its instructions load into your context and you follow its steps yourself. Treat its target-resolution step as already satisfied by the stage-1 checkout and `$BASE` fetch (same session, state carries over) and run everything through its report emission — classification, reviewer fan-out, prior-review audit, adversarial verification, printed report. **Stop before its posting selector** (the step that asks keep-local vs post): stages 5–6 below replace it. Keep its verified findings list with severities, `file:line`, comments, and suggestions. If the pipeline emits zero verified findings, print the clean report and stop — stages 4–6 have nothing to work on (gaps only exist via findings). State that plainly, return the clone to the recorded branch (mentioning the leftover local PR branch), and end without any posting question.

## Stage 4 — Systemic-fix escalation

For each verified finding, ask: **what prevents this class of issue from recurring?** Attach a `systemic_fix` when one exists. Two kinds:

- **Tooling** — a lint rule, formatter, type-checker, pre-commit hook, CI stage, or scanner would have caught it. First read the repo's actual config (`ruff`/`eslint` config, `.pre-commit-config.yaml`, CI workflows): it is only a gap if the rule is absent or disabled. Name the exact mechanism and placement (e.g. import inside a function → ruff `PLC0415` in pre-commit + CI lint stage). A tooling suggestion without a named rule is noise — drop it.
- **Design** — the recurrence guard is a shape change: extract an abstraction over duplicated code, move validation to the I/O boundary, encode the invariant in a type. Apply the user's DRY judgment: literal repetition → the systemic fix is "extract now"; similar-but-conceptually-distinct shapes → NOT a systemic fix — show a restraint note during step-through ("looks duplicated, but distinct domains; wait for the third call site") that is never offered for posting.

Dedup systemic fixes across findings into **repo-level gaps** (five inline-import findings → one "enable PLC0415" gap). Keep the finding↔gap links. A gap survives even if every finding linked to it is later dropped — it is a repo-level observation; note the drops when triaging it.

For each finding with a systemic fix, draft the "longer term: …" sentence now, so the user sees the exact posted wording during step-through.

## Stage 5 — Step-through triage

First print a one-screen overview: the risk header + a numbered list (severity tag + one-liner per finding). Map whatever severity scale the pipeline emits onto the user's tag set by meaning, not by label: must-fix-before-merge → `[blocker]`, important-but-not-blocking → `[should fix]`, cosmetic → `[nit]`, no-opinion-asking → `[question]`, genuinely-noteworthy-positive → `[praise]`.

Then present **one finding at a time**:
- The finding: tag, comment, suggestion block if any.
- The real code context around `file:line`, read from the checkout — enough to judge without an editor.
- Its systemic fix, if one exists.

Ask per finding with AskUserQuestion — at most 4 named options (the tool's hard limit): **Post** / **Post with systemic suggestion** (only when the finding has a systemic fix; the comment gains the drafted "longer term: …" sentence) / **Drop** / **Discuss**. Rewording needs no named option: the user types replacement text via the built-in Other, which means post-with-that-wording — the typed text is the full posted comment, nothing is appended to it. On Discuss, talk it through — the stage-2 context stays available for "why is this code like this" questions — then re-ask. If AskUserQuestion is unavailable, ask in plain text with the same options.

After the last finding, triage the **repo-level gaps** in one batch: a single multi-select AskUserQuestion (plain-text fallback) — tick the gaps to include in the top-level review body, untick to skip. For a gap the user includes, offer — only now, never unprompted — to file a tracker ticket or draft the config/refactor as a follow-up. Accepted tickets/follow-ups are queued and executed only after the stage-6 confirmation, never before.

## Stage 6 — Recap and single posting confirmation

Print the recap: findings to post inline (with final wording), review-body content (summary + included repo-level gaps). Ask one confirmation. On yes, post via the team skill's `references/post-to-github.md`; if that file is missing or its posting path is broken, STOP and hand the user the composed review content to paste manually — never improvise raw `gh api` posting. Approved findings go as inline comments anchored to diff lines, cross-cutting content in the review body, always as review event **COMMENT** (informational — never REQUEST_CHANGES or APPROVE; the human decides the verdict on GitHub). On no, the review posts nothing — but queued tickets/follow-ups do not silently die with it: ask whether they still proceed. Either way, return the clone to the branch recorded in stage 1.

## Guardrails

- **Nothing posts to GitHub before the stage-6 confirmation.** Per-finding "Post" answers select content; they do not send it.
- **Briefing before findings, always.** Orientation loses its value once judgment has been rendered.
- **Do not duplicate the team pipeline.** If `carto-ps-pr-review` is unavailable, stop and tell the user — do not improvise a replacement review.
- **Report faithfully.** If a stage failed or was skipped, say so in the recap.

## Common mistakes

| Mistake | Fix |
|---|---|
| Briefing that narrates the diff file-by-file | Group by concern; explain the *why* and the surrounding architecture |
| Systemic fix = "add linting" | Name the exact rule and where it plugs in, or drop the suggestion |
| Suggesting an abstraction over two similar-but-distinct blocks | Third-call-site rule: note it, recommend waiting |
| Treating per-finding "Post" as permission to post | Only the stage-6 confirmation sends anything |
| Re-running target resolution inside the team skill | Pass the already-checked-out PR and base ref into stage 3 |
