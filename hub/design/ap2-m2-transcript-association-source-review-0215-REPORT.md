# M2 transcript association source review

## Verdict

**EXECUTABLE MISMATCH — do not issue a SOURCE ACK.** The exact Agent source has
good pin and identity guards, but it does not address the App persisted carrier
and can miss a real App caption/review reconciliation case. Keep the existing
`project-transcript-host.associate` snapshot writer and catalog/document CRUD in
place.

## Exact source and consumers reviewed

- Agent successor: `e83d8fc5b609e34b692cfcb9185d2594fa0706b5`, tree
  `44735e9ce6b3f9c20a61c9f56e165c85af3ad327`, parent
  `4b784c3f90a5c3f5233e564721e734ce99bf3738`.
- Operation: `transcript.associate`, selector
  `parent/asset:<asset-id>`, closed args `asset_id`, `media_id`, `source_id`,
  `document`, `previous_document`, and
  `source_schema_ref = astrid.transcript_segment/v1`.
- App consumer reviewed at App `692765846fef511047445fecef3e55ec8bb6a5bf`,
  tree `e615c0a3aafca34504ba3544560de3887e4de38d`, especially
  `project-transcript-host.ts:600-651`, `projectTranscript.ts:184-207`,
  `reconcileTranscriptReferences.ts:66-147`, and the Runtime provider’s
  bundle save/reload paths.
- The old App2 recipe request is the bounded film association request in
  `peer-app2-to-agent-20261021T0042-transcript-and-system-source.md` and
  `app-ap2-m2-ordinary-artifact-boundary.md`.

## What matches

- **Pins and project scope:** Agent requires an exact three-field transcript
  `DocumentPin`, hydrates both new and prior pins, checks kind, document ID,
  version, content digest, project ID, transcript schema, canonical
  `(project, media, source)` identity, and refuses a replacement without the
  matching prior pin. This is the right shape for App’s deterministic
  `transcript:<hash>` document IDs and existing project-document owner.
- **Owner/media/source guards:** Agent binds `parent/asset:<id>`, checks the
  selected registry media identity, and checks document media/source against the
  command. App performs the same media ownership check before association.
- **Ordered identities:** New segments and words must have unique stable IDs,
  bounded timing, and word intervals inside their segment. Projection preserves
  document order and stable IDs. Existing source rows are selected by ordered
  `(asset, source, item.id)` membership and retained in order; unrelated schema
  collections and opaque parent/source values are copied.
- **Refusal atomicity:** The Agent handler checks reconciliation before its two
  `ctx.write` calls. Its focused test confirms the caption-refusal input bundle
  is unchanged. No association-only write is followed by a source write.
- **History shape:** The source records exact new/prior transcript dependencies,
  source selection, owner/segment/word bindings, and bounded writes. Its pure
  source tests cover inverse, replay/rebase-shaped preservation, and simulated
  restart pin retention. This is not accepted Runtime/App qualification.

## Mismatch 1: wrong persisted carrier and field name

The App’s real wire carrier is:

```text
parent_composition.config.bundle.transcriptReferences
parent_composition.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]
```

`RuntimeDataProvider.saveTimelineInOrder()` publishes `config.bundle`; both
reload paths read `config.bundle` and return it as `LoadedTimeline.bundle`; and
`useTimelinePersistence` builds the wire envelope with `itemsBySchemaRef`.
The App host’s `sourceItemsBySchemaRef` is an internal DTO name, not the wire
field name.

The Agent implementation’s `_source_paths()` only searches `parent`,
`parent.config`, and `parent.bundle`, and only for
`sourceItemsBySchemaRef`/`transcriptReferences`. It does not search
`parent.config.bundle` or the wire key `itemsBySchemaRef`.

Exact executable probe against the frozen Agent commit, using the actual App
wire shape, produced:

```text
actual_app_nested_bundle_unchanged= True
actual_app_nested_association_count= 0
actual_app_nested_source_count= 0
unexpected_root_fields= ['sourceItemsBySchemaRef', 'transcriptReferences']
root_source_count= 1
```

This is a data-visibility failure: a normal App save/reload would continue to
see no association or source rows and the operation would leave a second root
carrier behind.

Smallest correction: make the native carrier operate on the exact canonical
parent path and wire names (`config.bundle.transcriptReferences` and
`config.bundle.itemsBySchemaRef`), or introduce one explicit canonical
normalization seam that is proven to serialize to those exact fields. Add a
matched nested-bundle save/reload regression before any App migration. Merely
adding `config.bundle` while continuing to write `sourceItemsBySchemaRef` is
insufficient.

## Mismatch 2: reconciliation refusal misses App caption shape

The Agent’s `_reconciliation_needed()` only examines generated caption clips
whose own `clip.asset` equals the selected asset. The App’s generated caption
clips are text clips without an `asset` field; ownership is established by the
paired media clip and the caption fingerprint. The App identity control at
`importTranscriptIdentity.test.tsx:210-241` proves the legacy-to-canonical
caption and review-key rewrite for this shape, while the fixture’s caption clip
has no `asset` (`:97-122`).

An exact-source predicate probe removed `asset` from the Agent test caption
clip and the operation succeeded instead of refusing:

```text
caption_without_asset_refusal= not reached
operation_succeeded= True
```

For a real legacy-to-canonical mapping this can accept the association/source
replacement while the App reconciler would need to rename the caption clip and
review key. That violates the settled requirement that unsupported
caption/review reconciliation refuse before any write and preserve the whole
draft atomically.

Smallest correction: reuse the App reconciler’s exact generated-caption
ownership/fingerprint predicate, or conservatively refuse any affected
generated caption/review provenance regardless of `clip.asset` until that
reconciler is carried. Record the exact config/review reads in the same guarded
command. Do not guess by array position or add a second caption authority.

## History, reload, redo, and opaque limitations

The Agent source-only tests pass pure inverse/replay and simulated pin-cache
loss, and preserve retained source/root opaque values. They do not prove an
accepted Runtime revision, accepted dependency closure after document removal,
normal App serialization/reload, or actual film-association redo. The App’s
focused source-document undo/redo tests are catalog CAS behavior, not proof of
this proposed film command. No generated client, Runtime DTO/store/endpoint,
App activation, pin, release, deletion, browser, socket, or full suite was run.

The App focused controls do confirm the current consumer behavior and carrier:
`project-transcript-host.test.ts`, `importTranscriptIdentity.test.tsx`, and
`dataProvider.test.ts` together passed 104 tests, including source identity and
the nested `config.bundle` publication/reload witness. The exact committed
Agent source files and schema/floor controls passed 46 tests (with two
environment warnings about unsupported pytest timeout config). These green
results do not close either mismatch.

## Exact test commands

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx src/integrations/runtime/dataProvider.test.ts
=> 3 files, 104 tests passed
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private archive of e83d8fc5>:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/editing_conformance/test_recipe_film_transcript_association.py tests/editing_conformance/test_recipe_film_transcript_association_spike.py tests/sdk/test_timeline_current_union_schema.py
=> 46 passed in 124.28s; 2 PytestConfigWarning warnings
```

No App files or shared dependencies were modified. Recommended next step is a
small Agent source correction and exact nested-wire plus no-asset-caption
refusal controls, followed by a matched Agent/App/Runtime save/reload/undo/redo
qualification. Until then this remains an executable mismatch, not an ACK.
