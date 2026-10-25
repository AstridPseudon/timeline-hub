#!/usr/bin/env python3
"""Receive a completed Runtime full-service result without launching it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ("exit", "log.txt", "runtime-full.xml", "KEEP")


def receive(output: Path, receipt: Path) -> None:
    if not output.is_absolute() or not output.is_dir() or output.is_symlink():
        raise ValueError("service output must be an absolute regular directory")
    missing = [name for name in REQUIRED if not (output / name).is_file()]
    if missing:
        raise ValueError("missing durable service artifacts: " + ", ".join(missing))
    exit_text = (output / "exit").read_text().strip()
    if exit_text not in {str(value) for value in range(256)}:
        raise ValueError("runner exit is not a numeric byte")
    junit = output / "runtime-full.xml"
    if not junit.read_text().lstrip().startswith("<?xml"):
        raise ValueError("durable JUnit is not XML")
    if receipt.exists() and receipt.read_bytes() != b"":
        raise ValueError("receipt destination already exists")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(
            {
                "output": str(output),
                "runner_exit": int(exit_text),
                "junit": str(junit),
                "log": str(output / "log.txt"),
                "keep": str(output / "KEEP"),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receive(args.output, args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
