# G5 alias baseline independent review and D21 bind preparation

## Verdict

**PASS for the source-only no-weakening review.** D21 harness preparation is
complete, but no live Runtime body was run and no G5 completion or P1 GO is
claimed.

The reviewed candidate is `64795e8ab5a32b9177fcbd2f1812a94b60f246c3`, tree
`48e3c3facecda7adb51c9b6e9ba3cc10da6f0666`, with base parent
`6120c25492574353ac12279f184b2355b53c4828`.

## Source and assertion custody

The three approved complete blobs from `bfcf78db998868e4a7d92779a83cd3aaba82a98a`
are byte-identical in the candidate:

| Path | Blob |
| --- | --- |
| `astrid/core/timeline/authoring_bundle.py` | `c00323f0755d2d6b2409df952a61c9e154c85d95` |
| `astrid/sdk/timeline/native_occurrence_duplicate.py` | `4338045a2272765dd1e35ff17bbca357ccc4fe04` |
| `tests/editing_conformance/test_occurrence_fork_source_baseline.py` | `dad27a538885ab45dd03242ee1670e00ff615dd3` |

The only additional test delta is the intended mixed-transaction migration in
`tests/editing_conformance/test_native_sheet_current_runtime.py`, blob
`0a23991cb98ce270da7c6bb7bdd9ec73e2ff402e`, SHA-256
`2dd71d0be3d2f455427de6f96f8926a9d0095d2dd244a5426e9367a598e697c4`.

The source review confirms that the single transaction is
`occurrence.fork` plus two `doc.patch` commands. It exercises the selected
fresh source pin, unchanged sibling, complete canonical document, raw and
null/absent values, history/records, reload, undo and redo, and keeps the
malformed-provider refusal. Expected records are calculated from the actual
v2 request and authenticated evaluated head. No counterfeit record authority,
private cache, alternate executor, synthetic reads, or weakened refusal was
introduced. The full request/reply assertions for base pair, commands,
selection/args, label, per-step intent/tags/patch/reads/ordinals, merge,
declared reads, idempotency, dry-run, source/rationale/group ID, and accepted,
merged, conflict, invalid, canonical, records, bindings, effects,
dependencies, history, undo steps, and preview fields remain in scope.

The 52-test collection retained 19 Runtime functions and all 33
authoring-feedback assertions. The previously approved actual unchanged
source-baseline integration witness and 135-control evidence remain the
authoritative live/source evidence; this review reran the offline controls.

## Checks

All commands ran from the candidate worktree with the pinned Runtime
`3b926efab2eed122d374540baee297d4cdcec62a`, tree
`b794170504544b259781e50d7ca4d61b6729e67c`, and private pytest/mypy scratch
paths.

```text
pytest --collect-only tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
52 tests collected; PASS

pytest -m 'not integration' tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py
151 passed, 1 deselected (the one integration body); PASS

pytest tests/timeline/test_authoring_feedback.py
33 passed; PASS

python -m ruff check --no-cache [four touched source/test files]
All checks passed; PASS

python -m mypy --cache-dir=<private scratch> --follow-imports=silent [four touched source/test files]
Success: no issues found; PASS

git diff --check
PASS
```

## D21 harness preparation

Created a new immutable wrapper at
`workers/agt-G5-alias-review-bind-1317/run-g5-emitter-current-runtime-nodes.sh`
with the sanctioned 1217 origin/import guards, candidate parent
`64795e8ab5a32b9177fcbd2f1812a94b60f246c3`, candidate tree, target-file
hash, Runtime 3b pin, producer, schema and Composition checks. Its SHA-256 is
`34ac30dd634bfa25f5d8406479a4efce4db9e39bcd5fc575e1cd215f5b1474c7`.

Updated only the existing `g5-emitter-current-runtime-nodes` row in
`tests/suites.conf` to point to that wrapper and its literal hash. The old
1217 wrapper remains unchanged at SHA-256
`d720fba3ab285078c7f10d0ca20836f1405cd19d10ba95d3817748a80da57d40`.

The no-body D21 preflight passed: wrapper syntax, candidate and Runtime
identity, clean Runtime tree, exact-node collection once, and Agent/client/
Runtime import origins. No central request was submitted, no wrapper body or
original HTTP request was executed, and no daemon, package, venv, Runtime
build, schema, generated file, pin, shared dependency, or product/test source
outside the reviewed candidate was changed.

## Limits and next step

Runtime 3b's known whole-undo/leaf-turnover failure remains unresolved. Keep
the positive undo/redo assertions. The next permitted action is one bounded
central D21 run only after the meaningful Runtime leaf fix is merged and its
qualified source is available; do not use a failed candidate Runtime pin.
This is source PASS and harness-ready preparation only, not Runtime
acceptance, G5 completion, integration readiness, or P1 GO.
