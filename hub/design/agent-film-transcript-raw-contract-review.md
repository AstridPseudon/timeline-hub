# Agent film transcript raw-contract review

## Verdict

**COUNTEREXAMPLE — DO NOT APPROVE.**

The reviewed source prototype is not writing the actual persisted Main/App
canonical carrier. It writes test-local top-level parent fields, while the
real App serializer persists the source plane at
`parent_composition.config.bundle` and the normal App reload reads that nested
bundle. Therefore the prototype does not establish that a normal serialized
App reload sees either the association or the source items.

Reviewed Agent tree: `e83d8fc5b609e34b692cfcb9185d2594fa0706b5` (`e83d8fc5b`,
`feat(timeline): record bounded transcript associations`). The exact producer
handoff reviewed was
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-ordinary-transcript-native-recipe-source-REPORT.md`.
The App source read was tree `bebadd0e1283753e3805c2d61688e3dee8b929e2`.

## Concrete carrier mismatch

The Agent implementation's `_source_paths()` only searches `parent`,
`parent.config`, and `parent.bundle` (`astrid/sdk/timeline/native_transcript_association.py:27-42`).
It never searches `parent.config.bundle`. Its writes at lines 300-301 therefore
target top-level `parent.transcriptReferences` and
`parent.sourceItemsBySchemaRef` when given the real App-shaped parent.

The real App path is different:

- `RuntimeDataProvider.saveTimelineInOrder()` takes the bundle argument and
  places it under `parentComposition.config.bundle`
  (`/home/user/banodoco/reigh-app/src/integrations/runtime/dataProvider.ts:787-810`).
- Both normal reload paths read `configRecord.bundle`, validate it, remove it
  from the config DTO, and return it as `LoadedTimeline.bundle`
  (`dataProvider.ts:658-672` and `681-699`).
- `useTimelinePersistence` constructs that wire bundle from the assembled
  `TimelineData` fields (`useTimelinePersistence.ts:956-967`), and the
  `TimelineData` comments explicitly describe `sourceItemsBySchemaRef` as
  fields carried from `LoadedTimeline.bundle`, serialized in the bundle
  (`timeline-data.ts:110-118`). These are projection/DTO fields, not the
  persisted parent location.
- The existing App producer mutates those DTO fields before the save boundary
  (`project-transcript-host.ts:610-648`), which is then wrapped into the
  persisted bundle by the save path.

Bounded in-memory probe, using the reviewed Agent operation against a parent
whose source planes are in the actual nested `config.bundle` shape, produced:

```text
nested_bundle_unchanged= True
nested_bundle_association_count= 0
top_level_association= [{'assetId': 'asset-a', 'documentId': 'transcript:ec062dcd5ce205fa34c8520b908bd719721e3c6573d5c4a7d5e4577276338e7f'}]
top_level_source_count= 1
roundtrip_nested_bundle_unchanged= True
```

This is a direct data-loss/visibility counterexample: the accepted plan leaves
the actual persisted bundle unchanged and adds a second, non-App carrier at the
parent root. A normal App serializer/reload will continue to see zero
association/source items. The existing App provider test states the positive
wire/readback witness explicitly: `dataProvider.test.ts:404-424` expects the
publication at `parent_composition.config.bundle` and the reopened provider's
`loaded.bundle` to equal it.

## Contract checks

- New and prior `DocumentPin` hydration is present in the Agent source path
  (`commit.py` hydration handles both `document` and `previous_document`), and
  the source-only tests cover exact prior-pin capture. Runtime accepted
  closure retention and restart/reload retention are **not witnessed**.
- Stable segment/word IDs, source ownership, order, opaque preservation,
  canonical Agent document roundtrip, inverse/replay, and atomic unsupported
  caption/review refusal are covered by the worker's 14-test production slice
  and 42-test source/spike/schema run. Those are pure Agent/source-only tests,
  not native App/Runtime evidence; the prior 14+34 pass claim must not be
  promoted to native qualification.
- The schema change is additive to the current source schema (one operation
  and one args definition); the historical S2 floor explicitly removes this
  unfrozen prototype and the worker reported the 34-test compatibility file
  passing. This does not repair the carrier mismatch.
- Caption/review reconciliation remains an explicit refusal, so the old
  caption-positive/reconciliation path remains open as required. No positive
  native film association, App producer migration, Runtime accepted command,
  or generated-client qualification is claimed.

## Evidence run here

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association.py
=> 4 passed in 0.74s
```

The bounded nested-carrier probe above exited 0. A targeted App Vitest attempt
was not runnable in this checkout because `/home/user/banodoco/reigh-app` has
no `node_modules/.bin/vitest` (exit 127); no dependency installation was
attempted. No full/native/live/browser/socket suite was run.

## Required next witness

Do not ACK this prototype as native. The smallest missing witness is a matched
Agent/App/Runtime capture using the real `config.bundle` carrier, followed by a
normal `saveTimelineAtHead` publication and fresh App `loadTimeline` reload
showing the same association and source-item order/opaque payload. The same
matched fixture must prove accepted-history inverse/replay retains both the new
and prior exact `DocumentPin` sources across document removal/restart. Until
that witness exists, no new wire/DTO/store/projection or alternate hash
authority should be added, and the existing snapshot writer must remain open.
