# P4 HTTP command correction — source readiness retained

## PASS — corrected targeted selector; HTTP body still unexecuted

The prior 0242 source-readiness PASS remains valid for `ddff86c18`: exactly one
new test, collection/Ruff/mypy/diff checks, and the reviewed CLI → NativeSheet →
session/outbox → generated HTTP → Runtime/provider → `show`/`history` path are
unchanged. No repository files were edited by this correction.

The later service command was corrected because `agent targeted` alone uses the
default Agent `addopts`, which deselects `integration`. The future compatible
owner-join worker must be substituted for `OWNER_JOIN_WORKER`; 0242 and any
recycled author worker are not valid execution sources:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER targeted --files '-m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

`tests/suites.conf` expands that request to:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back
```

## Collection evidence

With the existing Runtime prerequisite and source path, the equivalent local
collection command was:

```bash
PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back
```

Result: **PASS — exactly 1 test collected**. The no-selector comparison was
`no tests collected (1 deselected)` with exit 5, confirming the correction. This
worker environment has no `/home/user/work/venv-agent/bin/python`, so the
collection check used the existing `venv-app2-native`; the central service must
use the suite's actual Agent venv. No targeted service run was queued.

## Boundary and prerequisites

Do not queue the body until the normal official client is corrected/adopted and
the compatible G3/R2 owner join is available, with `ASTRID_RUNTIME_CHECKOUT`
pointing at the matching Runtime source and `PYTHONPATH` exposing the Agent
source. The production caller is traced through parser, sheet, session,
generated HTTP, Runtime/provider, `show`, and `history`, but remains
**UNEXECUTED** here. This is not wire acceptance, P4 completion, or H3 credit.

Preserve the full v2 request and reply scope from the prior review: API version
1; project/timeline and base revision/publication IDs; commands, label, steps
with patches/reads; merge mode; request reads; dry-run; Idempotency-Key;
accepted/merged canonical closure, digest, heads, receipt, commands,
authoritative steps/dependencies/merge mode; conflict reason/head; invalid
code/path/hint/suggested command; and preview `would_status`. Conflict/invalid/
preview, ten-note per-step undo, re-run, restart, and other wire qualifications
remain open.

