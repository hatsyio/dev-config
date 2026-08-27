---
name: pr-brief
description: Use when the user asks to be briefed on, understand, or review a colleague's GitHub PR — especially code areas the user has not touched — or pastes a PR URL asking "what's going on here / why is this done this way". A bare pasted PR URL also triggers this skill (stage 1 routes the user's own and Dependabot PRs away). Not for Dependabot PRs (use carto-ps-dependabot-review) and not for the user's own branches, working tree, or own PRs (use carto-ps-pr-review directly).
---
# PR Brief — orient, review, escalate, decide on paper

Brief the user on an unfamiliar PR **before** any findings appear, run the team review pipeline, escalate each finding to its long-term fix, then hand the user **one report file** where they read, edit, and decide. Nothing reaches GitHub before the single final confirmation in stage 6.

**REQUIRED SUB-SKILL:** `carto-ps-core-team:carto-ps-pr-review` (stage 3). This skill never re-implements that pipeline.

## Stage 1 — Resolve and checkout

1. Check that the `carto-ps-core-team:carto-ps-pr-review` skill is available in this session. If it is not listed but its SKILL.md exists on disk (plugin cache/marketplace, possibly a newer version than the session loaded), read that file and follow it — that is the real pipeline, not improvisation. Only when no pipeline definition is readable: tell the user immediately and ask whether to proceed briefing-only (stages 1–2) or stop.
2. Parse owner/repo/number from the PR URL. `gh pr view <n> -R <owner>/<repo> --json author,title,body,baseRefName,headRefName,headRefOid,commits,files,url` (`-R` works without a clone), plus linked issues/Shortcut tickets referenced in the body or branch name. Enforce the routing the description promises: if the author is the user (`gh api user`), hand off to `carto-ps-pr-review` directly; if the author is `dependabot[bot]`, hand off to `carto-ps-dependabot-review`. The briefing is for colleagues' work.
3. Find the local clone. Check the cwd first; otherwise `find ~ -maxdepth 3 -type d -name <repo> -not -path '*/.*/*' 2>/dev/null`. A name match is not a clone match: verify with `git remote -v` that the candidate references `<owner>/<repo>` — a fork or stale copy silently poisons everything downstream. Multiple verified matches → ask which. None → STOP and ask the user where it lives (or whether to clone it, and where to) — never guess a path.
4. In the clone: pre-flight `git status` and record the current branch (on detached HEAD, record the SHA). Stop and surface uncommitted changes before `gh pr checkout <n>`.
   - If checkout fails because the PR branch lives in another worktree ("is already used by worktree at <path>"): use THAT worktree as the review checkout. Pre-flight `git status` there too — never update a dirty worktree. Verify its `git rev-parse HEAD` equals the PR's `headRefOid` (from step 2); update only if clean and stale, via `gh pr checkout <n>` run inside that worktree — never `reset --hard`. The main clone stays untouched.
   - Then `git fetch origin <baseRefName>` — a full fetch, never `--depth` (a depth-limited fetch leaves the clone shallow and can silently compute a wrong merge-base) — and set `$BASE=origin/<baseRefName>`. Stage 3 declares target resolution satisfied; this step makes that true.
   - After the whole flow ends (posted or not), return to the recorded branch. The local PR branch may stay; mention it in the recap.

## The report file

Every run produces exactly one Markdown file: `~/pr-briefs/<owner>-<repo>-pr<n>.md` (`mkdir -p ~/pr-briefs`). It lives outside the repo, survives the session, and is the **single source of truth** for what posts and with which wording. Stage 2 writes §1–§2; stage 5 writes §3–§4; stage 6 reads the file back and appends §6.

If the file already exists (re-review), first copy each old finding/gap one-liner with its `Decision:` into `## 5. Previous rounds`, then overwrite the rest.

Skeleton — keep the headings and field names exactly; stage 6 parses `Decision:` lines and ```comment fences:

```markdown
# PR <n> — <title>
<owner>/<repo> · @<author> · <base> ← <head> · <url> · round <k> · <date>

## 1. What and why
### What it changes
<grouped by concern, not by file>
### Why
<stated intent (ticket, description) + evidence from history/discussion; mark inference as inference>
### Where to look
<2–4 spots that deserve attention and why>

## 2. How it fits the codebase
| File | Change | Where it sits | Fits? |
|---|---|---|---|
| path | added / modified / deleted / moved from `old` | module role, layer, who depends on it | OK, or `flag: <why>` |
<prose: where the touched subsystems sit in the architecture; every `flag` explained>

## 3. Findings
### F1 · [blocker] · `path:line` — <one-liner>
- What the code does: …
- What breaks: …
- Why this severity: …
- Systemic: G1 | none
- Restraint: none | addressed-as-agreed | third-call-site
- Recommendation: post | post+systemic | drop
```comment
<draft comment, verbatim as it would post>
```
```suggestion
<pipeline suggestion block, if any>
```
Decision: post

## 4. Systemic gaps
### G1 · <name> · size: small | large · from F1, F4
- What recurs: …
- Mechanism: <exact rule / config / shape change and where it plugs in>
- Recommendation: in-pr | ticket
```comment
<in-pr ask wording, or ticket title + body>
```
Decision: in-pr

## 5. Previous rounds
<re-review only: F/G one-liners + decisions from the earlier file>

## 6. Posted
<stage 6 appends: date, review URL, what posted, what was dropped and why>
```

`Decision:` is prefilled with the recommendation so an unedited file means "I agree". Restraint findings are prefilled `drop`. Allowed values — findings: `post`, `post+systemic`, `drop`, `discuss`; gaps: `in-pr`, `ticket`, `drop`, `discuss`. The user may also rewrite the text inside any ```comment fence; that text posts verbatim. A ```suggestion fence survives unless deleted.

## Stage 2 — Deep-dive briefing (before any findings)

Fan out parallel Explore agents in a single message — one **Surroundings** agent per touched area (an area = the team skill's reviewer routing buckets: frontend / api / functions / db-data, falling back to top-level directory; cap at 4, merge small areas) plus one **History** agent:
- **Surroundings** — for each touched area, read the modules around the changed files (callers, the subsystem's entry points, its README section) so the briefing explains the code as it exists, not just the diff. Also report, per touched file, its role and whether its location follows the repo's structure and naming (sibling modules, existing layers, where similar files already live).
- **History** — `git log` of the touched files, recent merged PRs on the same paths (`gh pr list --search`), the linked ticket content, and the PR's own discussion so far.

Synthesize into **§1 What and why** and **§2 How it fits the codebase** of the report file, written for a reviewer who has never touched this code. §2 lists every file from `gh pr view --json files` (added / modified / deleted / moved — detect moves with `git diff --stat -M $BASE...HEAD`) and answers, per file, whether it makes sense where it is. `flag:` when a file lands in the wrong layer, duplicates an existing module, breaks a naming convention, leaves callers orphaned after a delete/move, or when a move loses history without reason. A `flag` in §2 is orientation, not a finding; stage 4 may promote a repeated one to a gap.

Do not write findings yet. Print one line in chat: the file path and "briefing written, running findings".

## Stage 3 — Findings via the team pipeline

Print a one-line status first so the user knows briefing → findings is in progress. Then invoke `carto-ps-core-team:carto-ps-pr-review` — its instructions load into your context and you follow its steps yourself. Treat its target-resolution step as already satisfied by the stage-1 checkout and `$BASE` fetch (same session, state carries over) and run everything through its report emission — classification, reviewer fan-out, prior-review audit, adversarial verification, printed report. **Stop before its posting selector** (the step that asks keep-local vs post): stages 5–6 below replace it. Keep its verified findings list with severities, `file:line`, comments, and suggestions. One addition to its prior-review fetch: extend the jq to also capture each prior comment's `id` and `in_reply_to_id`, so stage-6 thread replies target exact threads instead of fuzzy-matching by path/line. If the pipeline emits zero verified findings, print the clean report and stop — stages 4–6 have nothing to work on (gaps only exist via findings). State that plainly, return the clone to the recorded branch (mentioning the leftover local PR branch), and end without any posting question.

## Stage 3.5 — Re-review restraint (protect the colleague from re-litigation)

This stage runs **only on a re-review** — a second or later pass where the stage-3 prior-review audit found earlier review comments (ours or the team's) that the colleague has since addressed. On a first review there is nothing to re-open; skip it.

**The failure it prevents:** the colleague implemented the agreed fix, and the re-review requests changes on that same concern anyway — not because the fix is wrong, but because you now want it specified more tightly, or you now lean toward a different strategy. Both re-open a settled question and make the colleague redo work that was never defective. **You cannot keep re-asking the same person about the same area across passes.** A review that moves its own goalposts is not honest.

Classify each verified finding against the prior-review audit:

1. **Brand-new defect** — the fix introduced a new problem on a concern no prior comment raised. A normal new finding. This stage does not touch it; it flows to stage 4 at its real severity.
2. **Re-opens an addressed concern** — a prior comment raised it, the colleague changed that code, and the concern is resolved by any reasonable reading. Apply the bar below.

**The bar for re-opening an addressed concern — blocker only.** Raise it a second time **only if the implemented fix breaks something or is critical**: a correctness bug, data loss, security hole, or broken contract that the fix introduced or left behind. Everything below blocker — "specify it more", "I'd do it differently now", cosmetic, style, a cleaner abstraction — is **suppressed**: mark it `addressed-as-agreed — not for re-posting` and carry it into stage 5 as a restraint note (surfaced, never in the auto-post set — see stage 5).

**Systemic reveals go to a ticket, not back to the colleague.** If a suppressed re-open exposes a genuine recurring or systemic issue, do not re-ask on this PR. Route the long-term fix to a repo-level gap → follow-up ticket via stage 4/5, and never post a blocking comment on the colleague's PR for it. The colleague's fix stands; the class-level fix is separate work.

**Red flags — you are about to re-litigate a settled concern:**
- "The fix works, but I'd specify it more precisely now."
- "This is fine, but a different strategy would be cleaner."
- "It's technically addressed, but while we're here…"
- "I agreed this shape last round, but…"

All of these mean: **the concern is settled. Suppress it as a restraint note unless it is a blocker.**

| Re-review rationalization | Reality |
|---|---|
| "The fix is fine but under-specified" | Under-specification you did not raise last round is your change of mind, not their defect. Suppress. |
| "A different strategy is cleaner now" | You accepted the strategy when you agreed the fix. Re-opening it burns the colleague's time. Suppress. |
| "It's a small extra tweak on the same line" | Small + already-addressed is still re-litigation. Suppress unless blocker. |
| "It's a recurring pattern, I should flag it" | Flag the pattern as a follow-up ticket, not as a repeat change-request on this PR. |
| "I'm just being thorough" | Thorough is not endless. Honest review does not move its own goalposts across passes. |

## Stage 4 — Systemic-fix escalation

For each verified defect finding, ask: **what prevents this class of issue from recurring?** Attach a `systemic_fix` when one exists. Two kinds:

- **Tooling** — a lint rule, formatter, type-checker, pre-commit hook, CI stage, or scanner would have caught it. First read the repo's actual config (`ruff`/`eslint` config, `.pre-commit-config.yaml`, CI workflows): it is only a gap if the rule is absent or disabled. Name the exact mechanism and placement (e.g. import inside a function → ruff `PLC0415` in pre-commit + CI lint stage). A tooling suggestion without a named rule is noise — drop it.
- **Design** — the recurrence guard is a shape change: extract an abstraction over duplicated code, move validation to the I/O boundary, encode the invariant in a type. Apply the user's DRY judgment: literal repetition → the systemic fix is "extract now"; similar-but-conceptually-distinct shapes → NOT a systemic fix — emit a restraint finding in the report ("looks duplicated, but distinct domains; wait for the third call site") that is never offered for posting.

Dedup systemic fixes across findings into **repo-level gaps** (five inline-import findings → one "enable PLC0415" gap). Keep the finding↔gap links. A gap survives even if every finding linked to it is later dropped — it is a repo-level observation; note the drops when triaging it.

On a re-review, a systemic pattern surfaced by a suppressed re-open (stage 3.5) attaches **only** as a repo-level gap → follow-up ticket. It never becomes a repeated change-request comment on the colleague's PR.

**Size every gap** — the size decides the recommendation, and the default is NOT "file a ticket":

- **small** — enabling an existing rule, one config line, one pre-commit hook or CI step, a version pin, or a ≤20-line code change inside files the PR already touches, with no design decision and no behavior change for consumers. Recommendation `in-pr`: draft a review-body paragraph asking the author to include it in this PR, with the exact change spelled out (rule id, file, placement).
- **large** — touches files outside the PR, introduces an abstraction or module, needs a migration, its own tests, or a design choice. Recommendation `ticket`: draft the ticket (title; body = problem, evidence findings, proposed fix, scope). Never ask the colleague to grow this PR with it.
- Tie-break: if the author can do it in under 30 minutes with no new decision, it is small.

Exception: a gap that exists only because of a stage 3.5 suppressed re-open is always `ticket`, whatever its size.

For each finding with a systemic fix, draft the "longer term: …" sentence now, so the user sees the exact posted wording in the report.

## Stage 5 — Report and decisions

Write **§3 Findings** and **§4 Systemic gaps** into the report file. Map whatever severity scale the pipeline emits onto the user's tag set by meaning, not by label: must-fix-before-merge → `[blocker]`, important-but-not-blocking → `[should fix]`, cosmetic → `[nit]`, no-opinion-asking → `[question]`, genuinely-noteworthy-positive → `[praise]`. Order findings by severity, then by file. Each finding carries the real code context around `file:line`, read from the checkout — not the pipeline's paraphrase.

Restraint findings — stage 3.5 `addressed-as-agreed`, or a stage 4 third-call-site note — get `Restraint:` set, the reasoning in the bullets, and `Decision: drop` prefilled. They are never in the auto-post set.

Then print in chat, and END the turn:
1. The file path.
2. A one-screen overview: risk header, then one numbered line per finding and gap — `F1 [blocker] path:line — one-liner → post`, using the prefilled decisions.
3. The instruction: "Edit `Decision:` lines and comment text in the file, then reply `done`. Or give decisions here (`F1 drop, G2 ticket`)."

Decisions given in chat are written back into the file before stage 6, so the file stays the source of truth. `discuss` (in the file or in chat) is talked through in chat with the stage-2 context available; write the outcome back as a final decision and, if the wording changed, into the ```comment fence. Chat text that reads as an instruction ("make it softer", "drop F3–F5") is an instruction — act on it and confirm the resulting wording; never post instruction text verbatim.

Accepted `ticket` gaps and `in-pr` asks are queued; nothing is filed or posted until stage 6.

## Stage 6 — Recap and single posting confirmation

Re-read the report file. Refuse to proceed while any `Decision: discuss` remains or a value is outside the allowed set — resolve those first. If a non-blocker `addressed-as-agreed` finding is set to `post`, confirm the override explicitly: it re-opens a settled concern with the colleague.

Print the recap in chat, in four parts: inline findings to post (final wording from the ```comment fences), review body (summary + `in-pr` gap asks), thread replies, and queued tickets. The recap ENDS its turn as plain text; take the single confirmation from the user's text reply. On yes, post via the team skill's `references/post-to-github.md` (resolve the path from the stage-3 skill load's base directory), under these overrides and rules:

- **Payload = the approved subset only**, with the wording from the file — never the pipeline's raw report. Keep each finding's original `code_snippet` intact so inline anchoring still works.
- **No auto-fallback.** Ignore the reference's `|| gh pr comment`; on any posting failure — or if the reference file is missing — STOP and hand the user the composed content. Never improvise raw `gh api` posting.
- **No silent dedup.** The reference's dedup-by-`path:line:side` does NOT apply to the approved subset — triage already decided what posts, and re-reviews legitimately land on previously-commented lines. If anything is dropped for any reason, say so after posting.
- **Anchoring.** Out-of-hunk findings anchor to the nearest hunk line with the real location called out at the top of the comment body; the review body is reserved for genuinely cross-cutting content.
- **Order: review first, thread replies second.** A finding that responds to an existing PR thread (a still-open prior finding, or closing a thread the author declined once the user has ruled on it) posts as a reply (`gh api .../pulls/<n>/comments/<id>/replies`, using the ids captured in stage 3) — never as a new comment. The recap labels these as thread replies.
- **Event: always COMMENT** — never REQUEST_CHANGES or APPROVE; the human decides the verdict on GitHub.

After posting, file the queued tickets, then append **§6 Posted** to the report file: date, review URL, what posted, what was dropped and why, ticket links.

On no, the review posts nothing — but queued tickets do not silently die with it: ask whether they still proceed. Either way, return the clone to the branch recorded in stage 1.

## Guardrails

- **Nothing posts to GitHub before the stage-6 confirmation.** Per-finding "Post" answers select content; they do not send it.
- **Briefing before findings, always.** Orientation loses its value once judgment has been rendered.
- **The report file is the source of truth.** Decisions and wording live in the file; chat decisions are written back before stage 6. Findings are never walked through one by one in chat.
- **Size gaps before routing them.** Small gaps are in-PR asks; only large refactors become tickets.
- **Re-review restraint (stage 3.5).** A concern the colleague already addressed as agreed is not re-opened for tighter specification or a different strategy — only a blocker (breakage/critical) re-opens it. Systemic patterns become follow-up tickets, never repeat change-requests on the same PR.
- **Do not duplicate the team pipeline.** If `carto-ps-pr-review` is unavailable, stop and tell the user — do not improvise a replacement review.
- **Report faithfully.** If a stage failed or was skipped, say so in the recap.
- **When the user asks you to apply fixes to the PR branch instead of posting:** stage files explicitly by path — never `git add -A`/`git add .` (tooling side-artifacts like stray lockfiles get swept into the PR silently). Diff-stat the commit against the intended file list before pushing, and confirm before pushing when the branch belongs to a colleague — pushing to someone else's PR is outward-facing.

## Common mistakes

| Mistake | Fix |
|---|---|
| Briefing that narrates the diff file-by-file | Group by concern; explain the *why* and the surrounding architecture |
| Systemic fix = "add linting" | Name the exact rule and where it plugs in, or drop the suggestion |
| Suggesting an abstraction over two similar-but-distinct blocks | Third-call-site rule: note it, recommend waiting |
| Re-running target resolution inside the team skill | Pass the already-checked-out PR and base ref into stage 3 |
| Re-requesting changes on an already-fixed concern because you'd specify it differently now | Re-review restraint: blocker-only bar; suppress refinements and strategy changes as restraint notes |
| Re-flagging a recurring issue as a repeat PR comment | Route systemic reveals to a follow-up ticket; the colleague's fix stands |
| Walking findings through chat one at a time | Write §3/§4 to the report file; the user decides in the file |
| Every systemic gap becomes a ticket | Size it: enabling a rule or adding a CI line is an in-PR ask |
| §2 file table that repeats `git diff --stat` | Say what each file is, where it sits, and whether that location fits |
| Posting the pipeline's comment text after the user edited the fence | The ```comment fence in the file is what posts, verbatim |
