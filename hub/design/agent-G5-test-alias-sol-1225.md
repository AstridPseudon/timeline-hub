# G5 occurrence-local emitter migration — 1225

**BLOCKED: existing D15 fork cannot compile this retained App closure. G5 DRAFT ONLY; P1 integration gate unchanged.**

No repository change is retained. A provisional test-only fork + emitter adaptation was withdrawn after an offline reproduction showed a product producer/compiler failure. The original accepted edit, unchanged shared sibling, malformed-parameter provider refusal, full canonical equality, history/records, reload, undo/redo, and all authenticated exact-pair assertions remain unchanged. No passing behavior was converted to refusal, skip, or xfail.

## Exact source and continuation node

- Agent HEAD: `6120c25492574353ac12279f184b2355b53c4828`.
- Agent tree: `3ed568fbd57a7732712bdd3558edc6f5ba008282`.
- Worktree: `/home/user/work/wt/agt-G5-test-alias-sol-1225`; clean; no new commit/SHA.
- Target file SHA-256: `28ca8b12f2ca21c84d74c6601ae3887fc4873e90ffa1f35c20a56177272df72e`.
- Unchanged authoring-feedback file SHA-256: `37ce863249b1cd375064b2297756c4ed0577a9dcd4d74606ae59098a0d95f2e5`.
- Exact node: `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated`.

The earlier central `11640` failure remains the last live witness. This worker made no service request and executed no HTTP/native/full/browser body. There is no meaningful fixed input to bind yet, so the brief's fixed-input + manager next-ops binding condition was not met. No wrapper was edited or bypassed. No R1 atomic dependency change or competing body was attempted.

## Precise missing producer boundary

The original one-alias mutation correctly hits the unchanged contradiction guard at `astrid/sdk/timeline/emitter.py:205`. Broadcasting the change across shared aliases would violate the unchanged-sibling requirement.

The existing registered semantic path was traced and exercised with the real pure command engine:

1. `capture_occurrence_fork(before, 'occurrence:f2-occurrence', 'emitter-selected-shot')` in `astrid/sdk/timeline/native_occurrence_fork.py:39` captures the registered fork. Its handler reads the source, binds `fork.source`, copies the child, and writes only the selected occurrence's shot identity.
2. `copy_child()` at `astrid/sdk/timeline/native_occurrence_duplicate.py:48` copies both shot payload and complete internal payload. Its `create_entity()` call at line 60 carries no immutable source baseline.
3. `Recording.create_entity()` at `astrid/sdk/timeline/_recording.py:205` sets the new shot's `_created=True`; the new shot is absent from `source_mapping['shots']`.
4. `compile_authoring_candidate()` at `astrid/core/timeline/authoring_bundle.py:970` consequently classifies that copied root as a new creation. At lines 1011 and 1028 it uses empty shot/internal baselines.
5. The retained App source has shot-item media `{OLD, AUDIO}` while the internal clips select only `{OLD}`. The audio item is legitimate retained metadata in the original closure. After the fork, empty baselines classify both sets as additions. The competing-media check at lines 1066–1081 rejects their unequal sets:

   ```text
   AuthoringBundleError: shot 'emitter-selected-shot' has competing selected media between shot items and internal clips
   ```

This occurs before emitting the desired patch or testing malformed parameter validation. It affects both:

- `bundle_from_document(document_from_bundle(execute(before, [fork]).bundle))`, the allowed normal projection intended to prepare a unique sequential physical source;
- `execute(before, [fork], commit_request={})`, which activates ordinary commit metadata/effect processing.

Passing `source_bundles=(before,)` to `document_from_bundle()` does not help: `commit.py:309` invokes the compiler before historical image reuse, and the new shot remains classified as created.

Calling the emitter directly on the fork preview also fails through `Closure.__init__()` (`_doc_patch.py:117`) → `document_from_bundle()` → the same competing-media check. On a simpler existing emitter fixture whose media sets agree, the raw preview additionally retains an orphan authoring alias: `emitter.py:193–196` cannot find a unique physical root for that alias. Ordinary document projection resolves that representation problem on the simpler fixture, but projection cannot pass the real App closure's earlier media failure.

The production `Timeline.command()` + free-edit path does not introduce a different compiler: `commit_session.py:89–95` passes staged bundles to this emitter, and `_append()` uses this same command engine. The current staged fork has no verified copied-source baseline that either boundary can use to distinguish retained metadata from new authored selection. This is the missing D15/G3 producer-to-physical-root seam; it is outside the sole allowed test file. It is distinct from 1216's atomic dependency-union ownership.

## Reproduction and limits

Offline diagnostic script:

`/tmp/w-5c8a5ddae0/probe_g5_fork.py`

Output:

`/tmp/w-5c8a5ddae0/probe_g5_fork.log`

The script reads the existing `app_closure()` fixture, applies exactly the existing `seed_emitter_parent()` payload preparation in memory, and uses the existing pure trusted-seed `_closure()` converter. It does not call trusted acceptance, fabricate prepared records, inject private authority, patch managed edges, change fixtures, or run an alternative executor. It deliberately does not ingest media/start Runtime; fixture media IDs are retained. The live seed's distinct ingested replacements preserve the media-set inequality, but this diagnosis is not a new live Runtime witness.

```text
Original canonical closure roundtrip: PASS
Registered fork preview: PASS; input and sibling unchanged
Created marker: True
Created root in source mapping: False
Shot-item media: OLD, AUDIO
Internal selected assets: f2-clear, f2-plate
Internal registry media: OLD
Fork document projection: AuthoringBundleError: ... competing selected media ...
Fork document projection with original source: AuthoringBundleError: ... competing selected media ...
Fork authoritative metadata execution: AuthoringBundleError: ... competing selected media ...
Sequential fork + emitter: DocumentPatchError: ... competing selected media ...
Original shared edit guard: DocumentPatchError: ... contradictory authoring aliases ...
```

Exact diagnostic command, exit 0 (the script prints captured diagnostic failures):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python /tmp/w-5c8a5ddae0/probe_g5_fork.py
```

## Final-tree checks

All commands ran from the assigned worktree, with shared dependencies read-only. `/tmp/.../workers/agt-G5-test-alias-sol-1225/tmpdir` is a harness pointer file containing `/tmp/w-5c8a5ddae0`, not a directory. Initial pytest attempts using children of that pointer produced setup-only `NotADirectoryError` (33 and 135 errors); the commands below corrected the scratch path. No safety/approval denial occurred.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-5c8a5ddae0/final-author tests/timeline/test_authoring_feedback.py
# 33 passed in 1.51s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-5c8a5ddae0/final-emitter tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py
# 135 passed in 13.98s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# 52 tests collected in 2.20s (33 + all 19); exit 0

/home/user/work/venv-agent/bin/ruff check --no-cache tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# All checks passed!; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-5c8a5ddae0/final-mypy tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# Success: no issues found in 2 source files; exit 0

git diff --check
# PASS; exit 0

git status --porcelain=v1
# Empty; no retained repository changes
```

Final pytest logs are `/tmp/w-5c8a5ddae0/final-author.log`, `final-emitter.log`, and `final-collect.log`.

## Decision and next owner

Keep the original test unchanged instead of submitting a migration that cannot produce its sequential input. The complete production v2 request/reply surface and its callers are untouched, including base pairs, commands, step patches/reads/ordinals, merge/key/dry-run/source/rationale/group IDs, receipts/canonical documents/records/dependencies/effects/history/undo steps and structured refusal fields. No success, negative-provider, equality, fixture, source-owner or managed-edge invariant was weakened.

Assign the registered copy/fork producer's retained-source provenance/media-baseline issue to its product owner. Preserve genuinely new competing-selection rejection while allowing a verified unchanged copy to retain pre-existing shot metadata. Once that product seam supports the actual retained App closure, resume this test-only migration with the normal projected fork input and submit fork + emitted patches in the same original transaction. Retain full target new-pin and unchanged-sibling document/pin checks. Only then should the manager bind a fresh ops wrapper and dispatch the single exact node above once. No all-19/full/other gate body is warranted by this report.
