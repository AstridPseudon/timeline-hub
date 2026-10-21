# Agent RT03 owned raw/unplaced reference source handoff

Status: source-only, ready for peer review. This handoff does not change
Runtime, generate a schema artifact, publish a package, freeze a public cohort,
or activate a pin. The original Runtime strict positive remains open until the
paired Agent/Runtime acceptance path proves it.

## Exact source

The interrupted source branch was resumed at `96d5d94aa0ccc8a5fe7007e24441a90ff9a19551`.
The tracked working-tree patch over that WIP source has SHA-256
`579a02837e88e83d71032eacb1dbb21f67bc8ee83c9d609b854740e5906f4eea`.
The focused new conformance file is untracked until the harness commit and has
SHA-256 `52f4a93c9bfde8d4ec2a88c8b51061044b94cce40611dcb35ed4072b3c421cb4`.

Relevant final file hashes:

```text
38cae7f71344bdede54af9d25ebc8b34a1abe65efb77d345fe816e94615727dc  astrid/sdk/timeline/native_parent_reference_commands.py
905c2a806e1f95d9c7699a2bdadaed7ff0a6e1e6c918d3ac4465467d5b7185e1  astrid/sdk/timeline/commands.py
0cca0d16f308ca24e8f839f9d100c02bdc6dc3ae93fc2312891b1c88184b821d  astrid/sdk/timeline/commit.py
dba458065c560eb5fada2531743cae30cf1f7463fa4e4dbec3993a281f096734  astrid/core/timeline/schema/edit-command.schema.json
52f4a93c9bfde8d4ec2a88c8b51061044b94cce40611dcb35ed4072b3c421cb4  tests/editing_conformance/test_recipe_m2_parent_reference.py
90a0810b0ea2d7e4210bf009d77008fa970b1bba700bb40b8febde872eed7cdc  tests/sdk/test_timeline_current_union_schema.py
230e3f66fa7f02ba135d75ea6ab3c21a198563a905120cc390a37c497d1702cb  tests/sdk/test_timeline_materialization_schema_union.py
df3c88dbc18a8bfe28d83a8813849307815d8460a3e1f000a69e41a59fe0349a  tests/sdk/test_timeline_composed_schema.py
```

## Closed Agent behavior

`timeline.reference` v1 is parent-scoped and accepts exactly an opaque
`reference_id`, the literal role `source`, and the existing
`MediaManifestEntry` pin `{media_id, content_digest}` with equal SHA-256
digests. Its handler:

- requires an exact request-scoped `raw_media_info(pin)` result when the
  optional port is present; missing capture, missing metadata, mismatched
  object identity, or invalid media metadata fails closed;
- writes one namespaced parent leaf at
  `config.app.astrid.timeline_references[reference_id]`;
- reserves the same stable identity through the existing parent asset registry
  birth, preserving direct/config registry mirrors and exact container
  presence for inverse;
- records the exact media dependency and absent destination/registry guards;
- creates no occurrence, shot, clip, track, placement, catalog row, or managed
  five-field selection; raw `MediaInfo` never enters authored state; and
- relies on the existing recorder/rebase/inverse machinery for replay,
  identity collision refusal, ordered batch births, inverse, and redo.

`document_from_bundle` derives the existing dependency manifest from the raw
pin, and `bundle_from_document` round-trips it without introducing a new
manifest type. Existing frozen schema floors remain byte-identical when the
new source-only operation is explicitly stripped; the live closed union and
schema golden include `timeline.reference`.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_m2_parent_reference.py \
  tests/editing_conformance/test_recipe_m2_parent_media.py
91 passed in 20.77s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_composed_schema.py
61 passed in 173.09s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache \
  astrid/sdk/timeline/native_parent_reference_commands.py \
  astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py \
  tests/editing_conformance/test_recipe_m2_parent_reference.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_composed_schema.py --output-format=concise
All checks passed.
```

The focused tests are unit/conformance tests with a fake verified-media
boundary only. No Runtime positive, restartable HTTP path, browser, live
socket, full suite, package generation, publication, or pin adoption is
claimed here. Runtime must independently review and qualify its
request-scoped raw custody and projection before RT03 is closed.
