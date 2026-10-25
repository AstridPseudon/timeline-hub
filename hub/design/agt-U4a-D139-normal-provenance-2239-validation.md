# U4a / PLAN3 / D139 validation

## Scope

- Agent base: `cd63be424d62226e3ee5c26fc5ce03227f5394a5`.
- Runtime producer: `/home/user/work/runtime`.
- Runtime HEAD before and after: `f103bb46866999c961a8865636f2e66d544e0c9b` -> `f103bb46866999c961a8865636f2e66d544e0c9b`.
- Runtime tree after: `5d0cedf2e5134acf895e8d43191cc5fdc09f9883`.
- Runtime producer clean before and after: `PASS`.
- Independent Runtime D139 result: 1,571 passed, 0 failed/error/skipped, raw exit 0; this is provenance context only, not a new test run here.

## Canonical 15 and schema/config gate

- Existing Agent lock before adoption: source `ab1e4f6141987706132916e2da16477f5a019464`.
- Canonical source/mapping/hash rows: `canonical15.json`.
- All 15 mappings unchanged: `PASS`.
- All 15 Agent baseline bytes equal post-refresh bytes: `PASS`.
- All 15 post-refresh bytes equal Runtime producer bytes: `PASS`.
- All 15 lock hashes match current bytes and producer hashes: `PASS`.
- `astrid/core/timeline/schema/timeline-config.schema.json` source bytes: exact before/after/producer equality, `PASS`.
- Producer manifest `contract/artifacts.json`: exact committed/current metadata and all 15 selected source hashes, `PASS`.

## Normal commands

1. `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/runtime` — `PASS`; refreshed from `f103bb46866999c961a8865636f2e66d544e0c9b`.
2. `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime` — `PASS`; lock matches producer manifest.
3. `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — `PASS`; `artifacts.json is current`.
4. `git diff --check` — `PASS`.

## Diff boundary

- Tracked diff: `runtime.lock.json` only.
- Lock-only change: `source_commit` `ab1e4f6141987706132916e2da16477f5a019464` -> `f103bb46866999c961a8865636f2e66d544e0c9b`.
- Entire tree outside `runtime.lock.json` equals the pre-refresh Agent baseline: `PASS`.
- No product, HTTP, body, full-suite, old-control, package-acquisition, or generated-source write was made.
