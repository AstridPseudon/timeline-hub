# P4 ten-note reader source port — source preparation

## Result

Prepared the exact P4 test-only port from donor commit
`b8163c059a633af4b15836ab974188f6ed2fd398`, donor blob
`cdb186d001fe8bd7476c2a059ee65e9a312dbec5`, on Agent owner-fix base
`47aa77266f2287ad14519b07ce0bba7d4bba2170` (parent
`31a5e8d3c858d0e4cb1b333b95175862f07f5fa6`).

The only changed code path is
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`; the candidate
tree is `d06db493c0f671f4c072af882ce43f7aa008f88b`. The worker report is the
required additional handoff artifact. No donor product/report/
helper ancestry, generated client, schema, lock, fixture, or launcher change
was imported. The source retains the authentic 69-byte PNG and digest,
exhaustive media mapping, one physical chapter source closure for two
occurrences, distinct working aliases, and the complete original ten-note
P4 v2 assertions.

## Exact evidence

- Runtime-pinned collection command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — PASS, 1 collected; existing unknown `timeout` config warning.
- Scoped Ruff: `RUFF_CACHE_DIR=/tmp/w-64efbed334/ruff-cache /root/.local/bin/ruff check tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — PASS.
- Private mypy: `MYPY_CACHE_DIR=/tmp/w-64efbed334/mypy-cache PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — PASS.
- `git diff --check` — PASS.
- Outside-base diff proof — PASS; only the named test differs.
- Retained Runtime normal34e pin: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Retained d106 edit-command schema digest: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Retained owner-fix `RemoteTimelines.open_bundle` caller/source blob: `astrid/sdk/_remote_timeline.py` → `60b373bb920456514be2e0fa05a93a5a6483d7c9`.
- Retained public Timeline/TimelineSession blob: `astrid/sdk/timeline/sync.py` → `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b`.

## Gate

**SOURCEPREP only.** Independent owner review of this exact port is still
required. Per the settled start-on-branch rule, no readiness, merge, HTTP,
socket, service/body, full-suite, browser, build, or existing P4-v2 HTTP-node
run was attempted. No genuine base/test incompatibility was found; no
positive assertion was changed, skipped, weakened, or deleted. After owner
PASS and independent port review, run only the existing P4-v2 HTTP nodes.
