# Agent WC6 same-alias native continuation

## Result

The document adapter now publishes an original same-alias media replacement
through the existing private `occurrence.swap-media` command. The strict
positive hold was removed only after the original stale-head publication
assertion passed unchanged. The old registry alias remains in place; the
managed media binding and bounded authored payload mirrors are rebound to the
new exact Runtime-selected object.

The implementation is private and does not change the public pin or generated
contract. The current source floor remains the existing private S3 / 55
definitions / 29 operations, while the public S2 contract and the next
ordinary 55 floor are untouched. The exact existing operation used is:

```text
occurrence.swap-media v1
select: occurrence:<occurrence-id>/clip:<clip-id>
args: {old_media: MediaSelection, media: MediaSelection}
```

No new HTTP DTO, table, endpoint, source factory, root replacement, or
fallback writer was added.

## Bounded behavior

- `occurrence.swap-media` detects `old_media.asset == media.asset == target.asset`
  and treats it as a rebind. It validates every clip consuming that alias for
  kind and source-window compatibility before writing anything.
- The registry writes only `media_id`, `type`, `generationId`, and `variantId`
  at the existing `owner/asset:<alias>` record. Labels, opaque fields, order,
  and unrelated aliases remain untouched.
- Known child-shot payload mirrors (`items`, bounded `assets`/`source`, and
  `audio_bindings`) are updated with recorded leaf writes. This preserves raw
  materialized item identity on inverse/reload.
- The same-alias adapter path requires one explicit placement owner, exact
  old/new generation+variant pins, and Runtime `MediaSelection` plus
  `VerifiedMedia` reads. Missing or ambiguous scope remains a visible draft
  refusal.
- Imported media now carries the Runtime generation/variant receipt back into
  the same registry alias. No alias is renamed and no registry is copied into a
  new root.
- The existing generic state recorder now supports recorded list-member leaf
  writes, needed for the bounded payload mirrors; inverse and ABA guards remain
  the existing recorder/inverse machinery.

The adapter still explicitly holds narration/text and unsupported document
structure changes. This closes the same-alias media slice only; it does not
claim whole-WC6 closure.

## Verification

Local focused neighbors:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py
145 passed, 1 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_timeline_document_checkout_scope.py tests/packs/timeline/test_cli_native.py tests/editing_conformance/test_recipe_occurrence_media.py tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py
158 passed, 1 deselected
```

Additional checks:

```text
ruff check [all nine changed Python files]
All checks passed!
compile(Path(...), ..., 'exec') for six changed production modules
compile: ok
git diff --check
exit 0
```

The required central live Runtime lane for the existing normal
`WorkspaceClient`/`TimelineSession` reload–retry–undo/redo journey passed:

```text
agent commit-integration --files "tests/editing_conformance/test_commit_runtime_m1.py::test_normal_client_auto_placement_preview_restart_retry_inverse_and_redo[image-anchor]"
10 passed in 39.23s
```

The broader central occurrence-media integration request was run against the
supplied candidate and returned 10 passed plus 48 setup errors before the new
behavior could run. Its first failure is an existing candidate mismatch: the
Runtime archive at `/home/user/work/runtime` lacks `_binding_descriptor` from
`timeline_commit_film_fixture`. A diagnostic test-only local helper (not kept)
then reached the candidate's retired `create_project_shot` direct-write route
before publication. No product fallback or Runtime edit was made, so actual
same-alias Runtime acceptance remains unverified against that lane.

## Remaining holds

The private native command and document adapter are ready for peer review, but
the ledger WC6 native IDs remain held until the real matching Runtime
generation/service and script publication→reload→undo→retry proof is rerun on
a compatible Runtime candidate. This worker is blocked on that external
candidate mismatch. Do not publish a new public pin from this worktree.
