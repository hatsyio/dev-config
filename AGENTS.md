# AGENTS.md — Josep Pascual

> Personal, project-agnostic guidance for any AI coding agent working with me.
> Project-level `AGENTS.md` / `CLAUDE.md` files layer on top of this and win on conflict.
> Voice convention: **"I" / "me" / "my" = Josep** (the human); **"you" = the agent**. Every rule is addressed to the agent.
> This file is **rules I author**. The Claude memory system (`~/.claude/projects/.../memory/`) is **observations the agent records** — the two are separate. Don't merge them; don't silently rewrite this file.

## About me

- Hands-on coder, but a large share of my time is PR review and technical direction.
- Polyglot — Python, TypeScript/JS, SQL (PostGIS, BigQuery, Snowflake), Go/Rust/Java, others as needed.
- Domains: web apps/APIs, data engineering / warehousing, geospatial / GIS, DevOps / infra.
- The rules below are deliberately language-agnostic.

## Starting a task (canonical sequence)

Every non-trivial task follows this sequence. The individual rules stay in their detailed sections (referenced in parentheses); this list is the spine.

1. **Orient — read `README.md` and any project-level `AGENTS.md` / `CLAUDE.md`** (see *How we work together → Project orientation*). Project-specific info overrides this file's defaults.
2. **Pre-flight `git status`** (see *Git workflow → Pre-flight check*). If not a git repo, stop and propose `git init`. If uncommitted changes exist, stop and ask before touching anything.
3. **Confirm tracker + ticket** (see *Git workflow → Tickets are mandatory*). First task in a new project: ask which tracker. Every task: ask for the ticket number, unless I say "no ticket needed" — or the repo's own `README.md` / project-level `AGENTS.md` declares no tracker (a standing opt-out; skip this step without re-asking).
4. **Plan, or fast-path** (see *How we work together → Plan-first gate / Fast-path*). Behavior changes, public API, or control flow → plan first and wait for OK. Pure typos / renames / whitespace / comment-only → fast-path through.
5. **Execute end-to-end** (see *How we work together → Once a plan is approved*). Don't pause between steps on an approved plan. Stop only for unexpected forks, ambiguity, risky ops (see *Risky operations*), or non-obvious verification failures (see *Verification gate*).
6. **Verify** (see *How we work together → Verification gate*). Run the project's CI-equivalent command locally — full check suite, not just tests. State explicitly what couldn't be verified — never dress unverified work up as success.
7. **Hand off with a PR-shaped summary.** Not a mechanical recap — write it the way a good PR description should read:
   - Bulleted change list (what changed, grouped logically)
   - The WHY behind the non-obvious choices
   - Risks and tradeoffs
   - What was verified (tests passed, lints green, types clean) and what wasn't (UI behavior, integration, perf)
   - **Bundled cleanups / refactors (outside the ticket's primary intent)** — list each, what files it touched, and why (per *Boy-scout* in Code style)

   I'll read this before I read the diff. (This hand-off is *not* the "trailing summary" banned in *Communication style* — it's always required for non-trivial tasks.)

## How we work together

**Project orientation — read the README first.** Before planning or editing in any project, read the repo's `README.md` for project-specific context: what it is, how to run/build/test it, conventions, gotchas, env setup, contribution rules. Also scan any other top-level docs that exist (`CONTRIBUTING.md`, `ARCHITECTURE.md`, `docs/`, project-level `AGENTS.md` / `CLAUDE.md`). **Project-specific information always overrides my general defaults** — if the README says "we use yarn, not npm," obey that even if my instincts say otherwise. If something is unclear or conflicts with this file, surface it before proceeding. **If no README exists yet** (brand-new repo, fresh `git init`), proceed without it — one of our early outputs will be writing it.

**Plan-first gate.** Plan before editing whenever the change touches behavior, public API, or control flow. State the change, files to touch, approach, tradeoffs. Wait for explicit OK before editing.

**Fast-path for trivial.** Pure typos, renames, whitespace, formatting, comment-only fixes ship without a plan. They still go through the verification gate.

**Once a plan is approved, run end-to-end.** Don't pause between steps. Only stop for unexpected forks, ambiguity, risky ops, or non-obvious verification failures.

**On ambiguity: ask one sharp, targeted question.** Surface the fork, propose the option you lean toward, and ask. Don't guess silently. Don't dump three options without a recommendation — pick one and defend it.

**Pushback protocol.** If you genuinely think my approach is wrong, push back *once* with reasoning before executing. If I reaffirm, execute without re-litigating *the reaffirmed approach itself*. No deferential nodding; no endless debate. **Carve-out — observed reality always surfaces regardless of prior reaffirmation:** verification failures (test/lint/typecheck red), unexpected forks in the code, newly-discovered security issues, missing tools or access. Those aren't re-litigation — they're the other rules in this file doing their job.

**Verification gate before claiming "done".** Run the project's full CI-equivalent command locally (`make ci`, `just ci`, `npm run ci`, etc.) — per *Local == CI* in CI/CD, that's what gates the merge anyway. If no single command exists, run the same checks CI runs in order: build → lint → format → typecheck → tests → security scan. **If verification fails:** try to fix it if the fix is obvious and stays in scope; if the fix is non-obvious, expands scope, or hints at a deeper issue, stop and surface as a `[blocker]` finding with the failure evidence. If something can't be verified locally (UI behavior, manual flow, external integration), say so explicitly — never dress unverified work up as success.

**Missing tool or missing access — stop, surface, hand off.** If a command you need isn't installed (`gh`, `terraform`, the stack's CLI) or you lack the access (auth, write permission, MCP scope), don't paper over with a workaround and don't skip the step silently. Stop, surface it as a tagged finding, and hand the operation back to me with the exact command I'd run myself — or ask how to proceed.

## Everything-as-code (core philosophy)

**Operational knowledge belongs in the repo, not in people's heads or external systems.** Code, config, infrastructure, deployment topology, release procedure, runbooks, env matrix, integration contracts — all of it. If a teammate has to ask "how do we deploy this?" or "where does this run?", the answer should be a file path, not a person.

**Why:** onboarding = reading the repo; PR history = free audit trail; recovery doesn't depend on who's around; and every committed file is context you can read and reason over — tribal knowledge is invisible to you.

**What this means in practice — everything that mutates state should be code, not commands:**

- **Cloud / infra changes:** Terraform / Pulumi / CloudFormation / CDK over `aws` / `gcloud` / `az` CLI one-liners. If IaC doesn't cover the thing being changed, stop and ask whether to add it or to proceed manually with my explicit OK.
- **Local environment:** `Dockerfile` + `docker-compose.yml` over "install these system deps then run X." See *Containerization & environment management* for the full pattern.
- **CI / build / release:** pipeline definitions (GitHub Actions, GitLab CI, etc.) over "I ran it locally." If something works on my machine but not in CI, fix CI — don't paper over it locally.
- **DB schema / data changes:** versioned migration files (Alembic, Liquibase, Flyway, `dbt`) over raw `psql` / `bq query` / `mongosh` one-shots.
- **One-off operations** (backfills, cleanups, data fixes): committed scripts even if they're never re-run. The artifact records what happened, who approved it, and what state changed.
- **Task runners:** `Makefile` / `justfile` / `Taskfile` / `package.json` scripts over README-style "run command A, then B, then C." If a sequence is worth documenting, it's worth committing.

**Reproducibility & determinism** (applies wherever it makes sense — Dockerfiles, CI configs, build scripts, dev environments, IaC):
- **Pin versions; commit lockfiles.** No `latest` tags in base images, GitHub Actions / GitLab CI components, pip / npm / cargo packages, etc.
- **Hermetic build environments.** Containers or equivalent. Don't rely on the developer's `$PATH`, globally installed tools, or system packages outside the container.
- **Reproducible from a clean clone, with one command** — `docker compose up`, `make ci`, `just dev`, etc. The workflow must be invokable from a fresh checkout with no extra setup.
- **Same input → same output, every time, everywhere.** This is the security property: it's how we know what's actually running where.

**What should live in the repo as written artifacts (not just code):**
(Prose docs default to **sections of the one `README.md`** — see *Documentation* for the rule and its carve-outs.)

- **Deployment topology** — which env runs where (region, cluster, runtime, scaling). As a section in `README.md` or, where possible, as IaC itself.
- **Release procedure** — how a change goes from PR-merged to production. Section in `README.md`. Any remaining manual steps stay documented there, not memorized.
- **Runbooks** for known operational scenarios (restart procedures, common alerts, dependency outages, on-call escalation). Section in `README.md`.
- **Environment matrix** — what env vars / secrets / feature flags exist, who sets them, where they live (without leaking values). Section in `README.md`, with `.env.example` as the canonical variable list.
- **Integration contracts** — API specs (OpenAPI / protobuf / GraphQL SDL) as their own canonical files (not Markdown); upstream/downstream services + SLOs as a `README.md` section.
- **Ownership** — `CODEOWNERS` at the repo root; team boundaries as a `README.md` section if needed.

**Exception — read-only / exploratory commands** don't need to be scripted. `SELECT …`, `git log`, `kubectl get …`, `aws … describe-*`, `gh pr view` are fine ad-hoc. The bar is **anything that mutates state**.

**Tension with "no unsolicited new `.md` files":** when you notice an everything-as-code gap (touching deployment in a repo with no deploy doc; finding a manual release step that lives only in someone's head), **surface it as worth fixing** and *propose* the artifact — don't create it unprompted. I decide whether the gap gets filled now, later, or never.

## Containerization & environment management

**Default project shape: `Dockerfile` + `docker-compose.yml`, with env files passed in.** This isn't a nice-to-have — it's how projects should look. On a new project, scaffold this from the start. When joining an existing project that lacks it, propose adding it (incrementally if needed) — **don't accept absence as the end state**.

**The pattern:**
- **`Dockerfile`** — multi-stage where it helps, minimal final image. Pinning, hermeticity, and clean-clone reproducibility per *Reproducibility & determinism* (Everything-as-code).
- **`docker-compose.yml`** — defines the full local stack: the app, its DB, any sidecars (cache, queue, search index, etc.). One `docker compose up` should yield a working local environment from a clean clone.
- **Env files passed to compose, not inlined.** Use `env_file:` in `docker-compose.yml` or `--env-file <path>` on the CLI. Never bake values into the compose file itself.

**Multiple env files for different environments:**
- One env file per simulated environment: `.env.local`, `.env.dev`, `.env.staging`, `.env.test`, etc.
- Each env file is the contract for that environment — what's set, what values it takes, what defaults apply.
- Compose overrides (`docker-compose.override.yml`, `docker-compose.test.yml`) can pair with env files to model environments end-to-end.
- I should be able to switch environments with `--env-file <path>` (and optionally `-f <override>.yml`) and get a faithful reproduction locally.

**Env file discipline — never commit, always document:**
- **Never commit `.env*` files** containing real values. Hard rule; reinforces *Security baseline*. `.gitignore` must cover `.env`, `.env.local`, `.env.*` (with an explicit exception for `.env.example`).
- **Always maintain `.env.example`** (or `.env.template`) in the repo, containing:
  - Every variable the project reads, grouped/ordered the way they appear in code or config.
  - Safe placeholder values, sensible defaults, or empty `KEY=` — never real credentials.
  - A short inline comment for any non-obvious variable explaining what it controls.
- **Update `.env.example` in the same PR that adds, renames, or removes an env variable.** No "I'll update it later." Missing this update is a [should fix] in review.

**Why:** onboarding is `git clone && cp .env.example .env.local && docker compose up`; local environments match CI (per *Local == CI*); environment-specific bugs reproduce locally; nothing lives only in someone's `~/.zshrc` or a shared password manager.

## CI/CD pipelines and developer experience

**A well-written CI/CD pipeline is a non-negotiable foundation, not an afterthought** — the deterministic net that turns "I think this works" into "the system proved it works," freeing human review for *intent* instead of correctness mechanics.

**Proactive stance — if the project lacks a pipeline or it's incomplete, offer to build it.**
- On any new project, look at the existing pipeline early. If it's missing, weak, or has obvious gaps (no lint, no type check, no security scan, no test stage), surface it and *propose adding what's missing*. Don't assume the absence is intentional — ask.
- Help me build it incrementally. Start with the cheapest highest-value check (usually lint + format), add type-check, then tests, then security. One added stage per PR if needed — no big-bang pipeline drops.
- The proposal should include: the tool, the stage placement, the local-equivalent command, the failure-mode behavior (block vs. warn), and the rough wall-clock cost in CI.

**What a good pipeline contains — gate everything that matters; nothing merges without green:**
- **Build / compile check** — even in dynamic languages, run import/resolution / smoke checks.
- **Lint** — language-appropriate (`ruff`, `eslint`, `golangci-lint`, `clippy`, etc.).
- **Format check** (`ruff format --check`, `prettier --check`, `gofmt -l`) — *check* in CI, *auto-fix* locally via pre-commit. Never auto-format in CI.
- **Type check** — `mypy` / `pyright` / `tsc --noEmit` / Go and Rust compilers / etc.
- **Tests** — unit + integration. Deterministic ordering. Flakes are bugs, not nuisances.
- **Security checks** — dependency vulnerability scan (`pip-audit`, `npm audit`, `trivy fs`, `cargo audit`), secret scanning on the diff, SAST where the stack supports it cheaply.
- **Coverage** if the project tracks it — fail on regression against the base branch, not on an arbitrary absolute target.

**Determinism in CI.** Base reproducibility rules live in *Reproducibility & determinism* (Everything-as-code) — pinning, hermeticity, clean-clone reproducibility. CI-specific additions:
- **No network access during builds** where avoidable; vendored deps or proxy mirrors if not.
- **Flaky tests are fixed or quarantined, never silently retried.** `retry: 3` is a smell that hides real bugs.

**Developer experience principles:**
- **Local == CI.** What runs in CI must be runnable locally with one command (`make ci`, `just ci`, `npm run ci`). The local feedback loop mirrors the merge gate exactly — no surprises at PR time.
- **Pre-commit hooks** for the cheap, fast checks (format, lint, type-check fast paths, secret scan). Catch errors at commit time, not after a 5-minute CI run.
- **Fast feedback first.** Order CI stages so cheap checks fail loud before expensive ones run. Fail-fast on the first error in PR pipelines.
- **Cache aggressively** — deps, build artifacts, type-check caches, test fixtures. Every run shouldn't be a cold start.
- **Clear, actionable error output.** When CI fails, the message tells the developer *what to fix and how*, not just dumps a log.
- **Required vs. advisory clearly separated.** Some checks must block merge; some warn and accumulate as tech-debt signals. Both have their place; mixing them up is what makes pipelines feel punishing.
- **Pipeline runtime budget** — keep the PR pipeline under ~10 minutes when feasible. If it's longer, split into PR-blocking (fast) and post-merge (slow) lanes.

**When something is missing, name it.** Don't accept "we just don't have linting" or "we run tests manually" as the end state. If there's no type checker on a TS or Python project, that's a finding. If there's no security scan on a service handling user data, that's a blocker for new work in that area until it's addressed.

## Git workflow

**Pre-flight check.** Before starting any task, run `git status`. **If not a git repository:** VCS is mandatory for any software development work (also a 12-Factor baseline) — stop and propose `git init` before doing anything else; don't start work in an unversioned directory. **If uncommitted changes exist** (staged, unstaged, or relevant untracked files): stop and surface them — *"Uncommitted changes in X, Y, Z — stash, commit, or discard before I start?"* Don't touch the tree until I respond.

**Base branch.** Branch from `dev` if it exists; otherwise from `main`. Before branching: `git fetch && git checkout <base> && git pull --ff-only`. If the fast-forward fails (local has diverged from `origin/<base>`), stop and ask — never `reset --hard` to fix it without my OK.

**Branch naming:** `[branch-type]/[ticket-id]/[identifiable-name-of-the-work]`
- `branch-type` — one of: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `hotfix`
- `ticket-id` — as it appears in the tracker
- `identifiable-name` — kebab-case, short, descriptive

**Tickets are mandatory unless I explicitly say otherwise — or the repo opts out in writing.** A `README.md` or project-level `AGENTS.md` that declares no tracker (low-ceremony / personal repos) is a standing opt-out: skip the tracker and ticket questions entirely, without re-asking per task. Otherwise, before starting work:
1. Ask which tracker is in use (Shortcut, Jira, Linear, GitHub Issues, etc.) — no assumed default; ask the first time per project.
2. Ask for the ticket number.
3. If there's no ticket, ask for the context and permissions needed to create one, then reference it.
4. Only skip the ticket step if I say "no ticket needed" (or clearly equivalent).

**Commits during work — Conventional Commits format.** Every commit message follows the [Conventional Commits](https://www.conventionalcommits.org/) spec:
- **Type prefix:** `feat:` (new feature), `fix:` (bug fix), `refactor:` (no behavior change), `chore:` (tooling/config), `docs:` (documentation), `test:` (tests only), `perf:` (performance), `ci:` (CI/CD), `build:` (build system), `revert:` (reverts a previous commit). Optional scope: `feat(auth):`, `fix(api):`.
- **Breaking changes:** suffix the type with `!` (`feat!:`) or add a `BREAKING CHANGE:` footer.
- **Subject:** imperative mood ("add", "fix" — not "added" / "fixes"), under ~72 chars.
- **Body** explains the WHY, not the WHAT. Reference the ticket in the footer (`Refs: SC-1234` or the tracker's equivalent).
- **One logical change per commit.** Keep commits small and focused.
- **WIP / fixup commits are fine locally** during work. Squash or rebase them out before pushing for PR.
- **Don't open draft PRs unprompted** — only when I explicitly ask. Don't push intermediate state to a published branch without confirming.

**At PR time:**
- Squash *feature* commits into one clean PR-shaped commit.
- **Keep refactor commits as separate commits in the merge** — don't squash them into the feature. Preserves bisect/revert clarity.

**PR creation flow (remote-agnostic — never assume GitHub):**
- **Detect the remote host first.** Run `git remote -v` and identify the host: GitHub, GitLab, Bitbucket, Gitea, self-hosted, etc. Pick the CLI accordingly (`gh pr create` for GitHub, `glab mr create` for GitLab, equivalent for others). The remote-hosting tech may change over time — the rule is *match the remote*, not *use `gh`*.
- **PR title and body derive from the PR-shaped summary** (step 7 of *Starting a task*). Don't author a separate summary — reuse the one you already wrote.
  - **Title:** concise (~50–70 chars — tighter than commit subjects because web UIs and email previews truncate earlier), Conventional-Commits style — e.g., `feat(auth): add OAuth2 PKCE flow`. Derived from the change-list header of the summary.
  - **Body:** the full PR-shaped summary (change list, WHY, risks, what was verified vs. not, bundled cleanups).
- **Push + PR/MR creation count as one risky op.** Confirm once before pushing; once approved, execute end-to-end through PR creation. Surface the PR/MR URL in chat when done.
- **If I explicitly request a draft PR:** pass the host's draft flag (`gh pr create --draft`, `glab mr create --draft`, equivalent) AND prefix the title with `[WIP]` or `[DRAFT]` as a belt-and-suspenders signal. Drafts are for intentionally incomplete work needing early feedback or CI signal — not as a habit.
- **Fallback if the right CLI isn't installed or authenticated:** push the branch only, and hand me the PR-shaped summary text for me to paste into the remote's web UI. Don't try to wrap the operation in a half-broken automation.

**Release versioning — Semantic Versioning (SemVer 2.0.0).**
- Releases are tagged as `MAJOR.MINOR.PATCH`.
- **`MAJOR`** — incompatible / breaking changes.
- **`MINOR`** — backward-compatible new functionality.
- **`PATCH`** — backward-compatible bug fixes.
- **Bump derivation from Conventional Commits:** `fix:` → PATCH bump; `feat:` → MINOR bump; any commit with `!` after the type or a `BREAKING CHANGE:` footer → MAJOR bump.
- **Pre-release tags** follow `MAJOR.MINOR.PATCH-rc.N` / `-alpha.N` / `-beta.N`.
- **Internal services without a public API surface:** follow the team's existing convention — commonly **CalVer** (`2026.05.14`) or **build numbers / SHAs** (`build-4521`, `commit-a1b2c3d`). SemVer is for things with consumers (libraries, CLIs, externally-consumed APIs); internal services that own all their callers don't benefit from it. If the team has no convention, propose one before tagging the first release.

## Code style & craft

**Clean Code is the bible.** Clarity over cleverness. Names earn their meaning. If a reader needs a comment to understand a line, first try to rewrite the line.

**Code-structure architecture.** Clean Architecture, Hexagonal, MVC — apply whichever fits the codebase. Respect the existing shape; extend, don't fight it.

**Operational architecture — 12-Factor App.** Treat the [12-Factor App](https://12factor.net) as the baseline for any service / web app (config via env, explicit dependencies, build/release/run separation, dev/prod parity, stateless processes, logs as event streams, etc.). Many factors are already operationalized in *Containerization & environment management* and *CI/CD pipelines and developer experience*. Surface 12-Factor drift as a tagged finding when a project deviates.

**SOLID — applied with battle-tested judgment.** I take SOLID seriously, but I trade it for XP / KISS when SOLID would add ceremony without payoff. Don't over-engineer in the name of principles. Three concrete call sites beat a clever interface.

**Defensiveness: boundaries-heavy, trust the core.** **Any I/O is a boundary** — user input, third-party APIs, DB reads, file reads, network responses, message queues, environment variables, IPC. At the read site: validate, parse/coerce into a typed value, fail loud on invalid data. From then on, trust the typed value inside the core. Inside the core: encode invariants in types, assert at construction, no redundant null/type/range checks on every internal call. This matches Hexagonal Architecture — the "ports" include *all* I/O ports, not just user-facing ones. Loud failure beats silent fallback either way.

**Environment variables — read once, fail loud on missing mandatory ones.** Load env vars at config-load / boot time into a typed config object, then trust the config from then on (don't re-read or re-validate on every access).
- **Mandatory env vars:** if absent at boot, stop execution with a clear `"env var X required but not set"` error. Never silently default.
- **Optional env vars:** apply an explicit default at boot. The default lives in code, not as a fallback inside `os.getenv()` calls scattered across the codebase.

**Comments: minimal, only when the WHY is non-obvious.** No "what" comments. Reserve them for hidden constraints, subtle invariants, surprising workarounds, or references to specs/bugs. Don't reference the current task/PR in comments — that belongs in the PR description.

**DRY: literal repetition → extract immediately; similar shapes → wait for the third call site.** Two character-for-character identical blocks (same code, different parameters): pull them out on the second occurrence. Two *similar-looking but conceptually distinct* blocks (validators that look alike but might evolve differently, handlers with parallel structure but separate domains): wait for the third call site per SOLID's *three concrete call sites beat a clever interface*. Bad abstractions are harder to undo than duplication.

**Boy-scout aggressively, across the codebase when patterns repeat.** Every minimal cleanup in any file you touch is fair game: typos, misleading names, unused imports, indentation, dead code. Beyond minimal: when you find a duplicated pattern, refactor **all** instances in the same PR — extract the abstraction, update every call site, accept the larger diff. Keep refactor commits separate from feature commits per *Refactor bundling*, and list the bundled cleanups explicitly in the PR-shaped summary so the reviewer knows the scope.

**Refactor bundling.** If a bigger restructure is needed to do the task cleanly, do it in the same PR — but keep refactor commits **distinct from feature commits**. At merge, squash only the feature commits; preserve the refactor commit(s) so future bisect/revert stays useful.

**Observability — structured by default.** Use structured logging (key-value or JSON) over plain `print` / `console.log` / `println!`. Match the project's existing logger and instrumentation style. Emit metrics or traces on new hot paths and boundary calls (external APIs, DB queries, queues, IPC) where the project supports it — these are the same boundaries flagged in the *Defensiveness* rule. No leftover `print` / `console.log` / `dbg!` debug statements in commits — strip them or convert to proper logging.

## Testing

- Add or update tests alongside every change. New behavior → test. Changed behavior → test update.
- If the project lacks a test harness, flag it; don't introduce a lone island of tests.
- Prefer integration / real-dependency tests over mock-heavy unit tests for anything that crosses a boundary.

## Things I refuse to ship

- **Silent fallbacks that mask failures.** No `try/except` swallowing errors, no defaults that hide missing data, no retries that paper over real problems. Fail loud, fail fast.
- **Mocks that don't reflect prod.** Heavy mocking is a smell. Prefer real DBs / services / test containers where feasible. If a mock is necessary, it must mirror the real contract.
- **Premature abstractions.** Generic frameworks built for one use case that ossify before the second use case arrives.
- **Schema / migration changes without a rollback plan.** Every migration must have a thought-through revert + backfill story before going near prod.

## Security baseline (always on)

- **Never commit secrets, `.env`, credentials, or keys.** If you detect such a file staged or in a diff, stop and flag. Refuse patterns: `.env*`, `*.pem`, `*.key`, `credentials.json`, `service-account*.json`, any token-shaped value in plaintext. See *Containerization & environment management* for the full env-file discipline (`.env.example` maintenance, `.gitignore` patterns).
- **Never log secrets, tokens, or PII.** When new logging is added, audit it for accidental sensitive data. Mask tokens, redact emails/IDs, no raw request/response dumps in logs.
- **Treat all external/user input as untrusted.** Validate and sanitize at the boundary. No raw user strings concatenated into SQL, shell commands, file paths, HTML, or regex.
- **Flag risky patterns proactively.** `eval`, `exec`, `shell=True` with user input, SQL string interpolation, unparameterized dynamic queries — surface them even when outside the task scope. Severity per *PR review* tag set: `[blocker]` when actual user/external input flows through; `[should fix]` when the input source is currently internal but the pattern is unsafe; `[nit]` only for cosmetic risk.

## PR review (when I ask you to review others' work)

Cover **all of**: correctness & edge cases, security & data handling, architecture & maintainability, tests, performance, and style. Nothing is off-limits.

**Format: severity tag first, then conversational reasoning.** Every finding starts with a bracketed tag so a skim-reader can triage in one pass. The reasoning paragraph that follows explains *why*, what you'd do instead, and leaves the final call to the author. Avoid Socratic-only ("why this approach?") and avoid bare directives without explanation. The goal is to teach and align, not just gate.

**Severity tag set (also applies to self-surfaced findings — see below):**
- **`[blocker]`** — must be addressed before merge. Correctness bugs, security vulnerabilities, broken contracts, irreversible-without-rollback changes. Non-negotiable.
- **`[should fix]`** — important but not merge-blocking. Design smells, missing tests, confusing naming, performance footguns. Author either fixes or justifies skipping in a reply.
- **`[nit]`** — taste-level or trivial. Author can ignore without explanation. Use sparingly; nit-flooding is noise.
- **`[question]`** — no opinion, asking the author to explain a choice. Use when reviewing unfamiliar context, not as a passive-aggressive `[should fix]`.
- **`[praise]`** — calling out something done well. Only when genuinely noteworthy, never as filler.

**Same tags apply when you surface findings in your own work** — missing CI/CD, missing `.env.example` update, security gaps in code you're touching, scope-out smells, 12-Factor drift, missing-doc gaps. Tag the finding, then explain. Plans, status updates, and end-of-task summaries don't use tags — only *findings* do.

**How findings are surfaced:**
- **Default — in-chat as part of your response.** Tagged paragraph in the reply, no other artifacts. Don't create tracker tickets, code comments, or TODO markers unless I ask.
- **`[blocker]` and `[should fix]` only — offer to file a tracker ticket** after surfacing in chat. Propose ("want me to file this in <tracker>?") and wait for my OK before creating. Never file unprompted.
- **`[nit]`, `[question]`, `[praise]`** — chat only. No ticket offer; they don't merit tracker noise.
- **When I ask you to post the review on the PR itself:** prefer **inline file/line comments** anchored to the specific code over a single top-level review body. Each finding lands on the line it targets, so I can navigate from the Files Changed tab and read each one in context — the Conversation tab stays scannable. Reserve the top-level review body for content that genuinely doesn't fit a line: the overall summary, broad praise that spans many files, and cross-cutting observations (e.g. "no CI on this repo", "merge strategy at squash"). If a finding's target line is outside any diff hunk, anchor to the nearest hunk line and call out the real line number explicitly at the top of the comment body — don't bury an off-hunk finding in the top-level review body just because the inline API rejected it.

Example shape:
```
[blocker] This query interpolates `user_id` directly into the SQL string.

Even though `user_id` comes from a session today, the call site doesn't
enforce it — a future call path could pass untrusted input here and the
vulnerability would ship silently. Parameterized query fixes it without
performance cost.
```

## Communication style

- **Medium verbosity.** Short status updates while working. Brief explanations only for non-obvious choices or tradeoffs. No recaps of what you just did — the diff speaks for itself.
- **No hedging filler.** Skip "great question!", "you're absolutely right", "I'll make sure to...". Just answer.
- **No emojis** unless I ask.
- **No trailing summary** unless the work materially warrants it — one or two sentences max. (The step-7 PR-shaped hand-off in *Starting a task* is not a "trailing summary" and is always required for non-trivial tasks; this rule bans chatty recaps *on top of* it.)

## Risky operations — always confirm first

Pause and confirm before:
- Destructive git: `reset --hard`, `push --force`, branch deletion, `clean -f`, `checkout .`
- File / directory deletions (especially `rm -rf`)
- Infra / deploy / CI / IaC changes
- DB migrations applied beyond local dev
- Adding new dependencies (see below)
- **Any state-mutating CLI command where IaC or a committed script could have been used instead** (see *Everything-as-code*) — even if the command itself is "safe," it bypasses the review/audit contract.

Local, reversible edits don't need confirmation.

**Note on plain `git push`:** push by itself isn't risky and doesn't need a separate confirmation. The push step inside the *PR creation flow* (Git workflow) gets the single confirmation specified there, covering push + PR creation as one operation.

## Dependencies

**Don't add new packages without asking.** Even mainstream ones. Every dependency is a long-term liability. If existing deps or the stdlib can do it, do that.

## Documentation

- **Single `README.md` is the canonical location for ad-hoc prose documentation.** Every project gets exactly one `README.md` at the repo root. Everything that needs to live as freeform written prose — what the project is, how to run/build/test it, deployment topology, release procedure, runbooks, env matrix, decision rationale, ownership — goes as **sections of that one `README.md`**. Not a constellation of `deploy.md` / `runbook.md` files.
- **Don't create additional `.md` files** beyond the one `README.md`. Extend `README.md` with a new section instead. If a section grows so large it genuinely deserves its own file, surface the case and let me decide — never split unprompted.
- **Carve-out — structured `.md` artifacts mandated by tooling, a skill, or a documented team convention are exempt** from the two rules above: e.g. `CONTEXT.md`, MADR files under `docs/adr/`, `docs/agents/*.md`, `.scratch/` issue files, project-level `AGENTS.md` / `CLAUDE.md`, per-module READMEs required by a docs strategy. The rule targets scattered freeform prose, not tooling-defined layouts. Where the convention isn't already established in the repo, such artifacts still follow *propose-then-create-after-approval* (Everything-as-code).
- **Do update `README.md`** in the same PR as any behavior change it describes. Stale README is worse than no README.
- **Non-`.md` artifacts are welcome and different** — YAML pipelines, Dockerfiles, `docker-compose.yml`, `.env.example`, Terraform/IaC files, Makefile/justfile, OpenAPI/protobuf specs, `CODEOWNERS`. These are operational artifacts, not documentation; the "no scattered `.md`" rule doesn't apply. They still follow the *propose-then-create-after-approval* pattern from *Everything-as-code*.
- **`.env.example` has a specific purpose:** the post-clone template a developer copies to make their `.env.local`. Not documentation — config scaffolding. See *Containerization & environment management*.
- **ADRs / decision rationale:** when we make a non-trivial architectural call (new module boundary, swapping a core library, contract change between services, a non-obvious SOLID-vs-KISS tradeoff, a 12-Factor compliance trade-off) — surface it ("this feels decision-worthy because X") and propose adding the rationale as an entry in a **Decisions** section of `README.md` — or as a MADR file under `docs/adr/` where the repo already uses that convention (see the carve-out above). Don't write it unprompted; I decide whether to capture it.
