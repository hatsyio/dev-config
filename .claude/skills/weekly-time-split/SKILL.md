---
name: weekly-time-split
description: Use when Josep has to say where his contracted week went — the Friday timesheet run, a past week he still has to fill in, or "help me distribute my hours" for a day or two of the current week. Also fires from the launchd job on Friday afternoons.
---

# Weekly time split

Turn a week of digital traces into a per-repo split of Josep's contracted hours.

**Core principle: every hour is either evidenced or named as residual.** Josep reads the split to imputar horas, so an inferred hour that reads like an observed one is worse than an admitted gap. Inference is allowed and expected — labelling it is mandatory.

## The week

Monday to Friday, Europe/Madrid. Default target: **8,5 h Monday–Thursday, 6 h Friday = 40 h**.

Ask only if the calendar shows an out-of-office or holiday event inside the week — then confirm the reduced target before splitting. Otherwise assume the default and say so.

Default range: the current week when invoked on a Friday, the last complete week otherwise. A request naming specific days ("lunes y martes de esta semana") splits only those days, at their per-day target.

## Step 1 — Collect

Run the local half first, then the connectors in parallel:

```bash
~/.claude/skills/weekly-time-split/scripts/collect-local-evidence.sh <monday YYYY-MM-DD>
```

It prints commits authored, PRs created, PRs that moved, reviews submitted inside the week, comments written inside the week, and Claude Code active time per project per day.

Then, in one batch:

| Source | Call | What it settles |
|---|---|---|
| Calendar | `list_events` over Mon 00:00 → Sat 00:00 | The only hard hours in the week |
| Slack | `slack_search_public_and_private`, `from:<@U03PVCQ350T>`, sorted by timestamp | Afternoons that left no commit; page until the Monday |
| Gmail | `search_threads`, `in:sent after:… before:…` | Client-facing work, usually the quiet days |
| Shortcut | `stories-search` with `owner: me`, `updated: <range>` | Ticket-level framing; thin for a lead, don't force it |

## Step 2 — Attribute

One row per repo. Meetings and coordination that belong to no repo get their own rows: **Interno CSS / backend** (team meetings, dailies, 1:1s) and **Sin traza** (the residual).

- Count a calendar event only if Josep accepted it. Declined events and reminder-only events ("It's 10K time!") are zero. Overlapping meetings count once — take the union of the clock time.
- A repo earns hours from commits, reviews submitted, comments written, Claude session time, or a Slack thread about it. A PR appearing in "PRs that moved" because someone else pushed is not evidence.
- Work spills across midnight boundaries: commits landing at 09:00 Monday usually mean Friday afternoon work, and a day whose commits stop at noon often continues locally. Bridge those gaps and label the bridge as inference.
- Personal repos (`hatsyio/*`: dev-config, atiny-world) stay out of the split. Name them once in a `[question]` so Josep can overrule.
- Give the residual to **Sin traza** rather than to the day's dominant repo. Guessing which client owns an unlogged hour is exactly the error that corrupts a timesheet.

## Step 3 — Report

Answer in chat, in Spanish, in this order:

1. **One line on the calendar**: which meetings counted, which were dropped and why.
2. **The table**: repo rows × day columns, with a total column and, for a full week, a percentage column. Day columns must sum to their target; the grand total must equal the week target. Verify this arithmetic before printing.
3. **A paragraph per day**, naming the concrete evidence with timestamps — commits and their hours, review approvals, the Slack conversation that carried the afternoon. This is what lets Josep correct a number he disagrees with.
4. **Findings**, tagged per his AGENTS.md: `[should fix]` for every gap where hours rest on inference, `[question]` for attribution he has to decide.
5. **A running total** when the week is partial.

## Gotchas that produce wrong numbers

| Trap | What actually happens |
|---|---|
| `gh search prs --reviewed-by=@me --updated=<week>` | Returns PRs *updated* in the week, reviewed whenever. Always re-check `submitted_at` per review. |
| Session file mtime in `~/.claude/projects` | Resuming a session touches the file without adding messages. Only in-file message timestamps count — the script already does this. |
| `git log --all` without an author filter | Other people's merge commits land on his branches and look like his work. |
| `for x in $var` in zsh | zsh does not word-split unquoted variables. Use `printf '%s\n' … | while read`. |
| A quiet day in the traces | Means the traces missed it, not that he did nothing. Meetings, browser review and Cursor leave no trace here. |
| Slack tool name under launchd | A headless run resolves Slack as the claude.ai connector, not the plugin: `mcp__claude_ai_Slack__slack_search_public_and_private`. The plugin name is denied there, and without Slack the residual roughly doubles. |

## Identities

git `jpascual@cartodb.com` · GitHub `hatsyio` (personal and CartoDB work both) · Slack `U03PVCQ350T` · Shortcut `joseppascualbadia` · repos under `~/Workspace`.
