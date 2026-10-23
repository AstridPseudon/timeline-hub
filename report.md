# P4 ten-note reader source port

## Result

Prepared the bounded P4 test-only source port on owner-fix base
`47aa77266f2287ad14519b07ce0bba7d4bba2170` (parent
`31a5e8d3c858d0e4cb1b333b95175862f07f5fa6`). Only the code path
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py` changed; this file
is the required worker report. The test's final
blob exactly matches donor `b8163c059a633af4b15836ab974188f6ed2fd398`:
`cdb186d001fe8bd7476c2a059ee65e9a312dbec5`.

The candidate tree with that one unstaged file is
`d06db493c0f671f4c072af882ce43f7aa008f88b`. No donor product, report, helper,
schema, generated-client, lock, fixture, or launcher ancestry was imported.

The port retains the authentic 69-byte PNG ingest/hash, exhaustive media
mapping, two occurrences to one physical `chapter-shot`/`shot-1`,
`chapter-1`/`internal-1` closure, distinct working aliases, and the existing
ten-note one-commit, per-step undo/redo, mirror, full-closure, show/history,
restart, receipt, publisher, request/response, conflict, and rerun assertions.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — **PASS**, 1 test collected. Existing warning: app2-native pytest lacks the configured `timeout` option.
- `RUFF_CACHE_DIR=/tmp/w-64efbed334/ruff-cache /root/.local/bin/ruff check tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — **PASS**.
- `MYPY_CACHE_DIR=/tmp/w-64efbed334/mypy-cache PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — **PASS**, no issues.
- `git diff --check` — **PASS**.
- Outside-base proof: `git diff --quiet HEAD -- . ':(exclude)tests/editing_conformance/test_p4_ten_note_v2_runtime.py'` — **PASS**; only the named test is modified.
- Retained normal Runtime pin: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Retained edit-command schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Retained owner-fix reader blob: `astrid/sdk/_remote_timeline.py` Git blob `60b373bb920456514be2e0fa05a93a5a6483d7c9`; its `RemoteTimelines.open_bundle` production path resolves the authenticated canonical internal owner before `get_project_timeline_revision`.
- Retained public `TimelineSession` blob: `astrid/sdk/timeline/sync.py` Git blob `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b`.

## Limits and next step

This is **SOURCEPREP only**, not an integration merge candidate. No HTTP,
socket, service/body execution, full suite, browser, build, or original-node
run was performed. Independent owner review of this exact port remains
required before running the existing P4-v2 HTTP nodes. No base/test
incompatibility was found during collection or static checks.
