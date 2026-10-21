# Agent transcript Main caption/review reconciliation

Date: 2026-10-21

## Result

The Agent `transcript.associate` source recipe now carries the existing App
known-reference reconciliation. The persisted source carrier remains exactly:

```text
parent.config.bundle.transcriptReferences
parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]
```

No alternate parent-level carrier, serializer, DTO, store, operation, schema,
Runtime generation, pin publication, or activation was added.

## Reconciliation boundary

`reconcile_transcript_references()` is pure. It maps only the exact App legacy
source ID spelling to the exact canonical `(asset, source, segment)` spelling,
and only for the selected asset/source and existing source-item membership. It
uses the App host FNV-1a/64 caption fingerprint and the App's exact generated
caption provenance (`track`, extension, contribution, schema, contract version,
and source item). Caption ownership is resolved through the selected asset's
paired media clip, so the real no-`asset` caption shape is covered.

It changes only the generated caption ID/provenance and the matching
transcript-lane review key/value. Caption text, style, timing, review status,
review payload, unknown metadata, and other namespaces remain unchanged. A
destination collision, duplicate source identity, ambiguous source mapping,
ambiguous shared review, or ambiguous caption ownership refuses before the
association/source writes. The operation records leaf writes for the nested
bundle planes, the affected parent clip collection/mirror, and the transcript
lane namespace; it never replaces the whole parent/config/bundle.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q \
tests/editing_conformance/test_recipe_film_transcript_association.py \
tests/editing_conformance/test_recipe_film_transcript_association_spike.py \
tests/sdk/test_scene_save_core.py::test_real_save_paths_need_neither_scene_imports_nor_node
=> 22 passed

/home/user/work/venv-agent/bin/ruff check \
astrid/sdk/timeline/native_transcript_association.py \
tests/editing_conformance/test_recipe_film_transcript_association.py
=> All checks passed

git diff --check
=> passed
```

The compact Agent fixture mirrors the existing App identity fixture and proves
the no-`asset` generated caption, preserved output/review fields, nested
serialization, inverse, leaf-write paths, destination collision refusal, and
shared-review refusal atomically. The existing App Vitest helper test was
identified at `src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx`,
but could not be run because neither App checkout has `node_modules/.bin/vitest`;
no dependency installation or shared-dependency mutation was attempted.

No full suite, Runtime suite, live socket/browser suite, Node-based production
save, generation, pin, activation, or App/Runtime integration qualification was
run or claimed.
