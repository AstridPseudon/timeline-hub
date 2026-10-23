# A2 P2 readiness source review

## Verdict: PASS

The source-only diagnosis `app-A2-P2-ready-cause-sol-1947` is supported by App `2107e1870e51c650d59315f4cc1ab6af338f198c` / tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`. It correctly concludes:

- the `runtime-connection-status` selector is valid on the hosted `/tools/video-editor` route;
- same-origin mode conditionally bypasses the Pill because `RuntimeConnectionProvider` defaults `gated` from `runtimeOrigin() !== ''` (`src/integrations/runtime/RuntimeConnectionProvider.tsx:178-185`, `:435-456`);
- the Pill emits `data-testid="runtime-connection-status" data-state="connected"` only after connection and an `ok` restart watch (`src/shared/components/RuntimeConnection/RuntimeConnectionPill.tsx:42-58`);
- the Farm `31814` result remains **0 PASS / 3 FAIL / 5 NOTRUN**, with no gesture, delta, reload, undo or zero-old-route credit;
- actual `31814` cause remains **UNKNOWN**, and missing safe fields are not relabeled LOST without explicit custody evidence.

The route binding is production-reachable: `/tools/video-editor` selects `VideoEditorPage` (`src/app/routes.tsx:101-107`), while `App` and `AppProviders` mount `RuntimeDocumentBoundary` (`src/app/App.tsx:79-85`, `src/app/providers/AppProviders.tsx:112-127`). The boundary supplies the production Pill and panel (`src/app/runtime/RuntimeDocumentBoundary.tsx:19-26`). This is not a file-presence-only claim.

The diagnosis also preserves the health/realm versus authenticated-handshake distinction. The gate probe reads health, schema digest and realm (`src/integrations/runtime/RuntimeConnectionProvider.tsx:80-116`); it does not perform the authenticated handshake. `AstridRuntimeClient.openSession` separately performs health plus handshake, capability/scope and identity checks, then realm matching (`src/integrations/runtime/client.ts:469-533`). No auth, realm, Agent or Runtime fault is inferred from missing DOM alone.

The build distinction is correctly conditional: ordinary `build` and `build:hosted` are separate scripts (`package.json:15-16`); hosted build sets the Runtime origin and clears compiled identity (`scripts/build-hosted.mjs:4-7`), and boot applies the origin before app imports (`src/app/main.tsx:12-15`). This is not evidence that the Farm used either mode, nor an actual-cause claim. D28’s environment-first comparison remains Proof-owned.

The A2 contract boundary remains preserved without source changes. Generated request/reply DTOs retain the full request and `{data, receipt}` accepted/preview/failure shape (`src/integrations/runtime/timeline-commit-types.ts:67-76`, `:94-103`, `:112`); the local document save session/outbox and Runtime `commitTimeline` handoff remain in `src/tools/video-editor/hooks/useTimelineSave.ts:80-90`, `:180-193`, `src/tools/video-editor/commands/localSaveSession.ts:65-313`, and `src/integrations/runtime/dataProvider.ts:745-766`. No alternate publication or safety/classifier refusal path was introduced.

## Source and custody audit

The review worktree is `93cddc687d74f0aac844e04965b1762acaf5153b` / tree `2748a331f70fb5b4c70f6e896282b011cf577893`. Relative to the diagnosis pin `2107` / `a3ff358`, the only difference is the separately owned four-line popup fixture change in `tests/e2e/local/three-products.p2-popup.spec.ts`; all reviewed readiness source blobs match. `git diff --exit-code 2107e1870e51c650d59315f4cc1ab6af338f198c -- src ':!tests/e2e/local/three-products.p2-popup.spec.ts'` and `git diff --check` pass; worktree status is clean.

Protected custody remains unchanged: P1 first chunk `11,614` bytes SHA-256 `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; P1 second chunk `7,612` bytes SHA-256 `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`; original Gate5 source blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.

Tests/typecheck/lint are **N/A** under the read-only unchanged-source instruction; no fresh PASS is claimed. No browser/HTTP/body/preflight/seed/full/control-loop/dispatcher call was made. P3 readiness remains distinct from P2, and the popup `17324` correction remains Proof-owned and separate from this verdict. Next action is the already-authorized Proof-owned environment comparison or retained safe trace review; no App repair is justified until equivalent environment and earliest actual stage are evidenced.
