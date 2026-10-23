# A2 P2 initial connection readiness: source verdict and retained-evidence gap

## Verdict

**Selector valid on the selected hosted workspace route; actual 31814 failing stage UNKNOWN.** The selector was not removed or renamed. P2 navigates to `/tools/video-editor`, whose production boundary supplies the real `RuntimeConnectionPill`. On a gated/hosted build, `isConnected` plus restart status `ok` renders `data-testid="runtime-connection-status" data-state="connected"` as an `sr-only` element. P2 uses `toHaveAttribute`, so the element need not be visibly painted. The production guard must remain.

**The same route does not guarantee a Pill in every build mode.** `RuntimeConnectionGate` returns children without invoking the Pill when `gated=false`. The default is determined by whether the boot-configured Runtime origin is nonempty. Thus absent DOM does not by itself prove `connection.isConnected=false`, an authentication failure, or any Agent/Runtime defect. Actual served build mode and browser observations are missing. This is a conditional source distinction, not an attribution of the actual run.

No product repair or test change is justified by the available actual evidence. Preserve all guards, selectors and timeouts. No shared cause with P3's settled local owner or P1's second trim is established.

## Selected source and actual result

- App HEAD `2107e1870e51c650d59315f4cc1ab6af338f198c`, tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`; source audit matches HEAD and worktree.
- Farm's published tuple: Agent `079580ca46af77e0292d49dc34386b25c8391f99`, Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. These are reported pins, not independently observed browser/module identities.
- Actual body `app-ap2-P2-exact8-1023192238-31814`: FINAL exit 1, 204 s, 0 PASS / 3 FAIL / 5 NOTRUN. Preflight `app-ap2-P2-exact8-preflight-1023192026-14651`: GREEN, exit 0. These are prior Farm results; no fresh PASS is claimed.
- Element case `three-products.p2-elements-assets.spec.ts:376` and parent move `three-products.p2-tour.spec.ts:564` stop at the initial connection attribute expectation, before their gestures and before installing their gesture wire recorder. This supplies no gesture, delta, reload, undo or zero-legacy-traffic credit.
- Popup ADD `three-products.p2-popup.spec.ts:807` stops separately at fixture setup: 422 `capture_mismatch`, created identity declaration. Proof's popup-seed worker 1934 is sole author. No duplicate diagnosis/fix was made here.
- Five NOTRUN remain NOTRUN. Serial configuration exists in elements-assets `:43`, popup `:82`, tour `:37`, consistent with stopping each file's successors after its first failure; the actual runner disposition is not captured in the published summary, so this is source inference only.

The Farm summary calls both helpers `openCommandTimeline` at line 144. On the selected source, elements-assets instead calls `openTimeline` at `:377`, with the connection expectation at `:166`; tour calls `openCommandTimeline` at `:565`, with expectation at `:144`. Both use the same selector and route, but the actual retained stack/member is needed to settle this summary provenance discrepancy. It is not evidence of another source tree by itself.

## Production path, in execution order

| Stage | Selected source and behavior | What the initial selector can establish |
|---|---|---|
| Harness and fixture | `support/app.ts:56–76` creates a worker harness/browser and a new context. `support/harness.ts:491–512` requests local-network permission, applies host/certificate mapping and public-address-space treatment. Each P2 worker seeds native-none (`elements-assets:37–40`, `tour:31–34`). Both open helpers await `enableTimelineAuthoring` then `page.goto` before checking connection. `harness.ts:589–615` starts the authoring Runtime if not already active and waits for its health. | Node-side seed/health and requested browser permission are not proof of a successful browser connection. |
| Served page | `harness.ts:228–247` serves `DIST_DIR` with SPA fallback; `/api/*` and `/runtime-config/*` on the hosted origin explicitly return 404. | The actual built assets and resolved gateway-vs-same-origin mode matter. |
| Browser entry | `app/main.tsx:12–47` configures Runtime origin before imports and classifies the URL; `entryClassification.ts:4–12` makes this path app-owned. `main.tsx:80–103` completes migration, identity initialization and render. | Boot/migration/import errors can prevent the whole component path; current evidence does not exclude them. |
| Router and providers | `app/App.tsx:79–85` places `AppProviders` inside `BrowserRouter`. `AppProviders.tsx:112–128` composes `AuthProvider`, `AuthGate`, then `RuntimeDocumentBoundary`. `routes.tsx:101–107` binds this path to the production `VideoEditorPage` under Layout. `runtimeDocument.ts:3–9` classifies it as a workspace. | This is an actual route binding, not merely an unused Pill file. |
| Auth and boot connection | `AuthContext.tsx:27–30` owns `RuntimeConnectionProvider`. Hosted `AuthSession` derives auth/loading from its connection (`:84–95`), rather than running a separate bridge session. `AuthGate.tsx:18–23` passes a loading hosted workspace to its connection boundary. Same-origin auth uses its bridge probe and may show recovery (`AuthContext.tsx:48–80`, `AuthGate.tsx:27–39`). | No hosted auth principal is independently inferred from a missing status element. |
| Runtime boundary | `RuntimeDocumentBoundary.tsx:12–26` supplies Panel and Pill to the connection gate, wrapping document normalization as its child. Non-workspace bypass does not apply to the expected P2 pathname. | A retained route change would still need evidence. |
| Mode and connection gate | `connection.ts:75–100` sets origin once at boot. Provider `:180` defaults `gated` from origin. Gate `:435` bypasses Pill for same-origin; hosted `:437–456` renders Pill and children only once `isConnected`. A panel may remain over the mounted app, making it inert. | Pill absence can be build-mode bypass, not-connected, or a missing/unmounted/failed ancestor. Attribute success does not prove the overlay left or owner settled. |
| Pill/restart watch | `RuntimeConnectionPill.tsx:32–58`: null if disconnected; connected attribute when watch is `ok`. `:62–78` uses the same test id with `stopped`/`restarted` otherwise. Restart watch begins `ok`, tracks subsequent health failures/instance changes (`useRuntimeRestartWatch.ts:91–153`); realm-change maps to the restarted card. | Distinguish absent element from a present `stopped`/`restarted` element; the published shorthand cannot do so precisely. |
| Document/editor/local owner | Normalization is a sibling after the Pill within the gate (`RuntimeConnectionProvider.tsx:449–453`), then project/timeline reads and mounted local-save setup run. `RuntimeDocumentNormalizationGate.tsx:27–90` can hold/fail its own descendants. | Normalization, basis-read, recoverable identity or outbox/session failure alone does not suppress the earlier Pill in an otherwise mounted connected gate. |

### Initial connection probe versus authenticated client handshake

`RuntimeConnectionProvider.tsx:88–124` probes browser-door `/api/runtime/v1/health`, accepts the schema digest, then reads `/api/runtime/v1/realm` and requires the identity fields to be strings. It does **not** call `/handshake`. A health status string is required here; full client session health validation is a later, stricter boundary. Its health/realm fetches use the door; no browser credential body is exposed by this report.

Permission discovery precedes these reads (`:215–235`). Granted/unsupported permission permits probing; prompt requires Connect/auto-connect; denied blocks (`:280–298`, `:310–350`, `localNetworkPermission.ts:44–49`). Probe outcomes distinguish 502/503 door codes `runtime_unavailable` and `runtime_identity_mismatch`, incompatible schema, silent transport/non-200/malformed replies, and connected. The connected state is latched (`:237–272`); later recovery is the Pill watch, not a reset of that latch. None of these actual outcomes is recorded in the published P2 summary.

The separate `AstridRuntimeClient.openSession` (`client.ts:469–540`) runs health plus handshake, validates health/schema/capability/product-role scopes and selected/observed identity, then realm equality. It maps rejected authentication to `RuntimeAuthenticationError`, compatibility refusals to `RuntimeCompatibilityError`, and other failures to `RuntimeUnavailableError`. Recoverable identity (`:460–466`) follows that authenticated session. These production checks remain necessary, but their failure is not demonstrated by an initial missing Pill. Do not substitute P3 owner-readiness evidence for these first-connection observations.

### Concrete build-mode hypothesis, not actual cause

The published 17:56 P3/P2 packet body at line 77 invokes `npm run build` and contains no `VITE_RUNTIME_ORIGIN` assignment. `package.json:15–16` distinguishes ordinary `vite build` from `build:hosted`; `scripts/build-hosted.mjs:4–7` explicitly sets the gateway origin and clears compiled identity. Farm's published report lists a plain build with diagnostic/heap changes, but its final row and served bundle are not available here. Vite build inputs could still provide an origin: absence of an inline assignment is not proof of the compiled value.

If the actual served bundle resolves an empty origin, same-origin gate bypass omits this valid hosted selector even though its provider reports connected. The hosted harness supplies no same-origin API proxy (`harness.ts:233–234`), so its auth/read paths would also differ. If the bundle is correctly hosted, a retained connection-panel state and browser health/realm outcome are needed before assigning any production boundary fault. Neither branch has been proven for 31814. Do not change build configuration or weaken the selector on this hypothesis.

## Existing evidence availability and precise missing safe fields

Read inputs: PLAN A2/P2, `peer-app2-to-app-20261023T1936-P2-P3-readiness-popup-owner.md`, `peer-app2-to-farm-20261023T1936-P2-terminal-ACK-finite-evidence.md`, `farm-p2-run.md`, Farm 19:32/19:38 notes, App 19:47 ownership note, P3 source report 1934 and independent review 1939. The later P3 LOST acknowledgement applies only to P3 15659; it cannot establish P2 trace retention.

At this audit's publication scan, no flat safe 31814 trace projection was published in the shared design directory. `Path.exists()` returned false for the Farm-cited local paths `$ORCH/tests/app-ap2-P2-exact8-1023192238-31814/log.txt`, `/home/user/work/wt/.test-app-ap2-P2-exact8-1023192238-31814/test-results/three-products`, and `$ORCH/workers/tf-p2-run/p2-row-after-node.cmd`. This is local unavailability, **not** an owner statement that P2 traces were LOST. No raw trace/archive was copied or printed; no alternative service/path was used to bypass permissions. The shared suite file has no exact `app ap2-P2-exact8 ` row available for this audit.

For **each** of the element:376 and parentmove:564 cases, the following fields are UNKNOWN and must come only from already-retained safe evidence if available:

| Missing safe observation | Distinction it resolves |
|---|---|
| Run/case/test-source identity, artifact/member provenance, event time relative to navigation and assertion; actual source parent/tree and served entry/asset hash | Correct case/source, including the elements helper-line discrepancy; summary versus actual execution. |
| Route pathname and query-key presence only; root/app/migration-error/boot-hold presence; sanitized pageerror class/code/stage | Expected workspace mounted versus redirected/public/failed boot. No URL identity values. |
| Resolved mode: gateway origin configured boolean, provider `gated` boolean, compiled identity presence booleans, actual bundle binding | Hosted selector applicability versus same-origin bypass. No environment dump or identity values. |
| Status element count plus `data-state` if present; panel presence plus `data-state`/`data-leaving`; provider `isConnected`, `isBooting`, `awaitingConnect` if captured | Missing Pill versus stopped/restarted status versus boot/permission panel; overlay may remain after connection. |
| Browser local-network permission state and Connect/auto-connect stage if captured | Requested permission in source versus actual granted/prompt/denied state. |
| Browser request stage, method, redacted route template, HTTP status/transport-error class for door health then realm; sanitized refusal code; schema-accepted boolean; identity-fields-present booleans | Transport/permission/CORS, door refusal, digest rejection, malformed identity, or actual connection success. No headers/raw replies. |
| Restart-watch stage/outcome and identity-presence/change boolean if the status exists with a non-connected value | Later stopped/restarted card versus never-connected gate. No instance/realm values. |
| Only if already captured after connection: handshake stage/status and safe connector error class/code, capability/scopes-valid booleans, identity present/matches booleans | Later authenticated session issue without claiming it caused the first absent DOM selector. |

If retained evidence lacks a field, label it UNKNOWN/NOTCAPTURED as appropriate; label LOST only with Farm's explicit P2 custody fact. No new browser, HTTP, service, seed, preflight, body, graph, collector, control-loop or test probe is authorized by this report. The open permission disposition and Farm STOP remain intact.

## Separation of causes and unchanged contract

P3 1934/1939 establishes a conditional source lifecycle counterexample for the later owner path; it does not explain P2's earlier DOM expectation. Farm report §7's suggestion of a shared readiness issue is unproven; matching summary vocabulary does not connect the stages. P1 second-trim capture/adoption and worker 1945's production diagnostics are separate. None of those files was changed here.

Mounted saves still use `localSaveSession`/persisted outbox/`commitTimeline`. The full v2 request remains `api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label/steps(id,label,intent,tags,command_ordinals,patch,reads)/merge/reads/idempotency_key/dry_run/source/rationale/group_id`. Reply handling remains `{data,receipt}`, accepted/merged/historical-rebased, head/document/records/dependencies/effects/steps/history/undo_steps, preview/would_status, conflict reason plus actual head, and invalid code/path/hint/suggested_command. No private fixture claim, second executor, timeout waiver or selector removal was introduced.

## Verification and handoff

Commands run in the assigned App worktree:

- `git rev-parse HEAD 'HEAD^{tree}'` returned the selected 2107/a3ff source tuple above.
- `git status --porcelain=v1`: exit 0, no output (clean).
- `git diff --exit-code HEAD`: exit 0, no output.
- `git diff --check`: exit 0, no output.
- For each file listed in the worker's `source-audit.log`, `git hash-object <path>` and `git rev-parse HEAD:<path>` matched (18 files, including the gate, Pill, client, harness, both readiness cases and original Gate5 file). These are source-integrity checks, not behavior tests.
- Python standard-library byte audit: find the first and second literal `test('P1 split -> trim new clip:` titles in `tests/e2e/local/three-products.p1-chain.spec.ts`; SHA-256 first title to second title = `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f` (11,614 B); second title to EOF = `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7` (7,612 B). Both match protected values.
- Original Gate5-containing `tests/e2e/local/three-products.spec.ts` HEAD and working blob both `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.
- Targeted tests, full tests, typecheck and lint: **N/A, read-only diagnosis / unchanged code; no fresh PASS.** No test-service or bin/daemon/dispatcher call was made.

Only this flat design report and the assigned worker's normal report/audit/commit-message/DONE files were written; the App worktree stays clean. No source/product/test/collector/config/environment/dependency/pin/lock/schema/generated/kit/Git mutation, no deletions. No plan decision was shown wrong. The choice was to preserve UNKNOWN instead of inventing a fault from absent DOM or a conditional build mode.

Next: independent review of this source verdict; Farm/Proof may supply the existing safe 31814 projection or an explicit field/retention disposition. Establish the earliest actual observed stage separately for both readiness cases before assigning a product repair or requesting a rerun. This diagnosis is complete; actual causal attribution remains evidence-blocked, not a new execution request.
