# Agent/Runtime RT03 reference projection review

## Verdict

**APPROVE — bounded source/data-safety review only.**

I found no concrete cross-area data-loss, cross-project custody, identity
overwrite, or unplaced-to-placement counterexample in the requested Runtime
candidate and Agent source cohort. This is not approval to freeze, generate,
pin, publish, or claim the original strict normal-provider positive.

## Exact inputs

- Runtime candidate: commit
  `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`, tree
  `47d5f06df25618b45a95293c5217e6454f6ae69c`, directly on
  `f53bf588bf70b090ce8e0bed5ccb7d91157771b6` (parent tree
  `d82f37052847949e77c12e1704c3f27c6dd56a46`), base `95bd3c5…`.
- Agent source: `d1f5f7824a5ede5587088735fad6e6870f0b95db`, tree
  `ca825c4bf900400487f9a1ca6b8c1651d63d5a68`.
- Agent latest reference/order composition: commit
  `85c90d526901076bc6e8d543a1473427c7504593`, tree
  `4acbb9d3508a693d9d11da709684260d4cea0b16`, parent `d1f5f7824…`.

The Runtime candidate changes only the accepted projection, its store hook,
an explanatory document, and focused projection tests. The f53 carrier changes
remain the existing `MediaManifestEntry`/private `raw_media_info` seam; no
OpenAPI/schema/generated-client/artifact surface is changed.

## Cross-area safety checks

- The Agent command is parent-scoped and writes only the existing canonical
  `config.app.astrid.timeline_references[reference_id]` leaf, plus the
  existing parent asset-registry birth required by the Agent recorder. The
  closed leaf is v1, has literal `role: source`, and carries exactly
  `{media_id, content_digest}` with equal lowercase SHA-256 digests. No
  `MediaInfo`, catalog relation, generation tuple, alias, placement, shot,
  occurrence, clip, track, or managed five-field selection enters authored
  state.
- Agent commit capture calls Runtime `raw_media_info` for the exact command
  pin. Runtime requires that pin in the declared command set, checks the
  request project and managed ownership, opens one CAS descriptor, verifies
  regular-file identity/size/full digest/stable descriptor identity, and
  returns only the existing private `MediaInfo` shape. Acceptance rechecks
  the captured result and candidate manifest membership before persistence;
  only the captured raw object extends the existing authorized-media set.
- Runtime projection reads only the accepted parent revision’s namespaced
  carrier and existing dependency manifest. `_desired()` rejects malformed
  leaves, non-source roles, non-v1 leaves, unequal/invalid pins, and pins not
  appearing exactly once in accepted custody. It does not consult a catalog,
  infer placement, normalize the parent, or create a second authority.
- Occupancy is checked before writes against the global
  `timeline_references` identity, joined to its timeline/project. This covers
  same-project and foreign-project rows, active and archived timelines. A
  pre-existing identity is accepted only when the immediately previous
  accepted carrier and exact prior live row prove the same timeline/project,
  object identity, and role; otherwise acceptance refuses atomically.
- The projected snapshot starts from all live target-timeline rows, removes
  only IDs in the previous carrier, and applies the desired rows in sorted ID
  order. Unrelated references survive. Removal deletes the state row and live
  row only under the prior object/role/timeline/project predicate; a missing
  row is a safe no-op rather than an unrelated delete. The inverse-shaped
  Agent carrier therefore cannot remove another row or media object.
- Preflight happens after normal closure/raw-capture validation and before
  `_persist_closure`; projection, `timeline_revisions.references_json`,
  receipt/event publication, head movement, and timeline version update share
  the existing acceptance transaction. A projection refusal rolls back all
  externally visible acceptance state.
- The existing ledger lookup remains first in Runtime acceptance. Exact retry
  after restart returns the original receipt without provider execution or a
  second projection. The projection is version-checked at application time,
  and the candidate retains the Agent’s existing created-ID, binding,
  read/selection, role, ordering, and guarded inverse/rebase machinery.

## Agent source cohort for later freeze

The complete source-only cohort suitable for a later freeze is the `85c90d526`
tree `4acbb9d…`, consisting of the reviewed `d1f5` parent-reference source
and the current-floor `85c` composition of that source with `track.reorder`.
The reference implementation file is byte-identical between `d1f` and `85c`;
`85c` adds the current schema/registry composition and strengthens the
reference proof with authoring-candidate compilation, document reload, and
ordinary-asset same-ID refusal. The source cohort is not the current
integration HEAD `04fdd642…`, which does not contain the d1f/85c reference
source. No freeze authorization is implied.

Live source callers changed in the cohort are the Agent operation registry and
commit-provider raw-capture branch (`commands.py` and `commit.py`); no App,
Runtime, generated client, public endpoint, schema artifact, pin, generation,
or external product caller changed for this review. There are no additional
live callers to qualify.

## Evidence

Reused exact-tree bounded evidence from the prior source handoffs; I did not
rerun already-green custody/HTTP suites and did not run a full suite:

- Agent d1f reference/conformance and neighboring parent-media tests:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_reference.py tests/editing_conformance/test_recipe_m2_parent_media.py`
  — **91 passed**.
- Agent d1f schema composition/current-union/materialization tests:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py`
  — **61 passed**.
- Agent source lint: bounded `ruff check --no-cache` over the reference
  implementation, commit provider, schema tests, and conformance test —
  **all checks passed**.
- Runtime 449 projection tests:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/test_timeline_unplaced_reference_projection.py`
  — **4 passed**.
- Runtime bounded projection/closure/catalog neighbors — **21 passed, 4
  deselected** and **17 passed, 12 deselected**, respectively.
- The four HTTP history cases were run by the central service on the exact
  Runtime tree: **4 passed in 5.03s**. No full, renderer, browser, live-socket,
  generated-client, schema-generation, pin, or release suite was run.

## Limitations and next step

The normal generated Agent provider plus Runtime f53/449 acceptance path has
not been qualified. The original strict positive remains open and must later
prove owned raw capture, unplaced projection, restart-safe exact retry,
inverse removal/restoration, and occupied-ID refusal through the normal pair.
That future qualification must retain the existing carrier and must not turn
this source review into a freeze or public adoption claim.
