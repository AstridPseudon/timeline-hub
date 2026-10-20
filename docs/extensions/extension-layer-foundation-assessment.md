# Extension Layer Foundation Assessment

> **Historical status.** This assessment predates the M2 retirement of the
> Supabase AI timeline endpoint and its numeric proposal/config writer. The
> edge proposal route described below is not supported or available now.
> Current timeline authoring uses App `EditCommand` capture and the Runtime
> `/v1` commit door; retained task completion handles outputs, billing, media,
> and relational metadata without publishing canonical timeline state.

This document assesses the last three milestones of the **`astrid-extension-layer-foundation`** epic chain defined in `.megaplan/briefs/astrid-extension-layer-foundation/chain.yaml`:

| Milestone | Idea brief | Merged PR |
|---|---|---|
| M3 | `.megaplan/briefs/astrid-extension-layer-foundation/m3-proposal-agent-policy-spine.md` | #56 |
| M4 | `.megaplan/briefs/astrid-extension-layer-foundation/m4-diagnostics-schemaform-lifecycle.md` | #57 |
| M5 | `.megaplan/briefs/astrid-extension-layer-foundation/m5-manager-phase4-readiness.md` | #58 |

M5 also produced the Phase 4 readiness artifact at `docs/extensions/phase4-readiness.md`. The follow-up target architecture is captured in `.megaplan/briefs/astrid-extension-layer-full-extensibility-ticket.md`.

## 1. Executive summary

M3, M4, and M5 do not yet constitute a proper, complete foundation for a user-facing extension development surface. They are a substantial internal foundation: proposal storage/runtime primitives exist, the edge agent can emit proposal-shaped envelopes, diagnostics are bounded and scoped, SchemaForm exists, lifecycle cleanup is largely real, and the Extension Manager exposes package states, toggles, diagnostics, and trust warnings. The foundation breaks at the user-facing integration layer: agent-returned proposals are never imported into the client ProposalRuntime, the manager settings editor does not use SchemaForm and can persist unvalidated string values, proposal policy persistence is only half-built, crashed contribution boundary reset is not centrally wired, and the readiness artifact itself says Phase 4 is prepared but not cleared for public family promotion. The verdict is: useful groundwork, not a shippable Phase 4 extension surface.

## 2. What the goal seemed to be

The chain brief makes M3-M5 the transition from hidden foundation work to a user-visible extension surface. M3 was supposed to make destructive extension and agent workflows proposal-first, durable, versioned, expirable, stale-safe, wired from the frontend through the Supabase edge function, and acceptable/rejectable through the client proposal apply path (`.megaplan/briefs/astrid-extension-layer-foundation/m3-proposal-agent-policy-spine.md:3`, `m3-proposal-agent-policy-spine.md:16`, `m3-proposal-agent-policy-spine.md:20`, `m3-proposal-agent-policy-spine.md:55`). M4 was supposed to add the host primitives needed before the manager: spoof-resistant extension diagnostics, bounded diagnostic storage, SchemaForm V1, and deterministic cleanup for disable/unload/re-enable including error-boundary reset (`m4-diagnostics-schemaform-lifecycle.md:3`, `m4-diagnostics-schemaform-lifecycle.md:11`, `m4-diagnostics-schemaform-lifecycle.md:14`, `m4-diagnostics-schemaform-lifecycle.md:17`, `m4-diagnostics-schemaform-lifecycle.md:56`). M5 was supposed to expose the foundation to users through a local manager: inspect already-loaded packages, persist enable/disable, edit settings through SchemaForm, see per-package diagnostics, see explicit trust warnings, and produce the Phase 4 readiness gate (`m5-manager-phase4-readiness.md:3`, `m5-manager-phase4-readiness.md:11`, `m5-manager-phase4-readiness.md:15`, `m5-manager-phase4-readiness.md:20`, `m5-manager-phase4-readiness.md:56`).

The intended bar was not "types and components exist somewhere." The briefs ask for connected behavior: frontend to edge to runtime to UI for proposals, SchemaForm-backed settings in the manager, lifecycle cleanup that users can rely on, and a readiness gate that either clears or blocks the next public contribution-family phase.

## 3. What has actually been accomplished

### M3 proposal and agent policy

The public data and persistence shape exists. `ExtensionProposalStatus` includes `pending`, `accepted`, `rejected`, `stale`, and `expired`, with proposal records carrying `baseVersion`, `expiresAt`, `acceptedAt`, and `rejectedAt` (`src/tools/video-editor/data/DataProvider.ts:100`, `src/tools/video-editor/data/DataProvider.ts:112`). Provider-facing proposal CRUD methods exist on the persistence service contract (`src/tools/video-editor/data/DataProvider.ts:296`), the since-retired Supabase provider created a cached extension persistence service, and the cache persists proposal records and status transitions (`src/tools/video-editor/runtime/extensionPersistenceCache.ts:940`, `src/tools/video-editor/runtime/extensionPersistenceCache.ts:988`, `src/tools/video-editor/runtime/extensionPersistenceCache.ts:1160`).

The runtime proposal state machine is meaningful. It records an unsupported-persistence diagnostic when no persistence provider is available (`src/tools/video-editor/lib/proposal-runtime.ts:281`), auto-expires TTL-elapsed proposals before reads and accept (`src/tools/video-editor/lib/proposal-runtime.ts:373`, `src/tools/video-editor/lib/proposal-runtime.ts:481`, `src/tools/video-editor/lib/proposal-runtime.ts:596`, `src/tools/video-editor/lib/proposal-runtime.ts:602`), rejects base-version mismatches before mutation (`src/tools/video-editor/lib/proposal-runtime.ts:499`), applies accepted proposals only through `timelineOps.apply` (`src/tools/video-editor/lib/proposal-runtime.ts:538`), and exposes `reject`, `expireStale`, `importProposal`, and `importEdgeProposals` (`src/tools/video-editor/lib/proposal-runtime.ts:549`, `src/tools/video-editor/lib/proposal-runtime.ts:567`, `src/tools/video-editor/lib/proposal-runtime.ts:678`, `src/tools/video-editor/lib/proposal-runtime.ts:769`).

The former edge agent had a proposal mode, but that endpoint and its
numeric config-writer implementation were retired in M2. The proposal-runtime
observations in this historical assessment do not authorize an edge route or
provide a current authoring contract.

### M4 diagnostics, SchemaForm, and lifecycle

The diagnostic collection is real and bounded. It has a default per-extension capacity of 100, oldest-first eviction, replacement by ID, removal by predicate, and removal by extension ID (`src/sdk/index.ts:130`, `src/sdk/index.ts:155`, `src/sdk/index.ts:171`, `src/sdk/index.ts:185`, `src/sdk/index.ts:219`). The public SDK diagnostics service documents that the host owns `extensionId` and `source` (`src/sdk/index.ts:3110`) and `createExtensionContext` pins both values when an extension reports diagnostics (`src/sdk/index.ts:3612`, `src/sdk/index.ts:3617`). Sync into the host collection also forces top-level `source: DIAGNOSTIC_SOURCE_EXTENSION` and preserves finer provenance under `detail` (`src/tools/video-editor/runtime/diagnosticCollectionSync.ts:41`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:57`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:68`). Cleanup by extension ID and localStorage settings-prefix cleanup exist (`src/tools/video-editor/runtime/diagnosticCollectionSync.ts:93`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:144`).

SchemaForm V1 exists and is more than a stub. The standalone settings panel imports `SchemaForm`, adapts manifest settings schemas, creates an extension settings service, validates through `validateAndFocus`, enumerates schema-defined keys including defaults, and renders SchemaForm (`src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:1`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:27`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:70`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:87`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:133`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:193`). `extensionSettings.ts` adapts manifest schemas into SchemaForm-compatible schemas and emits diagnostics for unsupported or malformed shapes (`src/tools/video-editor/runtime/extensionSettings.ts:4`, `src/tools/video-editor/runtime/extensionSettings.ts:119`).

Lifecycle cleanup is materially implemented. Disposal calls extension dispose handles and host-owned service cleanup (`src/tools/video-editor/runtime/extensionLifecycle.ts:177`, `src/tools/video-editor/runtime/extensionLifecycle.ts:217`). The lifecycle host disposes changed or removed extensions, disposes live sources, notifies lifecycle-disposed listeners, and activates new lifecycles (`src/tools/video-editor/runtime/extensionLifecycle.ts:536`, `src/tools/video-editor/runtime/extensionLifecycle.ts:560`, `src/tools/video-editor/runtime/extensionLifecycle.ts:587`, `src/tools/video-editor/runtime/extensionLifecycle.ts:605`). `EditorRuntimeProvider` wires disposal listeners that unregister commands, effects, transitions, shaders, clip types, agent tools, diagnostics, and settings UI state (`src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:516`, `src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:524`, `src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:582`, `src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:619`, `src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:674`). Provider unmount disposes all lifecycles and live runtime services (`src/tools/video-editor/contexts/EditorRuntimeProvider.tsx:793`).

### M5 manager and readiness gate

The manager exposes explicit package states and does not collapse everything into a boolean. `PackageStateInventoryEntry` includes `extensionId`, `packageState`, `stateReason`, and metadata (`src/tools/video-editor/runtime/extensionSurface.ts:450`, `src/tools/video-editor/runtime/extensionSurface.ts:473`). `ExtensionManager` renders all seven current states with distinct labels (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:54`), subscribes to a live diagnostic collection (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1369`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1373`), shows per-package diagnostic badges and expandable diagnostic detail (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1119`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1213`), and persists enable/disable via `putEnablementState` followed by runtime refresh (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1050`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1067`). The manager is placed in the Properties panel's Extensions tab behind an error boundary (`src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx:413`).

Trust posture is explicit in UI and docs. The manager banner states that extensions run as trusted, unsandboxed code and manifest permissions are declarative only (`src/tools/video-editor/components/ExtensionManager/ExtensionTrustWarningBanner.tsx:3`, `src/tools/video-editor/components/ExtensionManager/ExtensionTrustWarningBanner.tsx:16`). The readiness artifact repeats the same trust posture and blocks arbitrary public code families until trusted/signed local packages or a real sandbox/permission broker exists (`docs/extensions/phase4-readiness.md:77`, `docs/extensions/phase4-readiness.md:81`, `docs/extensions/phase4-readiness.md:87`).

The readiness artifact is valuable. It identifies the stale `contributionFamilies.ts` roadmap reference, names current code anchors, defines render planner participation gates, lists trust/sandbox constraints, and gives a per-family promotion checklist (`docs/extensions/phase4-readiness.md:11`, `docs/extensions/phase4-readiness.md:13`, `docs/extensions/phase4-readiness.md:38`, `docs/extensions/phase4-readiness.md:96`, `docs/extensions/phase4-readiness.md:130`).

## 4. Where the implementation lives up to the goal

The proposal runtime itself is one of the stronger parts. Its state transitions respect the important safety rule: expired and stale proposals do not silently apply, and accepted proposals go through one apply path (`src/tools/video-editor/lib/proposal-runtime.ts:481`, `src/tools/video-editor/lib/proposal-runtime.ts:506`, `src/tools/video-editor/lib/proposal-runtime.ts:538`). The runtime also has persistence hooks and reload hydration when a persistence provider is supplied (`src/tools/video-editor/lib/proposal-runtime.ts:293`, `src/tools/video-editor/lib/proposal-runtime.ts:313`, `src/tools/video-editor/lib/proposal-runtime.ts:619`).

The former edge proposal mode is historical only. New proposals or edits must
be represented by the published `EditCommand` contract and submitted through
the Runtime commit path; this document does not define an alternate edge
writer.

Diagnostics are a credible primitive. The collection enforces deterministic per-extension bounds and removal, and sync into the UI collection pins extension-authored diagnostics to the extension source (`src/sdk/index.ts:155`, `src/sdk/index.ts:199`, `src/sdk/index.ts:219`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:57`). That is a good foundation for future manager and diagnostics surfaces.

SchemaForm is a credible primitive outside the manager. The standalone `ExtensionSettingsPanel` correctly uses schema-derived keys, defaults, validation, and a host settings service (`src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:87`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:133`, `src/tools/video-editor/components/ExtensionSettings/ExtensionSettingsPanel.tsx:193`). Tests are broad around SchemaForm, proposal runtime, lifecycle, and ExtensionManager component behavior.

The manager's package-state and diagnostic UX is largely sound for a local host-supplied package list. It has visible disabled/invalid/incompatible/duplicate/settings/runtime states, live diagnostic counts, expandable diagnostic detail, persistent trust warning, and no install/update/marketplace affordances (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:54`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1119`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1450`).

The readiness artifact is honest rather than promotional. It says Phase 4 should not begin as broad parallel family work and that public promotion remains blocked until stale roadmap references or planner integration are addressed (`docs/extensions/phase4-readiness.md:153`, `docs/extensions/phase4-readiness.md:155`, `docs/extensions/phase4-readiness.md:163`).

## 5. Where it falls short

### 5.1 Retired edge proposal surface

The former edge proposal lifecycle is retired with its endpoint and numeric
writer. The current safety boundary is simpler: App authoring captures a
published `EditCommand`, stores it in the outbox until acknowledged, and sends
it to Runtime for validation, rebase, acceptance, history, and undo. No edge
proposal response is a supported input to the timeline.

### 5.2 Retired edge session policy

The former edge session policy and its proposal response are not part of the
current execution contract. Do not restore them as a second timeline writer;
use the Runtime command contract for authoring decisions.

### 5.3 Current authoring boundary

The authoritative edit result is the Runtime accepted revision and receipt.
Completion-side generation, billing, media, and relational metadata remain
separate from canonical timeline publication.

### 5.4 Extension Manager settings are not SchemaForm-backed

M4 delivered a SchemaForm-backed `ExtensionSettingsPanel`, but M5's actual manager does not use it. `ExtensionManager.tsx` imports `adaptManifestSettingsSchema`, not `SchemaForm` or `ExtensionSettingsPanel` (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:47`). `PackageSettingsSection` uses schema adaptation only to decide whether to route to raw JSON for unsupported schemas (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:424`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:430`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:447`). For supported schemas it loads only existing saved values (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:484`) and renders an inline key-value editor with `<input type="text">` for every field (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:815`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:828`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:831`).

The normal manager save path persists `editValues` directly through `repository.putSettingsSnapshot` with no SchemaForm validation and no manifest-schema validation (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:518`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:524`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:533`). Raw JSON mode validates against the manifest schema (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:591`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:614`), but the default supported-schema path does not. New packages with a valid schema but no saved settings show "No saved settings" instead of rendering schema defaults or required fields (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:756`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:771`).

This directly misses M5's done criterion: "Settings edit/save/reload works through SchemaForm and provider persistence" (`m5-manager-phase4-readiness.md:61`).

### 5.5 Diagnostics source pinning has two implementations with slightly different contracts

The SDK `ExtensionDiagnosticsService` interface says callers cannot provide `extensionId` or `source`, and `createExtensionContext` pins both (`src/sdk/index.ts:3113`, `src/sdk/index.ts:3613`, `src/sdk/index.ts:3617`). The lifecycle-local `createExtensionDiagnosticsService`, however, accepts `Omit<ExtensionDiagnostic, 'extensionId'>` and pins only `extensionId`, not `source` (`src/tools/video-editor/runtime/extensionLifecycle.ts:124`, `src/tools/video-editor/runtime/extensionLifecycle.ts:130`, `src/tools/video-editor/runtime/extensionLifecycle.ts:131`). The collection sync layer later overwrites the top-level collection diagnostic source (`src/tools/video-editor/runtime/diagnosticCollectionSync.ts:57`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:62`), so this is not an immediate display spoofing bug. It is still contract drift in a security-sensitive primitive: the lifecycle diagnostics service type and implementation do not match the public SDK's "host overwrites source" promise.

### 5.6 Re-enable after crash does not centrally reset contribution boundaries

`ContributionErrorBoundary` supports `recoveryKey` and only resets a crashed boundary on recovery-key change when one is supplied (`src/tools/video-editor/runtime/ContributionErrorBoundary.tsx:181`, `src/tools/video-editor/runtime/ContributionErrorBoundary.tsx:187`, `src/tools/video-editor/runtime/ContributionErrorBoundary.tsx:193`). Search shows call sites wrap several contribution surfaces, but host components do not pass a lifecycle-owned recovery key into those boundaries. `EditorRuntimeProvider` also does not centrally own error-boundary reset state. M4 required "Re-enabling a crashed extension resets the render boundary and attempts fresh render" (`m4-diagnostics-schemaform-lifecycle.md:66`). The boundary primitive exists, but the lifecycle-to-render-boundary reset contract is not centrally wired.

### 5.7 Package manager inventory excludes direct-extension-only providers

`useExtensionLoaderWiring` returns direct extensions immediately when no repository is present, but returns `packageStateEntries: []` (`src/tools/video-editor/runtime/useExtensionLoaderWiring.ts:336`, `src/tools/video-editor/runtime/useExtensionLoaderWiring.ts:338`, `src/tools/video-editor/runtime/useExtensionLoaderWiring.ts:344`). `extensionSurface.ts` documents this backward-compatible empty inventory for direct-extension-only providers (`src/tools/video-editor/runtime/extensionSurface.ts:450`, `src/tools/video-editor/runtime/extensionSurface.ts:455`). That may be acceptable for repository-backed installed packages, but M5's manager says it manages packages already loaded/supplied by the host (`m5-manager-phase4-readiness.md:11`, `m5-manager-phase4-readiness.md:36`). In direct-only host setups, active extensions can exist while the manager shows no packages in inventory (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:1431`). That is a product-surface gap.

### 5.8 Non-active package contribution summaries are absent

`deriveContributionSummary` only looks in `extensionRuntime.extensions`, which contains active extensions; if the extension is disabled, invalid, incompatible, duplicate, settings-error, or runtime-error, it returns `null` (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:150`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:155`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:158`). This makes non-active packages inspectable but less informative. It is not a blocker, but it weakens the stated "disabled packages remain inspectable" goal.

### 5.9 Phase 4 readiness gate is not an acceptance

The readiness artifact correctly identifies stale roadmap references and future gates, but it explicitly does not update the roadmap/tickets (`docs/extensions/phase4-readiness.md:130`, `docs/extensions/phase4-readiness.md:132`) and ends by saying Phase 4 is "prepared but not cleared for public family promotion" (`docs/extensions/phase4-readiness.md:163`). This is the right call, but it means M5 produced a blocker list rather than a clearance.

### 5.10 Test coverage is broad but misses the most important integration paths

There are strong unit/component tests for ProposalRuntime, ProposalPanel, SchemaForm, diagnostics, lifecycle, and ExtensionManager behavior. The missing tests align with the highest-risk gaps:

- No full `useSendMessage` -> edge proposal response -> `importEdgeProposals` -> `ProposalRuntime` -> `ProposalPanel` -> accept/reject integration test. `importEdgeProposals` has no production caller (`src/tools/video-editor/lib/proposal-runtime.ts:769`).
- No E2E extension-manager coverage; the only e2e file in the repository is `tests/e2e/home-load.spec.ts`.
- No manager test can prove SchemaForm-backed settings because the manager does not import SchemaForm.
- No test proves lifecycle-owned recovery-key reset on extension re-enable because that wiring does not exist.
- No test of durable session-level `proposal_policy` read/write because the edge session code does not use the migrated column.

## 6. Risk ranking

### Blocker

1. **Agent proposal lifecycle is not end-to-end user-facing.** Edge proposals are returned and normalized, but never imported into `ProposalRuntime`, so the user cannot reliably see, persist, accept, or reject agent-generated proposals (`src/tools/video-editor/hooks/useAgentSession.ts:101`, `src/tools/video-editor/hooks/useAgentSession.ts:381`, `src/tools/video-editor/lib/proposal-runtime.ts:769`). This fails M3's core done criteria.

2. **Extension Manager settings are not SchemaForm-backed and can persist invalid values.** The manager's default settings path uses text inputs and direct snapshot writes instead of SchemaForm validation or manifest-schema validation (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:815`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:828`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:518`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:533`). This fails M5's user-facing settings criterion.

### High

3. **Historical edge proposal policy is retired.** It is not a supported authoring or persistence path; Runtime command acceptance is authoritative.

4. **Crash recovery boundary reset is not centrally lifecycle-wired.** The boundary supports `recoveryKey`, but lifecycle re-enable does not drive it (`src/tools/video-editor/runtime/ContributionErrorBoundary.tsx:187`, `src/tools/video-editor/runtime/ContributionErrorBoundary.tsx:193`). This fails part of M4's lifecycle cleanup contract.

5. **No integration test covers the user-critical proposal path.** Existing tests can pass while the agent proposal bridge remains broken.

### Medium

6. **Runtime command acceptance is the current mutation signal.** Historical edge proposal response fields must not be used as a substitute.

7. **Diagnostics service contract drift.** One service pins source and extension ID, another only pins extension ID, relying on downstream sync to normalize source (`src/sdk/index.ts:3613`, `src/tools/video-editor/runtime/extensionLifecycle.ts:130`, `src/tools/video-editor/runtime/diagnosticCollectionSync.ts:62`).

8. **Direct-extension-only hosts can have active extensions but no manager inventory.** This is documented backward compatibility, but weakens the manager-as-user-surface story (`src/tools/video-editor/runtime/useExtensionLoaderWiring.ts:336`, `src/tools/video-editor/runtime/useExtensionLoaderWiring.ts:344`).

9. **Non-active packages lack contribution summaries.** Disabled/invalid packages remain visible, but are less inspectable than intended (`src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:150`, `src/tools/video-editor/components/ExtensionManager/ExtensionManager.tsx:158`).

### Low

10. **Proposal persistence failures are swallowed without surfacing a live diagnostic.** Runtime persistence errors are non-fatal (`src/tools/video-editor/lib/proposal-runtime.ts:293`, `src/tools/video-editor/lib/proposal-runtime.ts:307`, `src/tools/video-editor/lib/proposal-runtime.ts:313`, `src/tools/video-editor/lib/proposal-runtime.ts:321`). That is acceptable for editing continuity but not ideal for a user-facing proposal surface.

11. **Readiness reconciliation is informational only.** The artifact names stale references and promotion gates but intentionally does not update source roadmap/ticket docs (`docs/extensions/phase4-readiness.md:130`).

## 7. Recommended next steps

1. **Wire agent proposal import into the frontend.** In `useAgentSession` success handling, get the provider-scoped `proposalRuntime`, call `importEdgeProposals(data, proposalRuntime)` for returned proposals, surface import diagnostics, and ensure imported proposals appear in `ProposalPanel`. Add a test that starts with a mocked edge response containing proposals and ends with a rendered pending proposal that can be accepted/rejected through the same runtime apply semantics.

2. **Make proposal policy durable or remove the dead column.** Either persist `proposal_policy` to `timeline_agent_sessions` and read it as the session default, or delete the unused session column and document that policy is per-invocation only. The safer foundation is durable session policy with request-body override rules.

3. **Replace `PackageSettingsSection` with the SchemaForm-backed settings path.** Reuse `ExtensionSettingsPanel` or a shared host-owned SchemaForm adapter inside ExtensionManager. It must render schema defaults for packages with no saved settings, use typed controls for primitive fields, block invalid saves, and write through provider persistence.

4. **Drive contribution error-boundary reset from lifecycle state.** Add a provider-owned per-extension recovery counter/key that increments on re-enable or retry-after-failure, and pass it to every `ContributionErrorBoundary` wrapping extension-rendered surfaces. Add a provider-level test for disable/re-enable after a throwing contribution.

5. **Tighten diagnostics service contracts.** Align `createExtensionDiagnosticsService` with the SDK interface by omitting both `extensionId` and `source` from caller input and pinning both at report time. Keep collection sync's top-level source override as defense in depth.

6. **Clarify manager inventory semantics.** Either include direct extensions in package-state inventory with a `loaded` state, or explicitly scope the manager to repository-backed package inventories and make the empty state say direct-only host packages are not managed here.

7. **Refine `mutation_applied`.** Track actual timeline config writes separately from proposal count. Read-only proposal-mode commands and blocked tools should report `mutation_applied: false`.

8. **Promote the readiness artifact into an actionable gate.** Update the stale roadmap/ticket references or restore a generated contribution-family matrix, mark whether Phase 4 is blocked or accepted, and make the artifact a checklist with owners/status instead of only a narrative reconciliation.

9. **Add acceptance-level tests before declaring Phase 4.** Minimum coverage should include frontend-agent proposal import/accept/reject, manager SchemaForm save/reload/default rendering, lifecycle crash/re-enable boundary reset, direct-extension inventory behavior, and a browser acceptance test for the Extensions tab.

Until those actions are complete, M3-M5 should be described as a partial internal foundation with several correct primitives, not as a proper complete foundation for a user-facing extension development surface.
