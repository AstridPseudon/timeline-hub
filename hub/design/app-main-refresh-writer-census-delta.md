# App upstream44f writer census delta

Date: 2026-10-20  
Scope: owner/new main `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` versus old `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2`, reconciled against refreshed App `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7`.

## Result

No new App canonical authored-timeline writer was introduced in the bounded upstream delta, and no existing one was deleted. All current D01 rows remain OPEN until native qualification. The refresh unifies the default editor onto the canonical Runtime route, relocates existing bootstrap/rename/primary callers, and hardens project/timeline identity resolution; it does not make UI reachability, Runtime `410`, media import, relational effects, or chat metadata evidence of writer retirement.

The supplied PLAN one-writer policy, current `app-writers.md`, and `deletion-ledger.app.md` are the settled sources; no extra artifact was required and the ledger was not altered.

## Main-before / refreshed-after evidence

The exact old→main diff contains 270 paths: 245 modified, 15 added, 8 deleted, and 2 renamed (`WorkspaceConnectionRecovery` → `RuntimeConnectorRecoveryBanner`, test and source). The source-only inventory used `git diff --name-status --find-renames=50% old main`, `git diff --shortstat old main`, and scoped `rg` over only those changed paths.

| Concern | Old `60aa` evidence | Refreshed `35db` evidence | Classification |
|---|---|---|---|
| Empty/bootstrap parent | Existing `createDefaultTimeline.ts` `publishEmptyTimeline` / `createCanonicalTimeline` / `ensureProjectHasTimeline`; existing callers in `useProjectCRUD.ts:165`, `VideoEditorPage.tsx:1009,1096` | `createDefaultTimeline.ts:60,84,104`; callers `useProjectCRUD.ts:154`, `VideoEditorPage.tsx:477,567` | Canonical parent bootstrap plus Runtime project-default metadata. Existing `D01-app-bootstrap`; no new writer. |
| Default editor timeline rename | Runtime-branch caller `VideoEditorPage.tsx:1331` | Unified caller `VideoEditorPage.tsx:716-721`, presentation dialog `ProjectTimelineSelectors.tsx:373-439` | Timeline metadata `name` mutation, not authored composition/registry state. Existing behavior relocated, not a new snapshot writer. |
| Primary timeline | Existing `dataProvider.setPrimaryTimeline` caller in the split editor branch | `VideoEditorPage.tsx:609-628` calls the existing provider operation; provider remains `dataProvider.ts:866` | Runtime project metadata `default_timeline_id` / selection, not a canonical authored-timeline edit. |
| Project/timeline URL/default editor | Local/runtime URL branches and alias readers | `runtimeDocument.ts`, `RuntimeDocumentNormalizationGate.tsx`, `VideoEditorPage.tsx:455-468` use catalog reads, `history.replace`, and local resume state | Selection/read behavior only; no durable timeline writer. |
| Asset add/drop | Existing gallery navigation and editor placement path | `useDropToGeneration.ts`; `useGenerationsPaneController.ts:388-398`; `VideoEditorProvider.tsx:577-626` | Media/object import and native `commands.dryRun/apply` placement. 44f adds MIME metadata to registration; it does not add a writer. `D01-app-parent-media` remains OPEN. |
| Registry | Existing parent snapshot/registry boundaries | Bootstrap still sends `registry: { assets: {} }`; no changed path adds a second timeline registry publisher | No new registry writer. Existing parent/shot/asset D01 rows remain. |
| Chat | Existing project-chat registry persisted project metadata | New rename route and New→Main behavior flow through `ProjectChatRegistry.change` at `scripts/astrid-project-chat.ts:155-163` → `WorkspaceClient.updateProject` | Durable `metadata.astrid_agent_chat_v1`, not canonical timeline state. `localAgents.ts:86-87` is localStorage only. |
| Mobile | Existing editor interaction paths | `TimelineMobileInspectorDialog`, `mobile-interaction-model`, pane controls, and touch tests | Presentation/reachability only. No new `saveTimeline`, `commitData`, `publishParentComposition`, or registry writer caller. |

## Exact refreshed writer/caller census

The only changed-path canonical composition boundary is the existing bootstrap helper:

- `src/integrations/runtime/createDefaultTimeline.ts:60` calls `client.publishParentComposition` for an empty parent.
- `src/integrations/runtime/createDefaultTimeline.ts:84-100` exposes `createCanonicalTimeline`; `:104-165` repairs/chooses the first timeline and writes `default_timeline_id` through `client.updateProject` at `:148`.
- `src/shared/hooks/projects/useProjectCRUD.ts:154` calls `ensureProjectHasTimeline` after project creation.
- `src/tools/video-editor/pages/VideoEditorPage.tsx:477` calls first-timeline ensure; `:567` calls additional-timeline creation.

The canonical timeline metadata caller is separate:

- `src/tools/video-editor/pages/VideoEditorPage.tsx:716-721` validates membership, calls `AstridRuntimeClient.renameTimeline`, then refetches.
- `src/shared/components/ProjectTimelineSelectors.tsx:373-439` only gathers/validates the name and invokes the callback.

The project-selection metadata caller is also separate:

- `src/tools/video-editor/pages/VideoEditorPage.tsx:609-628` calls `providerSelection.dataProvider.setPrimaryTimeline`.
- The implementation at `src/integrations/runtime/dataProvider.ts:866` updates project metadata; it is not a changed path and is not an authored-timeline writer.

The asset path remains a native command producer but is not qualified for D01 retirement:

- `src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.ts:388-398` writes only add-generation URL intent.
- `src/tools/video-editor/contexts/VideoEditorProvider.tsx:577-626` reads the generation, plans the registry entry, dry-runs `place-prepared-media`, and calls the existing command facade. The 44f change is `metadata: { content_type: generation.type }` at `:585`.
- `src/features/gallery/hooks/useDropToGeneration.ts` imports/uploads media and invalidates generation queries; it does not publish canonical timeline state.

The chat path is durable but explicitly non-timeline:

- `src/tools/video-editor/components/AgentChat/AgentChatSessionSelector.tsx:395-489` submits a title.
- `src/tools/video-editor/hooks/useAgentSession.ts:1146-1155` exposes `useRenameProjectSession`.
- `src/integrations/astrid/acpRoutes.ts:131-134` sends the project-chat PATCH.
- `scripts/astrid-acp-bridge.ts:783-785` dispatches rename to the registry.
- `scripts/astrid-project-chat.ts:155-163` CAS-updates project metadata under `astrid_agent_chat_v1`.

## Upstream positives and IDs

Relevant main-added positive tests are present in these changed paths:

- `src/integrations/runtime/createDefaultTimeline.test.ts`: canonical-ID alias, exact-ID collision, concurrent-primary refetch, and unresolved-alias retry refusal tests.
- `src/shared/components/ProjectTimelineSelectors.test.tsx`: “renames the selected timeline without selecting it”.
- `src/tools/video-editor/pages/VideoEditorPage.test.tsx`: canonical-route rename, retry with the same additional-timeline idempotency identity, primary selection, and canonical default/first timeline selection.
- `src/tools/video-editor/lib/timeline-asset-plans.test.ts`: Runtime content-type registration (`video/mp4` versus image fallback).
- `src/tools/video-editor/lib/mobile-interaction-conformance.test.tsx`: touch hover-action and no-global-mode controls.
- `src/tools/video-editor/components/AgentChat/AgentChatSessionSelector.test.tsx`: title persistence and validation.
- `scripts/astrid-project-chat.test.ts`: idempotent creation, Main concurrency, and rename CAS/validation.

The source commits contributing these positives are upstream `44f0b9ca9d`, `8c28e1847` (one editor/URL shape and bootstrap identity hardening), `7593259f7` (default-editor rename), `8efc4cd6f` (mobile), `d16f9d55c` (chat rename/Main behavior), and `ae5977826` (Hermes/local-agent registry). No tests were run by this worker because the task explicitly requires a source-only census and forbids broad/browser/socket/build/typecheck/install runs.

## Smallest next native-ingress gaps

1. `D01-app-bootstrap`: qualify the existing constrained Runtime creation/repair plus guarded initialization, including accepted reload/retry/undo/no-output/default invariants.
2. `D01-app-parent-media`: qualify the existing generation-to-editor native capture through accepted Runtime publication, reload, undo, retry, and direct zero-legacy-traffic evidence.
3. Continue the already named `D01-app-whole-parent`, `D01-app-shot-graph`, `D01-app-popup-add`, `D01-app-popup-swap`, `D01-app-split`, `D01-app-duplicate`, `D01-app-placement`, `D01-app-ordinary-batch`, and `D01-app-element-routes` captures. Nothing in this upstream delta justifies closing or deleting any of them.

No new canonical writer outside App ownership was found, so no escalation or product-code edit is recommended from this audit. No rows, claims, or behaviors were marked deleted merely because they became UI-unreachable.
