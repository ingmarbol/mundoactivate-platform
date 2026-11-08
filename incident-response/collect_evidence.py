#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Collect local synthetic evidence without modifying the source")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    destination = output / source.name
    shutil.copy2(source, destination)
    manifest = {
        "case_id": args.case_id,
        "collected_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_name": source.name,
        "evidence_name": destination.name,
        "sha256": sha256(destination),
        "size_bytes": destination.stat().st_size,
        "collector": "training-lab",
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"EVIDENCE {destination}")
    print(f"SHA256 {manifest['sha256']}")
    print(f"MANIFEST {manifest_path}")


if __name__ == "__main__":
    main()

