#!/usr/bin/env python3
"""Print the weekly split table from attributed hours.

stdin: {"targets": {"YYYY-MM-DD": hours, ...},
        "rows": [{"repo": str, "day": "YYYY-MM-DD", "hours": number}, ...]}

The remainder of each day's target goes to "Sin traza". Exits non-zero when a
row falls outside the targets or a day's attributed hours exceed its target.
"""

import json
import sys
from collections import defaultdict

RESIDUAL = "Sin traza"
FULL_WEEK_DAYS = 5


def fmt(hours: float) -> str:
    return f"{hours:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def main() -> None:
    data = json.load(sys.stdin)
    targets = {day: float(h) for day, h in data["targets"].items()}
    days = sorted(targets)
    cells: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in data["rows"]:
        if row["day"] not in targets:
            sys.exit(f"{row['repo']}: day {row['day']} is outside the targets")
        if row["repo"] == RESIDUAL:
            sys.exit(f"do not pass '{RESIDUAL}' rows; the script computes the residual")
        cells[row["repo"]][row["day"]] += float(row["hours"])

    for day in days:
        attributed = sum(repo_cells[day] for repo_cells in cells.values())
        if attributed > targets[day] + 1e-9:
            sys.exit(
                f"{day}: attributed {fmt(attributed)} h exceeds the {fmt(targets[day])} h target"
            )
        cells[RESIDUAL][day] = targets[day] - attributed

    week = sum(targets.values())
    with_pct = len(days) == FULL_WEEK_DAYS
    header = ["Repo", *days, "Total", *(["%"] if with_pct else [])]
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for repo in [*sorted(r for r in cells if r != RESIDUAL), RESIDUAL]:
        total = sum(cells[repo][d] for d in days)
        pct = [f"{100 * total / week:.0f} %"] if with_pct else []
        print(
            "| "
            + " | ".join([repo, *(fmt(cells[repo][d]) for d in days), fmt(total), *pct])
            + " |"
        )
    pct = ["100 %"] if with_pct else []
    print(
        "| "
        + " | ".join(["**Total**", *(fmt(targets[d]) for d in days), fmt(week), *pct])
        + " |"
    )


if __name__ == "__main__":
    main()
