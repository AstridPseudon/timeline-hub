**Named cause: the catalog panel executes an uncaptured owner adapter.** The actual D45 element failure is a pre-save head-guard rejection.

Source custody: App `c0fe88994405fd517b58473c14678a0d1b73056d`, tree `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`. No worktree changes.

- [ElementsLibraryPanel.tsx:46](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/components/ElementsLibraryPanel.tsx:46) obtains the shared adapter and calls `execute()` directly.
- [VideoEditorProvider.tsx:322](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/contexts/VideoEditorProvider.tsx:322) creates that owner with `getHead`, without `capturedHead`.
- [element-adapter.ts:400](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/runtime/element-adapter.ts:400) copies the current head into a captured adapter only through `captureForTurn()`. The first owner execution therefore has neither an acknowledged nor captured head.
- [element-adapter.ts:461](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/runtime/element-adapter.ts:461) reads the mounted document and rejects its present head against that missing capture. The Agent caller already captures correctly at [useAgentSession.ts:108](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/hooks/useAgentSession.ts:108).

Actual retained evidence:

- Run `app-readiness-D45-final-caller-sol-0446-full-e2e-three-products-1024045333-13583`: terminal exit **1**, **405s**, **3 failed / 5 NOTRUN**. Element case: **15.8s**.
- Inspected the element ZIP after repeated unchanged size/mtime, no open descriptors, and successful ZIP CRC verification.
- Original test at [three-products.p2-elements-assets.spec.ts:376](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/tests/e2e/local/three-products.p2-elements-assets.spec.ts:376) reached Apply, then failed the dialog’s `applied` assertion. Actual message: **“The captured timeline head changed or is missing. Inspect the current timeline before recovering this operation.”**
- Trace monotonic timings: Apply `32222.332–32312.716ms`; refusal visible by `32310.530ms`; assertion failed at `37336.179ms`.
- The commit-response wait began at `31746.268ms` and ended at `37796.732ms` because teardown closed the context. Recorded browser traffic contains **zero commit POSTs**, corroborating the source rejection before save. This conclusion does not derive from a timeout alone.
- Safe error identity: `AstridElementOperationError` at `element-adapter.ts:467`; no Runtime error code/path or commit reply exists for this gesture.

The reached chain is catalog Apply → admission refresh/authority checks → mounted document read → missing captured-head refusal. Local source guards, [mounted save handoff](/home/user/work/wt/app-P2-D45-element-cause-sol-0459/src/tools/video-editor/hooks/useTimelineSave.ts:708), outbox append/dispatch, `commitTimeline`, reply adoption, params edit, reload and Undo were **not reached**. Their correctness remains unverified by this case.

The exact prior `804134d…` run reported the same refusal, with trigger UNKNOWN. D45 independently establishes the missing-capture trigger; the panel’s caller is unchanged from that revision. No Runtime-cost or downstream source-mapping cause is established.

Recommended bounded next worker:

- Own `ElementsLibraryPanel.tsx`, its tests, and the relevant mounted staging test.
- Capture the adapter synchronously at the catalog gesture boundary, before execution’s first await.
- Preserve authority, generation, head and source guards.
- Cover first catalog Apply with a present head and refusal after an intervening head/editor change. Existing staging coverage calls `captureForTurn()` itself, bypassing this faulty caller.
- Retain the original line-376 journey and all eight/Gate5 assertions unchanged.

Other actual failures need separate ownership: popup ADD now reaches a command-shape assertion; parent move ends at a 90s response wait. Their product causes remain UNKNOWN here. D45 readiness PASS is stage evidence only.

No tests, services or browsers were launched. Checks: `git diff --check` PASS; `git status --porcelain=v1` empty; `git rev-parse HEAD HEAD^{tree}` matches the assigned base. Commit message and `DONE` created.