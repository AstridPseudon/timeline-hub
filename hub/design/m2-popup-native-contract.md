# M2 popup native contract — shared provenance fixed; popup publication pending

Worker: `agt-m2-media-manifest-provenance`. Base:
`c3da1535053b34bf63fcc4d6a06b3563087b38f4` (`tl/agt-m2-popup-media`).
Implementation is frozen at this handoff; the harness supplies its commit.
All M2 integration remains held until the orchestrator records PLAN M1 exit.

The shared media-manifest inverse blocker is resolved. Both original strict
xfails now pass with their exact-document expectations, including original
parent revision identity. No production occurrence media opcode, capture,
parameter schema, App args or recorder golden is published by this change.

## Exact framework seam

The existing import gains one optional, provider-only Python argument:

```python
from astrid.sdk.timeline.commit import document_from_bundle

canonical_document = document_from_bundle(
    plan.bundle,
    source_bundles=inverse_sources,
    inverse_records=inverse_records,
)
```

`RuntimeCommitService.commit` already supplies this argument. `inverse_records`
is the existing internal
`astrid.sdk.timeline._collections.AcceptedRecords` loaded from accepted history,
with `entries` and `load_boundary(entry) -> (before_bundle, after_bundle)`.
The loader checks publication ancestry, the previous publication/revision pair,
and exact project/timeline closure scope through the existing port. Native
handlers and clients do not construct this object, pass a manifest override,
or serialize any new recorder field. Detached lists cannot authorize pin removal.
Historical `source_bundles` alone continue to preserve all current source pins.
The new `_inverse_media_removals` helper is private.

The shared converter derives each accepted edge's added media pins from its
before/after manifests. It verifies exact immutable images, then reproduces the
accepted output payload/shot/internal closure from recorded authored and derived
writes. Every introduced pin must appear in those authored writes. Changed
unrecorded document scope or unexplained pin changes refuse with
`history_unavailable`; malformed closures refuse with `invalid_document`.
It processes targeted publication deltas in reverse order, including inverse
edges, rather than pruning all unused media or restoring a whole manifest.
Whole-closure restore continues through its existing exact-source mechanism.

Only proven introduced pins are eligible for removal. Original retained pins
and newer disjoint media stay. If a resulting payload or retained, verified
source document still references an eligible pin, undo refuses with
`surviving_dependents`. Missing retained document captures refuse with
`history_unavailable`. The normal authored-write/read/selection and intervening
publication checks still guard undo and redo, including same-value ABA writes.
Compilation and historical image comparison still determine exact revision
reuse; there is no parent snapshot replacement.

Grouped create+undo also exposed an existing inverse installation bug:
coalescing can yield an absent-to-absent child write. Such a write now remains a
recorded assignment, rather than attempting to recreate `before['value']`.
Its value and history guards remain in place.

## Recipe for the next popup worker

Continue using deterministic normal recorder primitives: read the exact owner,
source, old binding and selected child/membership; record creation of the missing
registry key (or require an identical existing binding); create the reserved
child for ADD or write the existing child's asset for SWAP. Preserve opaque and
null data and raw child-relative timing. Registry creation and its consumer
belong to the same command batch. Let the shared provider/compiler perform the
manifest and inverse work; there is no command-local cleanup hook.

Use ABI 1 `selected_media(MediaSelection) -> VerifiedMedia`, with the exact
`(asset, generation_id, variant_id, object_id, catalog_digest)` selection and
recorded dependencies, for production media admission. The held existing-slot
parent swap implementation/proof remains bounded to its prior scope:
`9ebd87afca97382e51c060fa2ca018c43f09f8bd`, 24 previously reported real tests.
This worker read that implementation and reused its real managed-output fixture
pattern; it did not port or rerun the 24-test parent suite.

The next worker must publish actual native occurrence capture exports,
operation names/versions, parameter schemas, App args and authoritative recorder
goldens before App consumes them. Those names and artifacts remain unavailable
here. Display `${occurrenceId}:${clipId}` is not the raw child ID; retain the
explicit occurrence owner and unprojected timing. Existing refusal scope still
applies: parent/display selectors, missing immutable closure/owner pins,
ambiguous membership, registry collisions, mismatched media tuples, implicit
shared edits, unsupported timing/source maps and out-of-occurrence intervals.
Clear/shared editing, placement, relational `timeline_frame`/`metadata.end_frame`
and standalone registry upserts remain outside this slice.

## Executable evidence and qualification limits

Source worktree:
`/home/user/work/wt/agt-m2-media-manifest-provenance`.

* `tests/editing_conformance/test_occurrence_media_manifest_inverse.py`: both
  former strict xfails pass; exact reload/undo/redo/undo, original unselected
  source pins, later disjoint media/references, surviving dependents, retained
  document captures, ABA guards, corrupt boundaries and grouped inverse deltas.
  Parent media introduction also uses the same framework successfully.
* `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`:
  real managed image outputs via the Runtime generation settlement fixtures,
  authenticated public selection read, public `RuntimeService.commit_timeline`,
  real port validation/acceptance, preview, reload, restart, exact retries of
  introduction and undo, changed-payload retry refusal, exact redo, immutable
  historical receipt/dependency/manifest retention, and integrity verification.

The real test uses a test-only deterministic recipe plus a provider subclass
that performs the declared `selected_media` ABI read and delegates all semantics
to the unchanged shared provider. It never replaces a prepared candidate or
accepted history. This proves existing Runtime acceptance permits a result media
manifest smaller than its captured input media closure while keeping historical
inputs. It does not qualify production popup admission or its captures.

The real legacy seed publisher only accepts numeric fps in its visual seam, so
that fixture uses 24 fps and scalar source offsets/speed. Rational 30000/1001 fps,
source preservation, occurrence isolation and opaque fields remain covered by
the detached regression. No production Runtime change was made.

Final commands from the source worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_recorded_graph_roots.py tests/editing_conformance/test_recipe_m1_commands.py
# 303 passed in 13.59s

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_runtime.py
# 4 passed in 2.43s
```

Ruff over all four changed Python files and `git diff --check` passed. Runtime
source was `9f9b25c000485e919f30f1411831fe2d5a3c1316`.
No full suite, browser/socket suite, installation, integration merge or push ran.
Normal packaged artifact refresh and production-provider qualification remain
release gates. Resume the bounded popup worker only on the orchestrator's
approved base; keep all M2 integration held pending PLAN M1.
