# AP2 M2 owned overlay: Agent f83 source ACK

## Result

**ACK — source contract approved at the exact f83e6cb boundary.** This is a
read-only source review of the private Agent successor, not generated-schema,
native-pair, hosted-admission, activation, or App product approval. No App,
Runtime, generated artifact, DTO, API, provider, store, pin, or freeze change
was made.

## Resolved carrier and authority

The f83 change adds only optional `args.schema_source` to the existing
`clip.add` `ClipAddArgs`, typed as the existing closed `DocumentPin`:
`{document_id, version, content_digest}`. The project scope is supplied by the
existing Runtime `/v1/projects/{project_id}/...` path and Agent binding; App
does not add a project field or derive a digest from a document body.

For an owned overlay, the exact source/tree/schema tuple is:

```text
DocumentPin: containing project-pack document's exact id/version/content digest
elementRef:  exact {packId, id, kind, revision}; packId is not stripped
object:      the selected admission's exact snapshot_object.object_id
schema:      the retained snapshot validated by Agent's existing
             admitted_element_snapshot_descriptor()
```

`clip.add` remains parent-owned and literal. When `schema_source` is supplied,
f83 requires an owner-qualified `elementRef`, `kind == effect`,
`elementRef.id == row.clipType`, and an active visual output track. The existing
selected-schema path reads exactly one matching project-pack admission, then
the exact retained document/object; it records `params.schema`,
`params.snapshot`, and fixed `params.element` authority. The resolver checks
the same exact pin and owner/id/kind/revision on later PARAM and inverse paths.

This authority is not a browser hash, inline declaration, bare ID, latest
catalog choice, guessed owner, or local source/build cache. The frozen builtin
`2a9b...` and hosted descriptor `8e3a...` are different identities and were
not substituted.

## Proven behavior

- The born selected clip's P1 `clip.add` records the genuine source/object
  association, `add.track` binding, created clip ID, literal row, opaque
  fields, and parent order. Later `clip.set-params` preserves unmentioned
  params and explicit clears use the same P1 association.
- A source-only probe used actual project-pack admission fixtures: after a
  newer P2 admission became current and all live source entries were removed,
  P1 PARAM still succeeded from retained authority; supplying P2 instead was
  refused atomically. No fake config document or accepted envelope was made.
- Existing inverse/redo/delete and disjoint-rebase controls preserve the
  complete row and dependency manifest. The no-`schema_source` literal,
  unowned `clip.add` path remains unchanged.
- This does not authorize App to activate the path. Current App selected-pack
  capture still fails closed until the Agent-produced binding, verified
  schema input, retained snapshot, and scoped realm are carried through the
  existing seam.

## Evidence

Frozen f83 archive, source-only targeted controls:

```text
F83="$(find /tmp -maxdepth 1 -type d -name 'ap2-m2-f83-source-*' | sort | tail -1)"
PYTHONPATH="$F83" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  /home/user/work/venv-app2-native/bin/python -m pytest -q -rs \
  -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_builtin_overlay_authority.py \
  tests/sdk/test_timeline_selected_param_authority.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/editing_conformance/test_recipe_m2_clip_add.py
```

Result: **112 passed**, 2 environment warnings for unavailable pytest timeout
plugins. The additional inline pure probe passed
`born-selected-P1-after-P2-live-source-removal` and
`wrong-P2-pin-refused-atomically` using real temporary project-pack admission,
retained document/object inputs, and the detached provider.

Current App pure route controls:

```text
TMPDIR=/tmp/ap2-m2-owned-overlay-f83-source-peer-review-vitest \
  node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/commands/clipParamsCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts
```

Result: **5 files, 98 passed**.

No full, browser, localhost/socket, hosted admission, generation, dependency,
native-pair, or Runtime/App integration suite was run. The normal hosted
builtin `audio-reactive-colour` producer still lacks an admitted pin/snapshot
handoff; that is a producer gap, not a mismatch in the f83 carrier semantics.
