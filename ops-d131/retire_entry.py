#!/usr/bin/env python3
"""Private manager wrapper for one authenticated bench-store retirement."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import bench_store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--tests-dir', required=True)
    parser.add_argument('--entry', required=True)
    parser.add_argument('--authorization', required=True)
    parser.add_argument('--now')
    args = parser.parse_args()
    try:
        authorization = json.loads(bench_store.read(Path(args.authorization)))
        receipt = bench_store.Store(args.root, args.tests_dir).retire_entry(
            args.entry, authorization, now=args.now)
        print(bench_store.canonical(receipt))
        return 0
    except (bench_store.Refused, OSError, ValueError, TypeError, KeyError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
