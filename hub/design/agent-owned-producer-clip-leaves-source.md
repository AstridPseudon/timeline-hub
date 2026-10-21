# M2 producer clip-leaf source handoff

Status: source-only carrier is complete for peer review. No Runtime/App activation, pin, generated output, endpoint, DTO, store, or new operation is included.

## Exact source and tree

Worker base: `f448c4b40c60d08f4092e232688b0de99bb07243` (`d4508b9fa5db9b2a2774fc5acc811fc34814c53d`). The source changes are in:

- `astrid/core/timeline/schema/edit-command.schema.json`: the existing `clip.set` values object now has only these additive producer fields: top-level `label`; partial `text` leaves `content`, `fontSize`, `color`, `bold`, `align`; and partial `app` leaves `managedBy`, `__generated__`.
- `astrid/sdk/timeline/_clip_scalar_commands.py`: `clip.set` validates and writes those leaves without replacing `clip`, `app`, or `text` objects. Existing `clip.set` hold/clear behavior is unchanged.
- `tests/editing_conformance/test_recipe_producer_clip_set.py`: Main-shaped producer fixture and source-only capture/execute/reload/inverse/ownership tests.
- `tests/sdk/test_timeline_materialization_schema_union.py`: compact exact stripping guard for the new unfrozen source composition. Existing frozen floor hashes remain unchanged; the current source composition hash is `0b747d87c763a8f0ba0dcc5027390ab04d6296cfddfffa8c049020334ca3ec92` (JSON pretty-print plus final newline).

The schema is deliberately additive to the existing `clip.set` recipe; it is not a new op or a new schema definition. The `text` and `app` subobjects are closed at the carrier boundary. Existing opaque siblings in a stored row survive because execution writes nested known leaves only.

## Producer capture shape

For an existing managed clip, the source capture is the normal `clip.set` recipe. A representative exact shape is:

```json
{
  "schema_version": 1,
  "op": "clip.set",
  "version": "<capture_version>",
  "select": "parent/clip:f2-app-clip",
  "args": {
    "values": {
      "hold": 2.25,
      "label": "new caption",
      "text": {
        "content": "new",
        "fontSize": 48,
        "bold": true
      },
      "app": {
        "managedBy": "haus.astrid.transcript-lane",
        "__generated__": {
          "extensionId": "haus.astrid.transcript-lane",
          "contributionId": "render-as-video-text",
          "provenance": {
            "contractVersion": 1,
            "sourceSchemaRef": "astrid.transcript/v1",
            "sourceItemId": "caption-1",
            "sourceFingerprint": "astrid-fnv1a64-v1:source",
            "sourceRevision": "after",
            "generatorVersion": "1.0.0",
            "outputFingerprint": "astrid-fnv1a64-v1:output",
            "conflictPolicy": "regenerate-output"
          }
        }
      }
    },
    "clear": []
  }
}
```

`capture_clip_set` adds the normal expect/authorship records. It captures the existing `app.managedBy` and complete existing `app.__generated__` leaf as guards; no IDs are allocated and no `created` records are emitted. The fixture uses the real Main-shaped mirrored parent/config clip rows and preserves an opaque text sibling and opaque app sibling through execute and strict inverse.

## Guards and exclusions

- App leaves require an existing non-empty `app.managedBy`; user clips with no owner and foreign clips with another owner refuse atomically as `unsupported_ownership`.
- An incoming `managedBy` must equal the existing owner. An incoming generated metadata leaf must already exist and must retain the existing `extensionId`/`contributionId`; `extensionId` must equal `managedBy`. Optional fixed identity fields (`generatedAt`, `sourceMapEntryId`) cannot change. Provenance may change for regeneration. This permits refresh but never silent adoption or identity replacement.
- Text is leaf-wise and bounded to the five known Main leaves above. Unknown incoming text leaves refuse; unmentioned stored style/opaque leaves survive.
- Existing deterministic clip IDs are selected and updated in place. Fresh clip creation remains the existing complete `clip.add` path; this carrier does not invent IDs or change creation ownership.
- `hold` is the only timing leaf carried here. `at` and `track` remain the existing `clip.move` authority, including its quantization/track rules. A consumer must split a producer update into the existing move recipe plus this `clip.set`; do not put raw `at`/`track` into `values`.
- Main producer geometry (`x`, `y`, `width`, `height`) is top-level clip data, not params. It is intentionally not disguised as `clip.set-params`; use the existing params recipe only when the selected authority actually stores a field in params. This source carrier therefore refuses those geometry fields.
- Do not send whole `app`, `clip`, or parent objects, host metadata in params, generated output/pins, or source guesses. A batch containing unsupported leaves must be refused before submission.

## Validation

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_producer_clip_set.py
3 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py
113 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_producer_clip_set.py tests/sdk/test_timeline_materialization_schema_union.py -k 'producer or only_carrier_additions or removing_only_group_additions or removing_group_and_project_data or extent_proposal or private_remove or private_extent_floor or literal_three_union or voiceover_property or complete_reviewed_private_s2'
12 passed, 15 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py -k 'only_reviewed_producer_and_consumed_additions or next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions or all_published_floors_preserve_every_field_with_only_historical_pattern_widening'
3 passed, 31 deselected

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_producer_clip_set.py tests/sdk/test_timeline_materialization_schema_union.py
All checks passed!
```

No full or live-socket suite was requested, per task instructions. App2/Runtime should consume this exact source shape and ACK before activation.
