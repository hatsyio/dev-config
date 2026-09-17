#!/usr/bin/env bash
# Collect the local half of the weekly time-split evidence: git commits,
# GitHub authoring/review activity and Claude Code active time.
# The calendar, Slack, Gmail and Shortcut halves are MCP calls, see SKILL.md.
#
# Usage: collect-local-evidence.sh <monday YYYY-MM-DD> [workspace-dir]
set -euo pipefail

MONDAY="${1:?usage: collect-local-evidence.sh <monday YYYY-MM-DD> [workspace-dir]}"
WORKSPACE="${2:-$HOME/Workspace}"
GH_LOGIN="${WEEKLY_GH_LOGIN:-$(gh api user -q .login)}"

# Saturday 00:00 is the exclusive upper bound of the working week.
SATURDAY=$(date -j -f "%Y-%m-%d" -v+5d "$MONDAY" "+%Y-%m-%d")
FRIDAY=$(date -j -f "%Y-%m-%d" -v+4d "$MONDAY" "+%Y-%m-%d")

echo "# Week $MONDAY .. $FRIDAY (github login: $GH_LOGIN)"

echo
echo "## Commits authored in $WORKSPACE"
for repo in "$WORKSPACE"/*/; do
  [ -d "$repo/.git" ] || continue
  # --all catches work that never reached the default branch; the author filter
  # keeps other people's merge commits out.
  log=$(git -C "$repo" log --all --since="$MONDAY" --until="$SATURDAY" \
        --author="$GH_LOGIN\|Josep\|jpascual" \
        --pretty=format:'%ad|%s' --date=format:'%a %d %H:%M' 2>/dev/null || true)
  [ -n "$log" ] && { echo "### $(basename "$repo")"; echo "$log"; echo; }
done

echo "## PRs I authored (created this week)"
gh search prs --author=@me --created="$MONDAY..$FRIDAY" --limit 50 \
  --json repository,number,title,createdAt 2>/dev/null \
  | jq -r '.[] | "\(.createdAt[0:10]) | \(.repository.nameWithOwner)#\(.number) | \(.title)"' | sort

echo
echo "## PRs that moved with me involved"
gh search prs --involves=@me --updated="$MONDAY..$FRIDAY" --limit 60 \
  --json repository,number,title,author,updatedAt 2>/dev/null \
  | tee /tmp/wts-involved.json \
  | jq -r '.[] | "\(.updatedAt[0:16]) | \(.repository.nameWithOwner)#\(.number) | \(.author.login) | \(.title[0:65])"' | sort

# A PR can appear above because someone else pushed to it. Only a review or a
# comment with a timestamp inside the week is evidence that I spent time on it.
REPOS=$(jq -r '.[].repository.nameWithOwner' /tmp/wts-involved.json 2>/dev/null | sort -u)

echo
echo "## Reviews I submitted inside the week"
gh search prs --reviewed-by=@me --updated="$MONDAY..$FRIDAY" --limit 60 \
  --json repository,number 2>/dev/null \
  | jq -r '.[] | "\(.repository.nameWithOwner) \(.number)"' > /tmp/wts-reviewed.txt
while read -r r n; do
  [ -z "${r:-}" ] && continue
  gh api "repos/$r/pulls/$n/reviews" --paginate 2>/dev/null \
    | jq -r --arg r "$r" --arg n "$n" --arg a "$GH_LOGIN" --arg s "$MONDAY" --arg e "$SATURDAY" \
        '.[] | select(.user.login==$a) | select(.submitted_at >= $s and .submitted_at < $e)
             | "\(.submitted_at[0:16]) | \($r)#\($n) | \(.state)"'
done < /tmp/wts-reviewed.txt | sort

echo
echo "## Comments I wrote inside the week"
for r in $REPOS; do
  for kind in pulls issues; do
    gh api "repos/$r/$kind/comments?since=${MONDAY}T00:00:00Z&per_page=100" --paginate 2>/dev/null \
      | jq -r --arg r "$r" --arg k "$kind" --arg a "$GH_LOGIN" --arg e "$SATURDAY" \
          '.[] | select(.user.login==$a) | select(.created_at < $e)
               | "\(.created_at[0:16]) | \($r) | \($k) | \(.html_url)"'
  done
done | sort

echo
echo "## Claude Code active time (5-minute buckets, Europe/Madrid)"
python3 "$(dirname "$0")/claude-active-time.py" "$MONDAY" "$SATURDAY"
