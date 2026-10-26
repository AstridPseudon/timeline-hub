#!/usr/bin/env python3
"""Receive a completed D141 P5 service result without launching it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = (
    "exit", "argv.json", "module-origin.json", "source-hashes.json",
    "start.json", "stop.json", "disk.json", "d141-p5-cut.xml", "KEEP",
)


def receive(output: Path, receipt: Path) -> None:
    if not output.is_absolute() or not output.is_dir() or output.is_symlink():
        raise ValueError("service output must be an absolute regular directory")
    missing = [name for name in REQUIRED if not (output / name).is_file()]
    if missing:
        raise ValueError("missing durable service artifacts: " + ", ".join(missing))
    exit_text = (output / "exit").read_text().strip()
    if exit_text not in {str(value) for value in range(256)}:
        raise ValueError("runner exit is not a numeric byte")
    argv = json.loads((output / "argv.json").read_text())
    if not isinstance(argv, list) or not all(isinstance(part, str) for part in argv):
        raise ValueError("durable argv must be a string list")
    if not (output / "d141-p5-cut.xml").read_text().lstrip().startswith("<?xml"):
        raise ValueError("durable JUnit is not XML")
    if receipt.exists() and receipt.read_bytes() != b"":
        raise ValueError("receipt destination already exists")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps({
        "route": "d141-p5-cut",
        "output": str(output),
        "runner_exit": int(exit_text),
        "argv": str(output / "argv.json"),
        "module_origin": str(output / "module-origin.json"),
        "source_hashes": str(output / "source-hashes.json"),
        "start": str(output / "start.json"),
        "stop": str(output / "stop.json"),
        "disk": str(output / "disk.json"),
        "junit": str(output / "d141-p5-cut.xml"),
        "keep": str(output / "KEEP"),
    }, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receive(args.output, args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
