# WC1 current landing report

## Resolved landing

- Merge parent: `c4b964f6a050edf63a4278d35717e46a88a80386`.
- Merge-parent tree: `d7796be264c341adbcb9765aae374b832dede144`.
- Expected resolved tree: `649d170a74304c5838596ac4baa7c127e57af9fa`.
- The harness should create the merge commit; no commit was created in the
  worker sandbox.
- Only these approved test paths differ from the merge parent:
  - `tests/editing_conformance/test_commit_runtime_occurrence_media.py`
    (exact approved blob `857fe815bd080ec4b999de89ee4425491968ca6c`)
  - `tests/editing_conformance/test_commit_runtime_parent_media_swap.py`
    (exact approved blob `66ba1bf4c77da3a008f762df749c74866e0e77dd`)
- All other paths, including product code, pins, and unrelated assertions,
  match `c4b964f6a` exactly. No fixture coverage was removed.

## Central proof identity

The central named lane recorded `2 passed in 9.16s` from source tree
`444e09d77f9774d0d7864c188a8f36541bc08fd1`. It is not identical to approved
candidate tree `d6aba756208419b9bdfa17e11c7b08710ad5399c`.

Concrete difference: the parent test checker blob was
`65ed693d5469bb9344feb75ecabd91b5bca85ca2` centrally and is
`66ba1bf4c77da3a008f762df749c74866e0e77dd` in the candidate. The candidate
changes the legacy writer path predicate from substring matching to exact
terminal `endswith('/composition-revisions')` / `endswith('/publish')`.
The occurrence fixture blob is identical (`857fe815...`) across both trees.

Therefore the 9.16s result remains a bounded prior result, not exact proof
of the approved candidate or this landing. Exact-candidate qualification is
HOLD. No HTTP, native, body, or full-suite rerun was made, as instructed.

## Preserved proof scope

The landed blobs retain the original 8cad fixture OLD identity and the
reviewed request method/path/phase checker, planted forbidden-writer negative,
request/key/body/base/media/guard assertions, outbox flight and restart
identity, receipt/reload/inverse/sibling assertions, and both parent and
occurrence scopes. The broader WC1/store-writer question remains open; this
landing carries only the approved native media/outbox slice.

## Checks

- Structural comparison against `c4b964f6a`: passed; no outside paths differ.
- Approved blob identity checks against `c7e392f19`: passed for both files.
- `git diff --check c4b964f6a -- .`: passed.
- Python AST parse of both approved test files with
  `PYTHONDONTWRITEBYTECODE=1 python3 -B`: passed.
- HTTP/native/body/full suites: not run.
