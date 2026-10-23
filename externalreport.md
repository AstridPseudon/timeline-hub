# P4 rerun owner review — PASS

## Scope and disposition

PASS for the independent Luna HOME OWNER REVIEW of `de046064f` against PLAN
§3 P4 and C0. This is source/owner qualification only; the requested live
HTTP body remains explicitly unrun and is Proof-owned after home merge.

Exact identity:

- owncommit: `de046064f1632eef96bf08289f50a6ec3fefe4a3`
- commit tree: `18ff8ef23233569b05438764b9a364183ad20de9`
- target: `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`
- target blob: `192efbfa14607f0edfb362d47d5238645c64e984`
- target SHA-256: `02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36`
- diff: `386` insertions, `0` deletions; one path only

The owncommit is exactly one commit after `2e12b49ba`. The target blob is
byte-identical to the independently reviewed Proof0850 donor. No dependency/
product ancestry, reviewer source/test/pin, shared dependency, schema,
generated-file, lockfile, or Git edit was introduced.

## Preserved predicates

The imported test retains the public `timeline.open()` and
`opened.commit(fn)` path and the fixture's generated HTTP client/Runtime
handler transport. It asserts:

- actual call statuses `[200, 409, 200]`;
- first evaluation on the original head and second evaluation on the peer
  head, with `[None, PEER_VALUE]` fresh reads;
- exact original/retry base revision/publication pairs, idempotency-key
  behavior, command/step shape, and a retry plan computed independently from
  an authenticated peer document;
- canonical closure, shared physical shot/internal identities, authored
  opaque/null/absence fields, canonical digest, revision/publication head
  bindings, receipt/data equality, authoritative records and steps;
- conflict `reason`, `code`, canonical `path`, `base`, `current`, structured
  hint/suggested command/conflicts, and no conflict receipt;
- the exact dependency boundary: raw command captures remain empty while
  authoritative step dependencies retain the timeline scope and guarded
  canonical field; no fabricated `reads: []` replaces those captures;
- persisted history, publisher/provider/compiler metadata, restart/readback,
  fresh authenticated head re-evaluation, and empty outbox state.

The existing ten-note P4 neighbor and all existing v2 request/reply tests are
unchanged by this owncommit, preserving the broader request fields and
accepted/merged/historical-rebased/head/document/records/dependencies/effects/
steps/history/undo/preview and conflict/invalid structured-error coverage.
The current source uses no `cast()` or alternate executor/transport shortcut.

## Evidence

All commands ran from `/home/user/work/wt/agt-P4-rerun-owner-review-0904`.
The Runtime collection check used a private archive extracted from Runtime
commit `a5d4258312c979024865ee704da2d632ca5b2730`, tree
`f74b016ea837f8148db4a602c972073a226ed177`, at
`/tmp/w-45cde9a62c/runtime-a5d42583`. Shared Runtime state was not modified.

1. Integration collect-only — **PASS, 1 test collected**:

   ```text
   env -i HOME=/root LANG=C.UTF-8 PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/tmp/w-45cde9a62c/runtime-a5d42583" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/tmp/w-45cde9a62c/runtime-a5d42583 /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider --collect-only -m integration tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
   ```

2. Scoped Ruff — **PASS**:

   ```text
   /root/.local/bin/ruff check --cache-dir=/tmp/w-45cde9a62c/ruff-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py tests/editing_conformance/test_p4_ten_note_v2_runtime.py
   ```

   Result: `All checks passed!`

3. Private-cache Mypy — **PASS** on both P4 files:

   ```text
   env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-45cde9a62c/mypy-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py tests/editing_conformance/test_p4_ten_note_v2_runtime.py
   ```

   Result: `Success: no issues found in 2 source files` (only normal
   untyped-function informational notes).

4. Private-cache compilation — **PASS**; `py_compile` completed for the rerun
   and ten-note files.

5. Whitespace — **PASS**: `git diff --check de046064f^ de046064f`.

6. Identity/outside-file audit — **PASS**: exact commit SHA/tree/blob/
   SHA-256, one commit after `2e12b49ba`, one changed path, and no outside-file
   changes.

7. Static caller/import audit — **PASS**: `timeline.open()` and
   `opened.commit(append_review_suffix, ...)` are the production caller path;
   the fixture uses `GeneratedWorkspaceClient(..., transport=transport)` and
   `RuntimeHandler`, with Agent and generated client imports from this
   worktree and `runtime_protocol` from the private `a5d42583` archive.

## Limits and next step

No actual HTTP body, socket/service run, full/native14/crash24/browser/journey,
or new-service execution was performed, by explicit task scope. Existing
independently reviewed focused/tamper evidence is reused only for the exact
unchanged product/test assumptions recorded in the handoffs. Proof should run
the one integrated original node after this home merge; this review does not
claim that behavioral result.
