# G5 current-source retirement draft (agt-G5-current-draft-1122)

## Disposition

**Bounded draft; G5 is incomplete and merge remains strictly gated on P1. No merge requested.** Based on `abfa78a65`, with seven changed paths, 31 insertions and 769 deletions. No old draft ancestry or whole old source files were restored. The complete G5 retirement cannot honestly be called PASS while the dependencies below remain.

## Changes

- Removed the native `edit move`, `edit track-label`, and `edit commands-file` parser registrations and handlers; ordinary move/trim and sheet commits retain their existing durable session implementation.
- Removed `apply --native`; the existing sheet-content/connected-client dispatch still sends the same request. Removed only the obsolete `parsed.native` assertion from the P4 sheet test; all request, provenance, raw/full-bundle, absence, ordering, and receipt assertions remain.
- Removed CLI `undo/redo --publication` and separate CLI `publish`. SDK/public G2 undo and local draft history are unchanged. Numeric local undo/redo remain available.
- Deleted `astrid/sdk/timeline/document_diff.py` with `apply_patch Delete File`. It had no production imports/callers; G3 emitter tests remain unchanged.
- Updated the already failing core-only duplicate fixture to the existing real Runtime `saved_source` setup, using its canonical flat-film fixture with an off-canvas sprite. It still requires successful duplication under renderer/process fences and rejects archive cleanup. It now asserts the real accepted head, one `timeline.duplicate` request, the exact off-canvas value, and unchanged source. The old two-write count belonged to detached publication plus narration; no production duplicate implementation was changed.
- Mechanically decreased the mypy baseline 1912 → 1911 using the existing tool. The sole removed finding is `astrid/packs/timeline/cli.py:3005`, `"object" has no attribute "data" [attr-defined]`, in the deleted publish renderer lambda. Compared diagnostics by `(path, message, code)` with multiplicity: exactly one removal and zero additions. Ruff identities/counts are unchanged at 2149.

## Exact remaining retirement/dependency gaps

1. **SDK publisher is still live:** `cli_working._cmd_restructure` at line 493 calls `Checkout.publish`; `_PublishMixin.publish` at line 109 calls `store.publish_bundle`; `store.publish_bundle` at line 336 calls `three_way`. These bodies and the facade re-exports at `timeline_checkout.py:153–154` remain unchanged. The current D17 `_commit_bundle` accepts `_duplicate_command`, so it is not a generic restructure replacement. Porting the old 68a generic staging implementation would overwrite the current D17 design. A bounded restructure migration must precede deleting these bodies, with its original follow-up/retry behavior proven.
2. **Detached concurrent draft saves still use the merger:** `Checkout._save_locked` → `_merge_writer` → `store.three_way(..., whole=True)` at checkout.py:243. The existing disjoint-save success/overlap refusal and two-writer preservation tests pass unchanged. Removing this dependency here would remove promised behavior; no refusal substitution, alternate merge adapter, or weakened test was introduced.
3. **Existing test imports remain after the expressly requested module deletion:** `tests/timeline/test_authoring_feedback.py:18` and `tests/editing_conformance/test_native_sheet_current_runtime.py:23` import the deleted document_diff module. They are outside this task's allowed test-scaffold paths. They were not changed, skipped, or run. Their import migration is required before broader suites; module collection would otherwise fail. Old parser/publication expectations outside the bounded selection also remain unqualified.
4. **Historical 217-case coverage is not present verbatim in current source.** Running the identical 0806 file/node selectors collects 216 current tests: current sync adds two exact-pair hydration tests, while current restructure lacks these three 68a tests: `test_cli_restructure_commits_the_complete_equivalent_bundle_and_followups`, `test_restructure_reconciles_narration_without_republishing_the_cut`, and `test_restructure_retries_the_original_commit_after_lost_ack`. No tests were deleted by this draft. These three behaviors are an existing current-source qualification gap; this report does not silently count them as covered by unrelated copy tests.
5. **D17 retirement stays held.** All current D17 source/test blobs, including both original positives, are unchanged. Current source already uses the semantic copy command; this draft neither removes another duplicate path nor restores the former detached duplicate writer. The mandatory inverse family is not all green, as detailed below.

Retirement/caller audit commands:

```sh
rg -n 'publish_bundle|three_way|document_diff|_cmd_publish|_configure_publish|commands-file|--publication|configure_native_edit_parsers|configure_history_options' astrid/sdk/timeline astrid/sdk/timeline_duplicate.py astrid/sdk/timeline_checkout.py astrid/packs/timeline
rg -n 'commit_edit\(' astrid
rg -n 'timeline\.duplicate|_commit_bundle|publish_bundle|\.publish\(' astrid/sdk/timeline_duplicate.py astrid/packs/timeline/cli_working.py astrid/sdk/timeline/{publish.py,checkout.py,store.py}
```

The only old production definitions/callers found are the deliberately retained merger/publisher and their facade exports/comment. Remaining commit_edit callers are ordinary move, ordinary trim, and sheet apply. Outputs: `/tmp/w-89d91a99d4/retirement-grep.txt`, `/tmp/w-89d91a99d4/caller-map.txt`.

## Behavioral evidence (no skips)

All commands below ran from `/home/user/work/wt/agt-G5-current-draft-1122`. These are bounded, in-process tests; no live-socket/browser suite or full suite was run or requested.

Exact 0806 selectors on current source:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-89d91a99d4/targeted-final tests/sdk/test_timeline_sync.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/sdk/test_authoring_diff_cli.py tests/timeline/test_authoring_diff_format.py tests/sdk/test_timeline_restructure.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits
```

**216 passed in 25.36s.** Includes both original successful duplicate tests. Pre-edit identical selection: **1 failed, 215 passed in 21.85s**, the stale core-save duplicate fixture lacking `client.timelines.history`. Final log: `/tmp/w-89d91a99d4/targeted-final.log`.

Current public hydration and G2 facade undo guard:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-89d91a99d4/public-g2-final tests/sdk/test_timeline_public_command.py tests/sdk/test_timeline_open_commit_v2.py::test_public_session_undo_preserves_whole_shape_and_forwards_steps
```

**12 passed in 2.97s.** Log: `/tmp/w-89d91a99d4/public-g2-final.log`.

Runtime integration advanced during this task from `49ce53289` to `3b926efab2eed122d374540baee297d4cdcec62a` (tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean when inspected). The large selection above used the live Runtime checkout; it is not claimed as immutable paired-head qualification. To make the small D17 result attributable, archived the new commit read-only into private scratch:

```sh
mkdir /tmp/w-89d91a99d4/runtime-3b926ef
git -C /home/user/work/runtime archive 3b926efab2eed122d374540baee297d4cdcec62a | tar -x -C /tmp/w-89d91a99d4/runtime-3b926ef
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-89d91a99d4/runtime-3b926ef ASTRID_RUNTIME_CHECKOUT=/tmp/w-89d91a99d4/runtime-3b926ef PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-89d91a99d4/d17-stable tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_retained_inputs_whole_undo_redo
```

**2 failed, 2 passed in 4.28s.** Both repeated-shot variants `[False]` and `[True]` fail with `provider inverse effect bindings do not cover its stage image`. The single-source and retained-input inverse cases pass on this newer Runtime. The earlier live four-case probe returned the same 2-fail/2-pass outcome in 5.51s; the stable recheck was prompted by the Runtime head change. Stable log: `/tmp/w-89d91a99d4/d17-stable.log`.

The prior 49ce result remains reported, not erased: `design/agent-D17-integrated-1053.md` and `design/peer-agent-to-runtime-20261023T1058-D17-current-inverse-failure.md` reported four failures with `inverse stage write differs from its sequential input`. No unchanged 40/281/58/P1/P4 HTTP/browser/native14 suite was repeated here.

Both original successful wrappers were also checked against the immutable newer Runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-89d91a99d4/runtime-3b926ef ASTRID_RUNTIME_CHECKOUT=/tmp/w-89d91a99d4/runtime-3b926ef PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-89d91a99d4/d17-positives-stable tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared
```

**2 passed in 2.22s.** Log: `/tmp/w-89d91a99d4/d17-positives-stable.log`. These positives do not waive the failing mandatory inverse guards.

## Quality and preservation

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-89d91a99d4/ruff-final make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-89d91a99d4/mypy-final /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline --write-baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-89d91a99d4/mypy-final make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
sha256sum astrid/core/timeline/schema/edit-command.schema.json remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz
```

Ruff **2149/2149 PASS**. Mypy mechanically tightened **1912 → 1911**; final normal gate result is recorded in the completion section. Vendor lock **PASS**, artifact manifest **PASS**, diff check **PASS**. Producer stays `34eac0041b0891e9011966b39bcbd26053fde5bc`; schema hash stays `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; Composition archive stays `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

For exact diagnostic identity comparison, archived only current HEAD's `astrid`, `scripts`, and `pyproject.toml` into `/tmp/w-89d91a99d4/baseline` and ran the same normal mypy command there. Before: 1912 errors/958 source files; after deletion: 1911/957. Reports `/tmp/w-89d91a99d4/mypy-base-isolated.txt`, `/tmp/w-89d91a99d4/mypy-final.txt`, and `/tmp/w-89d91a99d4/mypy-identity-delta.json` contain the exact evidence. An initial concurrent pre-edit mypy attempt was invalidated when document_diff was deleted during discovery; it was not used as baseline evidence. Intermediate attempts at adapting the old tiny fixture failed setup (media idempotency grammar, prepared-schema validity, then incomplete compiler closure); they were replaced with the existing canonical flat-film fixture, without changing a product guard.

`git diff --exit-code HEAD --` over sync.py, commit_session.py, every D17 provider/caller/test path, public-command test, generated client, schemas, runtime.lock.json, artifacts.json and remotion/artifacts passed. No G2/G4 active owner source, Runtime source, hold/native/provider file, generated inventory/pin, contract, documentation, or upstream policy was changed. Full v2 request/reply definitions and production `WorkspaceClient.commit_timeline` delegation are byte-for-byte unchanged: base pair, commands, label, per-step patch/reads/ordinals, merge/reads, idempotency, dry_run/source/rationale/group_id; data+receipt accepted/merged/historical rebased; canonical closure/records/dependencies/effects/steps/history/undo_steps; mandatory preview would_status and structured conflict/invalid fields remain intact. The existing generated client remains the mounted transport.

No Git commit/merge/rebase/checkout/push, daemon, new executor/adapter, guard waiver, auth/duplicate semantic repair, shared dependency/cache write, skip/xfail, or safety/tool-classifier refusal occurred. The harness `tmpdir` marker is a regular file containing `/tmp/w-89d91a99d4`; its specified private scratch location was used without replacing the marker.

## Recommended next steps

1. Keep this as a bounded draft, with no merge request until P1 GO and independent review.
2. Resolve the owner-held repeated-shot inverse proof before declaring D17 writer retirement safe.
3. Migrate the remaining restructure publisher and preserve its three missing follow-up/retry behaviors; retain the detached local merger until a behavior-preserving authorized replacement exists.
4. Authorize/assign migration of the two out-of-scope document_diff test imports and the obsolete CLI test expectations before broader qualification. Do not delete or skip their behavior tests.
