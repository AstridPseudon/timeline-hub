# G5 independent review: FAIL

Reviewed bounded draft `086db31e4` (`tl/agt-G5-current-draft-1122`) against
`abfa78a65`. The base is an ancestor and the draft is one production commit
with exactly the seven declared changed paths (`31 insertions, 769
deletions`). No product or test files were changed by this review, and no
merge is requested.

## Findings

1. **Blocking: P1 NO-GO still gates every G5 deletion.** PLAN §3 requires the
   integrated P1 feasibility set before A4/G5 deletion work. This review
   therefore cannot pass or authorize merge.

2. **The old publisher and merger are still genuine production paths.**
   `astrid/packs/timeline/cli_working.py:493` calls `Checkout.publish`, which
   reaches `astrid/sdk/timeline/publish.py:109` → `store.publish_bundle` →
   `store.three_way` (`store.py:311,336`). The facade re-exports both at
   `astrid/sdk/timeline_checkout.py:153-154`. Detached concurrent saves also
   use `_save_locked` → `_merge_writer` → `store.three_way(..., whole=True)` at
   `astrid/sdk/timeline/checkout.py:235-243`. Existing disjoint-save,
   overlap-refusal, and two-writer tests pass, so these are retained behavior,
   not safe deletion candidates.

3. **Two deleted-module imports fail collection.**
   `tests/timeline/test_authoring_feedback.py:18` and
   `tests/editing_conformance/test_native_sheet_current_runtime.py:23` still
   import `astrid.sdk.timeline.document_diff`. Collection-only verification
   produced two `ModuleNotFoundError` errors and collected no tests. These are
   outside this bounded task's allowed test-scaffold edits; they must be
   migrated by their owners. No tests were skipped, weakened, or deleted.

4. **The changed CLI still advertises a removed command.**
   `astrid/packs/timeline/cli.py:1209,1230-1234` and `:3235-3240` emit
   `publish` in workflow/resource/next-command guidance even though the
   `publish` parser route was removed. This is stale user-facing guidance.

5. **Historical qualification is 216 current tests, not the old 217-case
   set.** The exact current selector passes 216 tests; the older draft's
   217-case selector is not verbatim current source. Current sync adds the
   public hydration pair while current restructure lacks three historical
   restructure cases. No test was deleted by this draft, but the gap must not
   be counted as G5 coverage.

## What passed / was preserved

- Exact targeted selector: **216 passed in 25.52s**.
- Exact public hydration/G2 selector: **12 passed in 2.20s**.
- Retained ordinary move/trim, sheet commit, P4 request/receipt assertions,
  emitter, restructure, core-save, and detached merger assertions passed. The
  removed `parsed.native` assertion was the only assertion removed from the
  P4 sheet test.
- The duplicate core fixture is stronger, not weaker: trusted Runtime
  `saved_source` seam, canonical `flat_film`, an off-canvas sprite, the real
  production `duplicate_timeline` caller, one semantic `timeline.duplicate`
  commit, exact copied value, unchanged source, and an archive guard. The 216
  selector passes this test.
- `document_diff.py` has no production imports; only the two failing test
  imports above remain. G3 emitter tests are unchanged and pass in the
  targeted selector.
- Mypy normal gate: **1911/1911**. Archived `abfa78a65` identity comparison:
  **1912 → 1911**, exactly one removed diagnostic and zero additions:
  `astrid/packs/timeline/cli.py`, missing `data` on `object`, `[attr-defined]`.
- Normal Ruff gate: **2149/2149**. Direct changed-file Ruff reports 15
  pre-existing `cli.py` diagnostics; base/current comparison has the same
  diagnostics after line-number normalization, with no new finding.
- Vendor lock passed against frozen producer `34eac0041b08…`; artifact
  manifest passed; `git diff --check` passed. Frozen hashes remain
  `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`
  (schema) and
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
  (Composition artifact). Protected v2/client/schema/inventory paths are
  unchanged, including the full request/reply shape and production commit
  delegation.
- D17 source/test paths are unchanged. Existing exact Runtime3b checkout is
  `3b926efab2eed122d374540baee297d4cdcec62a` at
  `/home/user/work/wt/rt-pin-3b926efa`. Per brief, unchanged D17/full,
  browser, HTTP, P1/P4, and native14 suites were not rerun. Existing Runtime3b
  evidence is **2 passed, 2 failed** for repeated-copy inverse variants; the
  two failures are the known base mismatch involving newer public undo
  behavior (`publicundo78f`), not a regression from this deletion commit. This
  is not a pass for the D17 gate.

## Exact commands

The exact targeted commands were run with private `/tmp` basetemps:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-draft-review-1137-targeted/targeted tests/sdk/test_timeline_sync.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/sdk/test_authoring_diff_cli.py tests/timeline/test_authoring_diff_format.py tests/sdk/test_timeline_restructure.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits
```

Result: **216 passed in 25.52s**.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-draft-review-1137-targeted/public-g2 tests/sdk/test_timeline_public_command.py tests/sdk/test_timeline_open_commit_v2.py::test_public_session_undo_preserves_whole_shape_and_forwards_steps
```

Result: **12 passed in 2.20s**.

Also run:

```text
RUFF_CACHE_DIR=/tmp/agt-G5-draft-review-1137-targeted/ruff-scoped /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/timeline/cli.py astrid/packs/timeline/cli_native.py astrid/packs/timeline/cli_parser.py tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_scene_save_core.py
RUFF_CACHE_DIR=/tmp/agt-G5-draft-review-1137-targeted/ruff-full make ruff PY=/home/user/work/venv-agent/bin/python
MYPY_CACHE_DIR=/tmp/agt-G5-draft-review-1137-targeted/mypy make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy
python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
python scripts/artifact_manifest.py --check
git diff --check abfa78a65 086db31e4
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
```

The scoped Ruff command reports the same 15 pre-existing `cli.py` findings as
`abfa78a65`; the normal Ruff gate passes. Mypy, vendor lock, artifact manifest,
and diff check pass. Collection intentionally fails with the two
document-diff import errors above. No full, browser, HTTP, P1, P4, or native14
suite was run.

## Recommendation

Keep the draft bounded and **FAIL** it for G5 completion. Resolve P1 first,
then have the publisher/restructure, detached-merger, and two test-import
owners complete behavior-preserving work. Do not delete retained
publisher/merger bodies or weaken import-dependent tests as part of this
draft.
