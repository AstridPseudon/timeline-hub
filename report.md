# agt-V2-child-asset-trace-0623 — bounded readonly classification

## Verdict

- **Readonly review: PASS.** Evidence was produced against current Agent HEAD
  `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`; no product source, test,
  schema, generated file, pin, or dependency was changed.
- **Child missing-asset retention: FAIL.** The unchanged child selector is
  rejected before the final V2 validator can apply approved D12/D12a.
- This is a **pre-existing canonical authoring/projection limitation**, not a
  new V2 invalidity and not grounds to remove D12/D12a retention guards.

## Evidence

The prior exact probe identified in `agent-V2-D12-guard-audit-0612.md` was no
longer present at `/tmp/w-70ce9f45ed`. I reconstructed it from that report,
using the existing `document_fixture(shared=True)`, the existing child clip
and registry identities, and the exact prior missing selector
`asset: "already-missing"`—no new media digest or asset identity was invented.
The request changes only the parent name from `Renamed Film` to
`Unrelated parent name`; the child asset selector and missing target are
unchanged in baseline and candidate.

Scratch command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python \
  /tmp/agt-V2-child-asset-trace-0623/child_asset_trace.py
```

Result for the faithful original request:

```text
REFUSED CommitRejected
shots[shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f].internal_timeline.clips[0].asset references missing registry asset 'already-missing'
head_unchanged True prepared 0
```

The same production-provider scratch run supplied the two required strict
negatives, using only existing `picture` and `already-missing` identities:

| Negative | Result |
|---|---|
| Write child `clips/id:clip-a/asset` from existing `picture` to existing missing selector `already-missing` | `CommitRejected`, `invalid_document`; head unchanged; `prepared 0` |
| Remove existing child `registry/assets/picture` while `clip-a.asset` remains `picture` | `CommitRejected`, `invalid_document`; head unchanged; `prepared 0` |

Normal provider control with the same parent-name edit and a valid child
registry returned `accepted` and the new parent name. The direct final
validator probe, after opening the valid document and then changing only the
child selector to the already-missing value, returned:

```text
FinalCandidateError candidate.timing: ...clips[0].asset references missing registry asset 'already-missing'
```

## Classification and owner seam

Approved D12/D12a applies: the contract says an unresolvable declaration
already in the base is preserved byte-for-byte when its declaration and target
are unchanged; a target absent in both baseline and candidate was not removed
by this commit. The faithful request satisfies that condition. The two
negative requests do not: one writes a missing target and one removes a target
that was present, so their refusals are correct and must remain strict.

The smallest later-repair seam is the existing authoring compiler in
`astrid/core/timeline/authoring_bundle.py`, specifically
`_assert_internal_edit_supported()` (line 652, call at line 982) and
`_clip_selected_media()` (line 541, rejection at lines 552–554). The compiler
currently resolves every candidate child selector, including unchanged
inherited selectors, before the provider reaches the V2 final-validator path.
The existing map-locality owner remains untouched; no change was made to
`_commit_timing_validation.py`.

Any later repair must retain source authentication: use the Runtime-verified
`source_mapping["_runtime_document"]`, exact physical closure/revision pins,
content digests and dependency manifest; compare declaration/target ownership
against the authenticated baseline and candidate; preserve authored bytes; and
continue refusing newly written, changed, removed, retargeted, or physically
owner-changed assets. Payload equality or a guessed/latest asset may not prove
historical presence. No contract clarification is required for this finding;
the missing behavior is an existing-owner compiler change.

## Production caller and API preservation

The mounted caller remains `astrid/sdk/timeline/commit.py:1116–1125`:
`create_runtime_commit_service().commit()` invokes `validate_final_candidate`
with the candidate bundle, authenticated baseline/head selection,
`schema_inputs`, realm, and inverse source bundles, then materializes through
`document_from_bundle`. The timing adapter reaches
`compile_authoring_candidate()` at
`astrid/sdk/timeline/_commit_timing_validation.py:314`; the authoring compiler
refusal is therefore upstream of the intended D12 decision.

No request/reply surface was changed. The existing v2 request remains the
full `api_version/project_id/timeline_id/base_revision_id/base_publication_id`,
`commands`, `label`, `steps(id,label,intent,tags,command_ordinals,patch,reads)`,
`merge(fields|atomic)`, request `reads`, `dry_run`, `source`, `rationale`, and
`group_id`, with stable idempotency. Existing `{data, receipt}` accepted/
merged and historical `rebased` behavior, canonical document/head/revision/
digests/records/effects/steps/dependencies/history/undo_steps, conflict
reason/head, invalid code/path/hint/suggested command, and preview
`would_status` remain untouched. This is a bounded readonly classification,
not a wire qualification.

## Tests and quality gates

Targeted provider/D12 tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_p1_doc_patch_provider.py::test_child_vectors_use_runtime_commit_service_and_preserve_shared_alias \
  tests/sdk/test_p1_doc_patch_provider.py::test_unchanged_unresolved_legacy_timing_is_retained_for_unrelated_edit \
  tests/editing_conformance/test_commit_boundaries_d12.py
→ 27 passed in 1.83s
```

Passing focused quality gates:

```text
ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_boundaries_d12.py
→ All checks passed

mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py --follow-imports=skip
→ Success: no issues found in 2 source files

make ruff PY=/home/user/work/venv-agent/bin/python
→ current=2149 baseline=2149

python -m scripts.reshape.compare_mypy_baseline
  (using /home/user/work/venv-agent-typecheck-v2/bin/python)
→ current=1914 baseline=1914

python scripts/vendor_lock.py check runtime.lock.json
→ ok runtime.lock.json

python scripts/artifact_manifest.py --check
→ artifacts.json is current

git diff --check
→ clean
```

An exploratory broader scoped lint/typecheck including untouched legacy owner
files reported existing diagnostics (`F811` fixture-parameter redefinitions in
`tests/sdk/test_p1_doc_patch_provider.py`, and two existing union narrowing
errors at `authoring_bundle.py:1362`). The focused V2 gates above pass; no
baseline or budget was changed. No full, browser, HTTP, native14, heavy, or
farm suite was run.

Import origins used by the evidence:

```text
astrid                         /home/user/work/wt/agt-V2-child-asset-trace-0623/astrid/__init__.py
astrid.sdk.timeline.commit    /home/user/work/wt/agt-V2-child-asset-trace-0623/astrid/sdk/timeline/commit.py
authoring_bundle               /home/user/work/wt/agt-V2-child-asset-trace-0623/astrid/core/timeline/authoring_bundle.py
_commit_timing_validation      /home/user/work/wt/agt-V2-child-asset-trace-0623/astrid/sdk/timeline/_commit_timing_validation.py
validation                     /home/user/work/wt/agt-V2-child-asset-trace-0623/astrid/sdk/timeline/validation.py
runtime_protocol               /home/user/work/runtime/runtime_protocol/__init__.py
banodoco_timeline_schema       /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py
Python                         /home/user/work/venv-agent/bin/python
Typechecker                    /home/user/work/venv-agent-typecheck-v2/bin/python
```

Recommended next step: add a separate owner row after the current map-locality
work, scoped to the authoring compiler seam above, then rerun this exact
faithful request plus the two strict negatives without changing any existing
expectation or D12 exemption.
