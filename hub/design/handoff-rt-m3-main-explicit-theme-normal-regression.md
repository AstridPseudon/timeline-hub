# Runtime M3 normal explicit Theme regression

## Corrected disposition

This is retained as historical red evidence, not a current SDK qualification.
The test-only branch `68465ef` is **ABANDONED**, along with its four stopped
dependents: `tl/rt-m3-main-theme-final-source-consumer-handoff`,
`tl/rt-m3-main-theme-final-source-custody-r2`,
`tl/rt-m3-main-theme-one-failed-positive-final`, and
`tl/rt-m3-main-theme-retry-atomic-gate2`. They are not integrated branches,
public test deletions, or gate passes. Preserve the one passing
foreign/tamper negative and the one red positive; do not merge or xfail the
fixture. The old custody REQUEST CHANGES is superseded because this raw
`params.timeline_ref` fixture was mistaken for a current SDK caller. No test
rerun or reviewer re-review is authorized; physical parity remains
Viewing-owned.

## Scope and source identities

This worker owns only `tests/test_timeline_explicit_theme_main_preservation.py`.
The test is based on Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
(tree `d3a290b407fa61e6ab2d476f50c068073f70df00`). The source trace follows
the owner ruling's Agent `497714c7` and App `860d43b3` Main paths. The current
normal Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / Runtime-95bd client
pair was not needed to seed this Runtime-only proof; no client, schema, pin,
or product source was changed.

The reviewed Main route is:

`media.import_file(theme.json)` -> project CAS descriptor
`{object_id,digest,filename}` -> render `inputs.theme` -> Runtime ordered
input admission -> claim -> GenericHost `theme.json` -> existing resolver.

Agent source anchors from the owner ruling are `astrid/sdk/remote.py:1543`,
`astrid/packs/rendering/actions/render/STAGE.md:128`,
`astrid/core/execution/generic_host.py:6899`, and the existing resolver's
`rendering_backend/__init__.py:89`; the Runtime managed freeze is
`runtime_protocol/store.py:_freeze_managed_render_inputs`.

## Test evidence

Added one positive and one bounded negative test using the existing
`canonical_scene` / `_publish` fixtures and Runtime's public `service.ingest`
CAS API. The authored bytes contain a distinct id, canvas, colors, font, and
generation sections; they are never used as an inline authority or fake
certificate.

Positive assertions cover:

- exact descriptor retention and exact authored bytes in project CAS;
- Main SDK input order: `[theme, canonical media..., snapshot]`;
- saved parent authority and Runtime-owned snapshot digest;
- claim and GenericPackHost materialization as `theme.json`, byte-for-byte.

The negative case imports a foreign-project Theme and tampers a same-project
descriptor digest. Both refuse visibly and preserve Runtime SQL, CAS, and
staging state exactly.

Commands/results:

- `python -m pytest -q tests/test_timeline_explicit_theme_main_preservation.py` — 0 nodes (Runtime default excludes integration; 2 deselected).
- `python -m pytest -q -m integration tests/test_timeline_explicit_theme_main_preservation.py` — **1 passed, 1 failed**. The refusal test passed. The positive failed at Runtime's existing `render input_object_ids do not match the canonical timeline registry` check: the genuine imported Theme ID is rejected as an extra input before claim/materialization. This is the intended product regression on 95bd, not a fixture failure.
- `python -m py_compile tests/test_timeline_explicit_theme_main_preservation.py` — passed.
- `python -m pytest --collect-only -q -m integration tests/test_timeline_explicit_theme_main_preservation.py` — 2 nodes collected.
- `git diff --check` — passed.

No product fix is present yet in the paired product worker worktree, so the
failed positive was not rerun. No full, browser, live socket, renderer, MP4,
default-five, old28, generation, pin, release, or schema suite was run.

## Remaining seam

The product worker must preserve the existing Runtime managed-render authority
while accepting the already project-associated named `theme` object in the
ordered input manifest. It must retain the descriptor, snapshot/parent
authority, project/CAS digest and size checks, claim binding, and no-write
refusals. No new Theme document, source-selection protocol, resolver, DTO,
private preparation mode, or default fallback is implied.

After that exact reviewed product source is committed, rerun only the failed
positive node once through the test service if the product path requires it;
the passed negative node remains valid evidence and should not be relabelled.
