# Runtime D04/WC10 current consumer frontier

Status: **held; no Runtime deletion is safe on this frontier.** This is a
read-only production-caller investigation. No Runtime/App/Agent source,
tests, schemas, generated clients, pins, or route behavior were changed.

## Source read

- Runtime worktree: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- Agent integration: `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`, tree
  `075339b2c6d5e57c1b0e76754457d053b51edf2c`.
- App integration: `1557c312b999ddc0a21c1728acbc64052ef6491f`, tree
  `cf94daef960fe1426f6f50e4000b00c0fc42867e`.
- Current manager STATUS files, Runtime D04/WC10 ledger, the original
  runtime/App reports, and the current peer handoffs were read.

## Current production callers

### Runtime owner

There is no Runtime-owned production caller. Runtime owns the route and its
implementation:

- `runtime_protocol/server.py:582-584` dispatches the POST
  `/v1/projects/{project}/timelines/{timeline}/composition-revisions` route.
- `runtime_protocol/service.py:2779` implements
  `publish_parent_composition`; the current source still performs the legacy
  publication body rather than refusing it.
- Generated client methods and Runtime fixtures/tests are surfaces or test
  callers, not product consumers.

The existing replacement is `/v1/.../timelines/{timeline}/commit`, handled by
`RuntimeService.commit_timeline` and the installed Agent provider. Removing
the route now would break the live peer callers below.

### Agent owner

The current Agent source has these live production paths:

1. **Empty timeline creation** — `astrid/sdk/remote.py:482-551`, with the
   direct call at `:535-537` from `RemoteTimelines.create_empty`. This creates
   the Runtime shell, then publishes an empty parent with `expected_head: null`.
   The existing replacement is Runtime `create_timeline` followed by Agent
   native `timeline.init`/registered `EditCommand` commit through
   `WorkspaceClient.commit_timeline`. It is not cut: the installed launcher
   result `4406` is only the normal installed-carrier prerequisite, and the
   later corrected runner stopped at the existing mutation-envelope mismatch
   before provider bootstrap/canonical-read qualification.

2. **Single parent-media replacement** —
   `astrid/sdk/remote.py:1211-1425`; the `_Writer` calls
   `publish_parent_composition` at `:1405-1419`. The CLI path is
   `astrid/packs/timeline/cli.py:_cmd_replace_parent_media`. The existing
   replacement is the scoped native `clip.swap-media` /
   `occurrence.swap-media` command and existing media-selection reads, but the
   Agent WC3 row remains held: the original raw-parent/occurrence positive and
   its lost-ACK/wire assertions are not yet closed by the current candidate.

3. **Checkout/whole-document publication** —
   `astrid/sdk/timeline/store.py:305-355` (`publish_bundle`), reached by
   `astrid/sdk/timeline/publish.py:_PublishMixin.publish` and its narration
   follow-up. The `_Writer` calls the legacy method at `store.py:346-352`.
   The existing replacement is `TimelineSession`/NativeSheet command capture
   and commit. Only qualified attached/native slices have moved; detached,
   mixed, and unsupported whole-document edits remain live (Agent WC7/WC8).

4. **Producer whole-candidate publication** —
   `astrid/sdk/authoring_remote.py:297-312` (`TargetBoundAuthoringBundle.publish`)
   calls `publish_authoring_candidate`, whose writer contract reaches the same
   legacy method. The current in-repo producer replacement is the settled
   proposal shape: immutable media/data producer emits commands and the
   requesting client commits them. That producer/requester cut is not yet
   qualified, so this is a live caller.

5. **Document-script whole-candidate publication** —
   `astrid/packs/rendering/docs/scripts/timeline_document.py:89-98,216-219`
   publishes a prepared candidate through the same legacy writer. Its
   replacement is proposal plus requester commit; the Agent WC6 row remains
   held pending preservation of the original publication positives.

`astrid/core/timeline/shot_composition_migration.py:1030-1040` retains a
dynamic migration port requiring `publish_parent_composition`, but there is no
current in-repo production call site for `migrate_shot_compositions`; it is a
public migration seam, not evidence that a live product caller has vanished.
`astrid/core/dev/reference_realm.py:99` is a dev/reference fixture and is not
counted as production.

### App owner

The qualified native bootstrap is distinct from ordinary save migration:

- `src/integrations/runtime/createDefaultTimeline.ts:56-64` now calls
  `RuntimeDataProvider.initializeNativeBootstrapTimeline`, which uses the
  existing create/history/immutable-read ports and `/commit`; it no longer
  calls `publishParentComposition`.
- App native bootstrap qualification `real7782` passed the create/init,
  lost-ACK, reload/restart, history, and immutable readback assertions. The
  activation merge is App `1557c312` (r24). This proves the initializer path,
  not all App publication consumers.

Two live App production callers remain in `src/integrations/runtime/dataProvider.ts`:

1. `:295-300`, the shot-composition provider `publish` implementation. It
   serializes the graph with `toRuntimePublication` and calls
   `publishParentComposition` for shot-composition saves.
2. `:1131-1142`, `saveTimelineInOrder`, the ordinary editor snapshot/config
   save path. It sends the whole parent composition through the same client
   method and remains the fallback writer for consumers not yet producing
   commands.

`src/integrations/runtime/client.ts:722-734` and `generated.ts:162` are
   transport surfaces, not additional callers. The existing replacement is
   App command/outbox `commitTimeline`, including the native bootstrap helper;
   it is not yet wired for these two general save families. Therefore the
   qualified bootstrap does not authorize a Runtime route cut.

## Next deletion step

There is no narrow dead Runtime wrapper to delete now. The next bounded step
is a **peer-owned consumer cut**, not a Runtime route edit:

- Agent: qualify and cut one exact remaining caller, starting with
  `RemoteTimelines.create_empty` through the existing create + native
  `timeline.init` commit seam, while preserving the original empty-timeline
  and first-clip positives and adding direct no-legacy traffic proof.
- App: after native bootstrap activation, qualify one exact `dataProvider`
  save family through existing command/outbox commit; do not claim the whole
  App row until both the shot-composition `publish` and ordinary
  `saveTimelineInOrder` callers are migrated.

Only after those peer cuts and the remaining Agent WC3/WC6/WC7 whole-candidate
consumers are qualified should Runtime delete
`service.py:publish_parent_composition` and the POST dispatch. Until then,
keep D04/WC10 **held** and make no DELETED claim.

## Evidence limits

No tests were run, per the read-only brief. Static source/line tracing and
existing recorded results were used; no new qualification, route rejection,
or full-suite claim is made.
