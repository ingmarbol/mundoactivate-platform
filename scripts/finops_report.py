#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from pathlib import Path
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--budget", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

budget = yaml.safe_load(Path(args.budget).read_text())
rows = list(csv.DictReader(Path(args.input).open()))
required = budget["allocation"]["requiredDimensions"]
totals = {dimension: defaultdict(float) for dimension in required}
total = allocated = 0.0

for row in rows:
    cost = float(row["cost_usd"])
    total += cost
    if all(row.get(dimension, "").strip() for dimension in required):
        allocated += cost
    for dimension in required:
        totals[dimension][row.get(dimension) or "unallocated"] += cost

monthly_budget = float(budget["monthlyBudgetUsd"])
active_students = int(budget["businessUnits"]["activeStudents"])
coverage = (allocated / total * 100) if total else 0
unit_cost = (total / active_students) if active_students else 0

lines = [
    "# FinOps baseline",
    "",
    f"- Total cost: USD {total:.2f}",
    f"- Budget consumed: {total / monthly_budget * 100:.1f}%",
    f"- Budget variance: USD {monthly_budget - total:.2f}",
    f"- Allocation coverage: {coverage:.1f}%",
    f"- Cost per active student: USD {unit_cost:.2f}",
]
for dimension, values in totals.items():
    lines.extend(["", f"## Cost by {dimension}"])
    lines.extend(f"- {key}: USD {value:.2f}" for key, value in sorted(values.items()))
Path(args.output).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
