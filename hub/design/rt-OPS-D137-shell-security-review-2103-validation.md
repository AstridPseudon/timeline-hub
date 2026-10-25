# D137 independent source/security review

## Verdict

`PASS` for the assigned source/tests/kit review. The candidate makes the
smallest authorized maker change: the actual `STORE_CONTEXT` declaration now
exports exactly the two transitive shell helpers that were missing from the
parent boundary. The regression materializes the source declaration, executes
the resulting context through the real `Store.ensure` cleanup boundary, and
covers nonzero and timeout failure paths.

The result is source-unit evidence only. No production install, real request,
package acquisition, whole make, provider/core execution, browser, Farm, or
full suite was run. D137 fixture E2E remains withdrawn/NOTRUN, and the original
request remains stopped.

## Exact commands and results

- `TMPDIR=/tmp/w-dd3063825f PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — **PASS, 44/44**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/*.py` — **PASS**.
- `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` — **PASS**.
- In-memory compile of all 7 embedded Python blocks plus AST parse of scoped `install-prep/*.py` — **PASS**.
- Parent/candidate `STORE_PY` and `STORE_VERIFY` byte comparison against base — **PASS; byte-identical**.
- `TMPDIR=/tmp/w-dd3063825f PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` — **PASS**.
- `git diff --check` — **PASS**.

The suite's changed regression passed both cases through `Store.ensure`: exact
private stderr was retained at mode 0600, stage exit 17 and timeout 124 were
preserved, the public failure record remained payload-free, and the staging
tree was empty after rollback. Existing negative controls also passed,
including 1 MiB truncation with truthful full-input SHA-256, symlink/hardlink
and no-clobber defenses, ownership/RECORD/source closure, registration, and
reserve controls.

## Source audit

- Candidate `make-child-venv`: `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, 75,541 bytes, mode 0755.
- Parent/base and actual installed preimage: `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, mode 0755.
- The maker diff is one line only. The exported function list is exactly `failure`, `run_stage`, `progress`, `source_state`, `stage_stderr_path`, `retain_stage_stderr`.
- Static closure is complete: `run_stage → stage_stderr_path, failure, progress`; `failure → retain_stage_stderr`; `source_state` remains available for build and post-build source checks.
- The actual Store path is preserved: `STORE_PY` reads `STORE_CONTEXT`; its real `build` callback invokes `bash -u -o pipefail -c context + setup + body`; `Store.ensure` rolls back before recording the bounded public failure evidence.
- `STORE_PY`, `STORE_VERIFY`, `STORE_BUILD`, staging inventory, relocation, provenance, distribution metadata, and identity blocks are byte-identical to base. `bench_store.py` and `verify_dependency_seed.py` match the pinned hashes.
- Installer prep pins bind candidate `f07b8093…b969f` to preimage `4435d499…1d0a36` and preserve the reviewed CAS/no-follow/no-clobber route. The source-commit field is intentionally supplied only by the exact D137 decision input; this review did not invent or consume one.

## Red/green and disposition

The parent source reproduces the recorded first-boundary refusal:
`environment: line 60: stage_stderr_path: command not found`, exit 2.
The candidate's serialized context contains the helper and passes the same
first boundary. The authorized candidate regression then proves nonzero,
timeout, private 0600 retention, payload-free public status, and rollback
cleanup through `Store.ensure`.

No source finding remains. Recommended next step is the orchestrator's separate
owner disposition and reviewed CAS install gate; do not treat this source PASS
as live-route or E2E acceptance.
