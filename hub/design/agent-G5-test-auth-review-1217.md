# G5 authenticated emitter test fidelity review — 1217

## Verdict

**SOURCE PASS; BEHAVIOR FAIL; integration NO-GO.** This is a draft-only review
of `6120c25492574353ac12279f184b2355b53c4828` cumulatively against
`086db31e4`. No product or test-source edit was made by this reviewer.

## Source review

The cumulative diff is limited to the two intended test files:

- `tests/editing_conformance/test_native_sheet_current_runtime.py`
- `tests/timeline/test_authoring_feedback.py`

The 1208 change itself is only the authenticated current-Runtime test (+28/-11
in the target file). It preserves the public/private boundary correctly:

- the default public `open_bundle()` result is asserted not to contain
  `source_mapping['_runtime_document']`;
- the exact `revision_id` + `publication_id` pair is read through the public
  client boundary;
- project/timeline/revision/head identity, canonical document equality,
  canonical digest, complete hydrated bundle equality, and dependency closure
  equality are asserted;
- `bundle_from_document()` is applied only to the authenticated canonical
  document, and `persisted_bundle(before) == public_before` verifies that the
  private context was not injected into the ordinary public bundle.

This matches the production path: `_remote_timeline.open_bundle()` verifies the
scoped history receipt/publication and revision, rebuilds the complete closure,
checks the canonical document projection and dependency manifest, and restores
`_runtime_document` only on the exact-pair response. `commit_session.py` calls
`fetch_bundle()` with both basis pins before direct emitter execution, and
`sync.py` hydrates the outbox base with both pins. The full v2 request/reply
surface and production callers are unchanged by this diff.

The existing assertions remain in place for shared physical source/sibling
isolation, raw/opaque values, null and absence semantics, step/dependency
records, complete history, reload, undo/redo, and provider-boundary malformed
parameter plus unverified-media no-write cases. The malformed authoring cases
use `DetachedRealm.call()` → `create_runtime_commit_service().commit()`, not a
serializer refusal. The pre-1208 target node had 43 AST `assert` nodes and the
6120 target has 52; no subset-equality weakening, skip/xfail, refusal
conversion, fixture-file change, synthetic private cache, or forged Runtime
genesis was introduced. The trusted setup remains the existing Runtime test
acceptance boundary with ingested media and preserved canonical closure data.

## Verification

All local commands ran in the assigned worktree with the shared agent venv,
private basetemp/cache locations, and no source changes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-G5-review-1217-author tests/timeline/test_authoring_feedback.py
33 passed in 2.64s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  --basetemp=/tmp/agt-G5-review-1217-emitter \
  tests/editing_conformance/test_document_patch_emitter_engine.py \
  tests/editing_conformance/test_document_patch_emitter_v2.py \
  tests/editing_conformance/test_native_sheet_ordinary.py \
  tests/sdk/test_timeline_sheet_native.py
135 passed in 17.97s

... pytest --collect-only ... test_authoring_feedback.py test_native_sheet_current_runtime.py
52 tests collected in 2.58s (33 + 19)

/home/user/work/venv-agent/bin/ruff check --no-cache \
  tests/timeline/test_authoring_feedback.py \
  tests/editing_conformance/test_native_sheet_current_runtime.py
All checks passed!

... python -m mypy --cache-dir=/tmp/agt-G5-review-1217-mypy [the two files]
Success: no issues found in 2 source files

git diff --check 086db31e4..HEAD
passed
```

## Central behavioral witness

The independent ops worker updated the existing named service route and ran one
exact changed node, with wrapper hash
`d720fba3ab285078c7f10d0ca20836f1405cd19d10ba95d3817748a80da57d40`:

```text
agt-G5-witness-bind-1217-g5-emitter-current-runtime-nodes-1023121605-11640
1 failed in 4.07s; one body executed; no skip/zero-test/cache result
```

The wrapper verified Agent parent `6120c254`, tree
`3ed568fbd57a7732712bdd3558edc6f5ba008282`, Runtime `3b926efa` / tree
`b7941705`, and before/session-start/session-finish/after origins. The prior
29910 missing-private-image failure is therefore fixed: the test passed through
the public read and exact-pair authenticated hydration assertions.

The new failure is at
`tests/editing_conformance/test_native_sheet_current_runtime.py:309`, before
the malformed command is submitted to Runtime:

```text
DocumentPatchError: cannot emit a source-bound doc.patch:
closure root 'internal-revision:...-internal-revision' has contradictory
authoring aliases; use a semantic command
```

The emitter rejects the test’s one-child-row malformed mutation because its
internal revision aliases are no longer consistent. No Runtime commit/refusal,
history write, or no-write assertion after that line ran. This is an
emitter/test-input mirror-consistency failure exposed after the private source
hydration fix, not a Runtime response failure and not the R1 atomic dependency
union issue owned by 1216. Do not waive the emitter guard or claim behavioral
PASS.

## Recommended next step

The G5 owner should repair the test input at its owning boundary so the
malformed parameter change is represented consistently across the internal
timeline aliases, or construct the malformed provider request from a valid
emission without bypassing the emitter guard. Then rerun the same single
central node once. Until that bounded witness passes, keep G5 draft-only and
P1/integration NO-GO. No full, browser, daemon, dependency, pin, native14/58,
D17, or duplicate body run was performed.
