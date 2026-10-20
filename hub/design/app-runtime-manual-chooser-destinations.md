# Runtime manual recovery destinations

Delivered a bounded read/presentation adapter on App base `5dbe9fa9da28a752a20d925d35bce1515b33162a`. Manual placement is still unavailable in the actual TasksPane because this source tree has no qualified native ADD command-service callback.

## Selected authority and existing UI

`TasksPane` supplies only its explicit Runtime editor project/timeline selection. `RuntimeRecoveryChooser` uses the existing `ShotSelector` inside the existing `MediaLightbox.customOverlay` seam. The dispatcher now forwards that already-defined overlay to image/video lightboxes; no shared selector API, global store or second selector implementation was introduced. Runtime mode continues to withhold the legacy shot workflow, including outside the editor where no explicit timeline is selected.

`loadRuntimeRecoveryDestinations` calls `RuntimeDataProvider.loadTimelineCommandBasis(timelineId)`. That existing provider verifies the current history head, scoped immutable parent/shot/internal reads, dependency manifest and closure identities. The adapter then calls the normal `getProjectTimeline` read and requires matching project, timeline, revision AND publication. It never resolves a project default.

Options come from raw parent occurrences, their exact shot revision links and exact internal revision images. The binding retains raw occurrence ID, shot/revision, internal timeline/revision, parent lane and child track separately. Parent tracks support the existing explicit `tracks` and `config.tracks` representations. Missing/ambiguous child images or tracks, missing parent lanes, conflicting occurrence lanes and inactive/nonvisual child tracks cannot produce guessed destinations. Shared shot occurrences remain separate choices; presentation does not certify that a native operation supports their ownership.

The chooser key is local presentation data, never a canonical ID or owner. No owner is reconstructed from a projected ID, shot ID or task params. Nothing is selected automatically. Timeline start and source-window endpoints are explicit seconds, initially blank; a complete draft requires finite nonnegative values and a positive source window.

## Exact media and lifetime

`useTasksLightbox` retains a deep-frozen copy of the opened task, managed association and exact existing five-field Runtime media selection (`asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`). The selected lightbox variant never supplies placement identity. The object digest never supplies a generation ID.

The local chooser retains that source alongside its frozen verified basis and explicit destination/timing selections. Every five seconds it rechecks the task, managed output, selection and selected timeline closure/head. A changed head keeps the old draft and makes it unavailable rather than silently rebasing it. A changed task/output/selection also makes the draft unavailable. A prospective callback request rechecks current source and head again, compares all tuple fields and fences pending reads against selection edits. Scope/source replacement remounts the local draft; project/timeline/task/output changes and unmount invalidate pending work. Callback errors retain the chosen destination and timing. No accepted/placed state is synthesized.

The existing recovery surfaces, provenance labels, normal output reads, gallery links, task inspect/export/cancel/retry and non-Runtime lightbox workflows are preserved. Modern generation intents remain excluded. Unknown placement remains unconfirmed; only the existing proven retirement marker labels an output not placed.

## Exact native callback / tuple blocker

There is **no actual native ADD callback wired in this branch**. `RuntimeRecoveryChooserProps.onRequestPlacement` is an optional **local typed routing seam**, and `RuntimeRecoveryPlacementDraft` is local routing data, not a Runtime DTO, command, authority or new endpoint. TasksPane does not pass it. Tests supply a recording callback only to verify preserved routing data. Those tests do not demonstrate manual placement or canonical acceptance.

`RuntimeDataProvider.commitTimeline` is generic command transport, not a qualified native ADD capture service. The existing `useShotActions` / `useAddImageToShot` / `placeGeneration` path resolves a default timeline and uses the snapshot writer; it remains disconnected from Runtime recovery. No fallback, fake success, notification placement or auto-approval was added. Writer retirement is not claimed.

Next integration requires the matched native ADD/ownership-guard release and the App service that accepts the frozen basis plus exact media tuple and explicit raw owner/child-track/timing, captures the supported native command and submits through the existing command session. The manager must select/qualify that port on the matched App/Agent/Runtime tuple, then qualify the real browser pair. Image/video support, shared ownership and source-window interpretation belong to that qualified native port, not this read adapter.

## Evidence and limits

245 targeted tests passed in 19 files: all 202 prior cases, 30 new chooser/provider cases, one new TasksPane wiring case and 12 lightbox neighbours. The chooser tests use the real RuntimeDataProvider and normal in-memory Runtime read transport. They reuse the actual Runtime `generation.publish_v1` fixture already captured in `runtimeRecoveryGeneration.json`; timeline closures come from the existing accepted-command fixture. The ShotSelector and MediaLightbox dispatcher are real; image/video leaf lightboxes are mocked in the new routing tests. A recording callback proves only routing data and race refusal.

ESLint and `git diff --check` passed. No full suite, build, tsc, browser, install or socket was run. The active full run was not disturbed. All dependencies stayed read-only; Vitest used runner config loading, `--no-cache`, one worker and a private cache path. Exact commands, results and logs are in the worker notes report below.

Worker report: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-runtime-manual-chooser-destinations/notes/report.md
