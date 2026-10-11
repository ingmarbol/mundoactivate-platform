#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--state", required=True)
parser.add_argument("--dlq", required=True)
args = parser.parse_args()

state_path = Path(args.state)
processed = json.loads(state_path.read_text()) if state_path.exists() else {}
counts = {"processed": 0, "duplicate": 0, "dlq": 0}

with Path(args.input).open() as source, Path(args.dlq).open("a") as dlq:
    for line in source:
        event = json.loads(line)
        event_id = event.get("id")
        if not event_id or not event.get("type") or not event.get("source"):
            dlq.write(json.dumps({"reason": "invalid-schema", "event": event}) + "\n")
            counts["dlq"] += 1
            continue
        if event_id in processed:
            print("DUPLICATE", event_id)
            counts["duplicate"] += 1
            continue
        print("PROCESSED", event_id, event["type"])
        processed[event_id] = {"status": "completed", "type": event["type"]}
        counts["processed"] += 1

temporary = state_path.with_suffix(".tmp")
temporary.write_text(json.dumps(processed, indent=2, sort_keys=True) + "\n")
temporary.replace(state_path)
print(json.dumps(counts, sort_keys=True))
