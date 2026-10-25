# F-final independent runner review

Result: **FAIL**. This is a read-only private review of return2342. No product,
test, fixture, generated, pin, registry, checkout, source, service, provider,
browser, network, build, ZIP, or live tuple was changed or executed.

## Targeted validation

- `PYTHONPYCACHEPREFIX=/tmp/rt-F-final-runner-review-2345-private/pycache PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile $(find <candidate> -type f -name '*.py' ! -path '*/__pycache__/*' -print | sort)` — **PASS**, 19 files.
- JSON parse over the 7 candidate JSON files — **PASS**.
- `find <candidate> -type f -name '*.sh' ! -path '*/__pycache__/*' -print0 | xargs -0 bash -n` — **PASS**, 3 shell files.
- `RUFF_CACHE_DIR=/tmp/rt-F-final-runner-review-2345-private/ruff-cache /root/.local/bin/ruff check --select F <all 19 candidate Python files>` — **PASS**, all checks passed.
- `/root/.local/bin/mypy --ignore-missing-imports --follow-imports=skip --explicit-package-bases --cache-dir /tmp/rt-F-final-runner-review-2345-private/mypy-cache <7 harness files plus 6 source-input files>` — **PASS**, 13 source files.
- `PYTHONDONTWRITEBYTECODE=1 python3 <candidate>/acceptance-d73.py` — **PASS**, one capture; four checkout receipts before request; newer-home marker accepted; selected-checkout drift refused.
- `PYTHONDONTWRITEBYTECODE=1 python3 <candidate>/d59-final-matrix/stubcontrols.py` — **PASS**, positive dispatch count 1; poisoned dispatch count 0; pending owner route refused without dispatch.

## Runner and inventory controls

- Private in-process `run-final-services.py` `main()` invocation with only
  source identity and `run_private_command` replaced by harmless stubs —
  **PASS**. Captured existing `core` argv had 101 Python targets, all unique,
  included the three successor targets, and retained
  `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test`.
  No subprocess or test body ran.
- Read-only existence check against `/home/user/work/runtime` — **PASS**,
  101/101 inventory targets are regular files.
- Negative inventory controls — missing file **REFUSED**; duplicate target
  **REFUSED**; absolute target `/tmp/unsafe.py` **REFUSED**; traversal target
  `tests/../../outside.py` **ACCEPTED** (**F2 failure**).
- `validate_artifacts()` private installer preflight — refuses with
  `core runner hash mismatch: a2d463... != 5ab35...`; no registry or tuple
  mutation occurred. This corroborates F1's stale runner binding.

## Preservation

- Predecessor/successor candidate comparison: 66/66 regular files present; only
  `run-final-services.py` and its derived `__pycache__/run-final-services.cpython-313.pyc`
  differ.
- All 41 physical files under `d59-final-matrix` were hashed and compared
  byte-for-byte; **PASS**.
- Source worktrees remained read-only and clean for this review. The final
  tuple and gate tuple remain pending; no D73 capture or installation was done.
- C0 request/reply shape and preservation claims are inherited unchanged from
  the byte-exact non-runner candidate files; no product/schema source was
  modified. No full/core/live suite was run.

## Blocking findings

### F1 — production route does not consume the successor runner

The directly tested successor runner is SHA-256
`49df8dfe2a5f889c49894c1e302181ca893547e74d0943abba7faf4c7e36c8c2`, but the
existing service row still executes the predecessor
`rt-F-final-2252-first-return-1130/evidence/candidate/run-final-services.py`
with SHA-256 `a2d463b32c9a1e13be1c0c7f1c003867094554b3a9a78ed6c332d273e03ce963`.
That predecessor is the 98-target runner identified by D136c, so the 101-target
inventory fix is dead metadata on the actual route. `run-final-delivery.py`
also pins that predecessor. The installer’s core-runner path/hash pair is
internally inconsistent and refuses before mutation.

### F2 — traversal is accepted by the new inventory control

The loader checks only `tests/` prefix, non-absolute form, count, and uniqueness.
It accepts `tests/../../outside.py`, allowing a selector entry to escape the
Runtime tests directory. The validator must reject parent-directory components
before this runner can qualify.

Recommended next step: return the candidate to its owner to bind the successor
runner/hash through the existing service row, delivery caller, and installer,
and reject traversal components; then obtain a fresh independent review.
