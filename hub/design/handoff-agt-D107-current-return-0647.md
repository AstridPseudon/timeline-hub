# F-D86 D107 first return

## Scope

Updated only `tests/editing_conformance/test_m1_current_equivalent.py`. The
original `test_commit_runtime_m1.py`, fixtures, product code, Runtime, pins,
schema, and shared files are unchanged. The test remains one NEW-OURS test
function and parameterizes the original disjoint-rebase/undo branch and the
relevant-peer conflict branch.

## Conserved combination

- The held current product source remains unchanged: the registered native
  word picker uses `native_word_anchor_fixture.DECLARATION`, the real
  transcript, its persisted pin, and the current provider's binding command.
- The setup emits the original independent parent clip exactly: `id` and
  `asset` `music-bed`, `clipType` `audio`, track `music-other`, `at` 0,
  `hold` 5.5, and `extension.opaque == [None, {"keep": True}]`; the parent
  clip mirror is asserted equal. The current fixture admits the row's asset
  against an existing real media pin so current final validation can express
  the original audio topology without synthetic source data.
- The original CLI move writes `music-bed` to 1 and asserts response,
  stored-parent, reopened-bundle, receipt, command, source, pin, opaque, and
  timing readback.
- A is queued and durably accepted with a deliberately lost HTTP ACK. B is
  queued before A is acknowledged or the Runtime is restarted; its exact
  captured guard and pending order are asserted.
- A separate peer moves `music-other` to 2. Restart checks both foreign realm
  and foreign actor refusal, then retries A byte-for-byte with the same receipt
  and no duplicate history row.
- The touched-basis parameter changes `music-bed` to 4 and asserts B's exact
  conflict, no write, unchanged history, retained pending command, and
  retained conflict flight.
- The disjoint parameter flushes the original queued B at the accepted A
  base, asserts merged/rebased compatibility, exact command/base/source/guard,
  preserved peer field and opaque data, canonical readback, guarded undo,
  guarded redo, history provenance, CLI show/layers readback, and visualize
  inspection timing (`start == [2, 1]`).

## Static verification

- In-memory compile: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_m1_current_equivalent.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_m1_current_equivalent.py`: PASS.
- `git diff --check`: PASS.
- No pytest, import/collection, helper/fixture/function execution, service,
  browser, renderer, package install, or full suite was run, per the brief.

The production caller consumes this test's registered-provider/current-SDK
journey; no by-design refusal was substituted for setup or missing behavior.
