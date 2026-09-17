#!/usr/bin/env python3
"""Active time per project from the Claude Code session logs.

Every message timestamp lands in a 5-minute bucket; the bucket count per
project per day is the active time. File mtimes are not usable here: resuming a
session touches the file without adding messages, so mtime reports work on a day
where none happened. Only in-file timestamps count.

Usage: claude-active-time.py <start YYYY-MM-DD> <end YYYY-MM-DD>   # end exclusive
"""
import collections
import datetime
import os
import re
import sys

BASE = os.path.expanduser("~/.claude/projects")
LOCAL_OFFSET = datetime.timedelta(hours=2)  # Europe/Madrid in CEST
TS = re.compile(rb'"timestamp":"(20\d\d-\d\d-\d\dT[\d:.]+Z)"')


def parse(raw: bytes):
    text = raw.decode()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.datetime.strptime(text, fmt).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
    return None


def main() -> None:
    start = datetime.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=datetime.timezone.utc) - LOCAL_OFFSET
    end = datetime.datetime.fromisoformat(sys.argv[2]).replace(tzinfo=datetime.timezone.utc) - LOCAL_OFFSET

    per_day = collections.defaultdict(lambda: collections.defaultdict(set))
    for root, _, files in os.walk(BASE):
        for name in files:
            if not name.endswith(".jsonl"):
                continue
            try:
                raw = open(os.path.join(root, name), "rb").read()
            except OSError:
                continue
            project = os.path.relpath(root, BASE).split(os.sep)[0]
            for match in TS.findall(raw):
                moment = parse(match)
                if moment and start <= moment < end:
                    day = (moment + LOCAL_OFFSET).strftime("%a %d")
                    per_day[project][day].add(int(moment.timestamp() // 300))

    rows = []
    for project, days in per_day.items():
        hours = sum(len(b) for b in days.values()) * 5 / 60
        spread = {d: round(len(b) * 5 / 60, 1) for d, b in sorted(days.items(), key=lambda kv: kv[0][4:])}
        rows.append((hours, project, spread))
    if not rows:
        print("(no Claude Code sessions in range)")
    for hours, project, spread in sorted(rows, reverse=True):
        print(f"{hours:5.1f} h | {project.replace('-Users-joseppascualbadia-', '')} | {spread}")


if __name__ == "__main__":
    main()
