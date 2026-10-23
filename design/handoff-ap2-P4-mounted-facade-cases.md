# Handoff: ap2-P4 mounted facade cases

Status: PASS for bounded early P4 proof on Agent SHA `131561e2ba99eab41ce3588cfdee59e193aeeff3`.

Added `tests/sdk/test_p4_commit_v2.py` only for proof code. It exercises the public Python `timeline.open` facade through the mounted G3 emitter and the existing R1 command engine/provider seam:

1. A single parent clip edit is emitted as a guarded `doc.patch`, submitted once and observed in the accepted canonical document.
2. Ten independently addressed notes are staged with ten public `Timeline.command` calls and accepted as one commit. The request reaches the submission seam with ten `doc.patch` commands and ten ordered steps; all values survive provider execution and unrelated clip fields remain unchanged.

Verification:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_commit_cases.py tests/sdk/test_p4_commit_v2.py` → `4 passed` (one pre-existing environment warning for unknown pytest `timeout`).
- `/root/.local/bin/ruff check tests/sdk/test_p4_commit_v2.py` → pass.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_commit_v2.py` → pass.
- `git diff --check` → pass.

Unexecuted requirements are deliberate: R2 step undo is not integrated; no per-note undo, ten-note doc-patch conflict/re-run, show/history step readback, official Runtime HTTP/acceptance, authentic receipt attribution, CLI process path, or sheet-to-G3 path is claimed. Current CLI generic edits still use detached checkout save and native CLI move uses `session.move`; NativeSheet uses native `commit_many`, so those callers need a later owner task before they can qualify G3 P4 coverage. Existing G2 native conflict/re-run tests are evidence only for that native path.

The parent-only fixture is intentional for the original single-edit case. The connected fake provider’s compile helper drops unchanged child revisions in a parent-only document with an unrelated child closure; the existing joined-document G3 test covers the child-closure path separately. No fixture or product implementation was modified.
