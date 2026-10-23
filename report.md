# P4 physical-boundary oracle adaptation

## Result

Adapted only the initial shared-identity oracle in
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.

Source basis: commit
`3696239c48f9705568af30f2704855cc6a9175e5`, tree
`94f7f4ff4d60a798d9cd664638a2b182234ad82c`. The edited test blob is
`cdb186d001fe8bd7476c2a059ee65e9a312dbec5`.

The old assertion incorrectly required the two WORKING occurrence aliases to
have equal `shot_id` values. The corrected oracle follows C0c's equivalent
stronger physical rule: both authored occurrences resolve through the
authenticated canonical closure to exactly one physical `chapter-shot/shot-1`
and exactly one `chapter-1/internal-1`. It also proves:

- occurrence order, timing, source offsets, tracks, speed, and opaque fields;
- all three authored media references resolve to one manifest media pin;
- shot/internal reference edges, payload digests, and sorted manifest entries;
- the complete canonical document shape and opaque parent/shot/internal fields;
- each occurrence-specific WORKING alias resolves through the authenticated
  `source_mapping`, with no guessed identity or edge rewrite.

The original fixture's shared physical meaning is retained. The ten-note,
one-commit, per-step undo/redo, mirrors, show/history, restart, publisher,
request/base-pair/label/steps/reads, merge, accepted/merged/conflict/invalid,
and full authored-closure assertions remain unchanged.

## Checks

All checks were offline and targeted; the integration test body was not run.

Exact collection command:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$WORKER_TMP" PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
```

The scoped Ruff, private mypy, and whitespace commands were run against the
target and the five-file private mypy scope, using the worker-owned `$WORKER_TMP`
cache path.

- Exact collection command: **PASS**, 1 test collected (existing unknown
  `timeout` configuration warning).
- Scoped Ruff on the target test: **PASS**.
- Private mypy on the target plus `commit.py`, `commit_session.py`, `emitter.py`,
  and `sync.py`: **PASS**, no issues in 5 files (two existing unchecked-body
  notes).
- `git diff --check`: **PASS**.
- Offline actual `bundle_from_document` physical-mapping witness from the
  authentic canonical genesis: **PASS**. It confirmed two distinct working
  aliases, one physical shot/internal tuple, one media pin, and matching
  payload digests.

Not run: HTTP, sockets, Runtime service calls, test body, central test service,
full suite, browser, build, or live readback/inverse evidence.

## Known boundary

The independent review confirmed the remaining production seam is Agent-owned:
the remote reader requests `internal-1` under parent timeline `film`, while
the authenticated canonical internal image is owned by `chapter-1`. This task
does not modify that caller, retarget the source, rewrite edges, or claim live
P4 acceptance. Owner-read repair and a later current-source test-only import
remain required before running the body.
