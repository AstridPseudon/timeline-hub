# Independent review: selected PARAM authenticated retained-read bridge

**APPROVE the bounded bridge at `89bb04462`, against `64d7e19b3`. Production activation remains gated.** No blocking bridge finding. Read PLAN, the authenticated-read-bridge report, the production-binding source report and the original-pin authority audit. No settled decision changed; no product or repository test edit made.

## Scope and implementation

The complete diff is six paths, +302/-1: four product paths (+45 lines) and two test paths (+257/-1). It adds only the optional two-method `DataProvider.paramReadClient`, project-scoped forwarding through `RuntimeDataProvider`'s existing facade, the facade's guarded forwarding through existing `withSession`/`WorkspaceClient`, and the one `useTimelineSave` argument. Existing exact-retained helper, capture/acceptance, generated clients, package pins, validator, hydration and preview/render bodies are unchanged.

- `dataProvider.ts:332–341`: both methods reject another project synchronously before I/O. The provider project/client are constructor-bound; its capability object is stable. No second connector or authority cache.
- `client.ts:592–619`: the supplied pin is copied before negotiation. Existing `withSession` authenticates; the read closure holds its original base/client, then checks the current slot/opening and shared fence before and after its awaited work. Observed actor/realm/instance comparisons run before retained I/O and before returning its result. Reconnect invalidates the opening; no latest-source fallback or new endpoint is added. These checks detect observed identity changes; they do not claim a fresh remote identity request on every GET.
- `commitSession.ts:486–508`: existing scope, original pin, capture identity, head, local/read/projection generations and readiness checks surround retained prefetch. Only validated matching exact document/object metadata becomes the frozen capture inputs. The helper still leaves portable-byte/schema validation to native capture/acceptance.
- `useTimelineCommandSession.ts:183–215`: existing data/head/read-generation/session/disposal checks reject stale prefetch results; effect cleanup invalidates reads and disposes the old session. Its stopped check runs after prefetch too. Provider/project replacement or unmount cannot submit a late read into the replacement session.

## Refusal lifecycle

No new read path projects an accepted result or invokes a successful-state callback on failure. `useTimelineOps.setClipParams` clones literal command input before awaiting prefetch and submits only on success. `SelectedElementParamFields.apply` sets the submitted observation only after that awaited call returns; its catch preserves raw draft text, and draft clearing requires actual acceptance. `commitSession` updates acceptance/outcome and projects server after-state only when durable dispatch records a new accepted intent.

The real provider/save-hook bridge tests show accepted4 while 8 is pending, then accepted8 only after ACK. Literal16 reaches the synthetic rejecting server unchanged, preserving literal16/clear/original pin/verified inputs in the durable outbox and accepted4 on screen. Unavailable document/object reads and late client/project/disposal changes send zero commits. Existing mounted cases additionally preserve raw text under refused/validation/conflict outcomes and read failure, allow corrected retry, and cancel an unfinished read. No behavior expectation was weakened.

## Independent validation

CWD `/home/user/work/wt/app-m2-selected-param-read-bridge-independent-review`; Node22.22.0 / Vitest4.1.5. Worker-private `private12/node_modules` supplies the tracked Composition0.0.12 tarball; other dependencies are read-only links. Private TMPDIR/cacheDir, runner loader, cache disabled, one worker, no file parallelism. Scripts/configs, diagnostic probes and logs are under `$N` below. The preparation script records the private overlay setup and can recreate it after cleanup.

```bash
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-read-bridge-independent-review/notes
python3 -B "$N/prepare-test-env.py"
python3 -B "$N/audit-deps.py" > "$N/deps-before.json"
env TMPDIR="$N/tmp" node --require "$N/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineSave.selectedParams.test.tsx src/integrations/runtime/client.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/retainedParamInputs.test.ts
env TMPDIR="$N/tmp" node --require "$N/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx --testNamePattern='sends raw16 under V1|operational retained-read error|captured basis changes during retained reads|cancels an unfinished retained read'
env TMPDIR="$N/tmp" node --require "$N/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.probes.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
python3 -B "$N/audit-deps.py" > "$N/deps-after.json"
cmp "$N/deps-before.json" "$N/deps-after.json"
git diff --stat 64d7e19b..HEAD
git diff --numstat 64d7e19b..HEAD
git diff --exit-code HEAD -- src package.json package-lock.json vendor config
git diff --check 64d7e19b..HEAD
```

| Run | Result | Log |
| --- | --- | --- |
| Bridge/provider/client/exact-retained helper | **4 files / 166 PASS**, exit0, 9.55s | `notes/bridge-provider-helper.log` |
| Selected mounted refusal lifecycle | **6 selected PASS**, exit0, 5.20s; 11 unselected by explicit name filter | `notes/refusal-lifecycle.log` |
| Independent private boundary probes | **8 PASS**, exit0, 2.08s | `notes/boundary-probes.log` |
| Dependency/cache comparison and diff checks | **exit0**, shared observations identical, no worktree product/test change | `notes/deps-before.json`, `notes/deps-after.json` |

The private probes exercise both document and object methods: an existing fence refuses before any traffic; a fence installed during handshake prevents retained traffic; a second real facade observing a replacement realm fences the first facade's pending read; repeated exact reads negotiate once but fetch twice without cached inputs. They use the existing public constructor/identity-store surface and synthetic Transport, with the original bearer credential checked on every request. They are diagnostic scratch outside the repository, not replacements for main-suite evidence.

The prior 315-test result was read, **not repeated or counted as this review's pass**. No full suite, build, browser, localhost/socket, tsc, install, live Runtime acceptance, or admission build ran. The synthetic maximum10 refusal proves transport/draft handling, not native semantic validation. The mounted tests supply their own authoritative pin/ops and do not prove production PropertiesPanel ingress.

## Remaining actual gate and handoff

The bridge resolves the missing authenticated-read capability only. **Original selected-target DocumentPin authority is still unresolved**, as documented in `design/app-selected-param-original-pin-authority.md`; its native probes were not rerun here. A canonical closure may have no pack documents, or multiple retained versions without a selected-clip association. Current admission/catalog binding and a unique manifest match do not establish the historical original pin. The Agent edit-contract owner must identify or define the authoritative accepted association for parent and occurrence clips, including empty/multiple-pin cases. No inference/accessor/hydrator was introduced in this bridge.

`PropertiesPanel/PropertiesPanel.tsx:522–559` still does not pass `retainedDocumentPin`, `timelineOps`, or `commandState` to ClipPanel. After the authority answer, wire those existing seams with the original captured basis/pin and qualify the actual Props→panel→ops path. Native maximum10 accept8/refuse16 after V2/removal/restart, restart-safe lost-ACK retry, inverse/reload and browser zero-legacy traffic remain open qualification. This APPROVE does not close or bypass those gates.

No blocker for this read-only review. Recommended next step: land/review the bounded bridge and keep production activation gated on that authority answer, UI wiring and actual qualification. Shared dependency/cache/venv/runtime trees were not written; the worker-local node_modules link is restored and private dependency/cache/temp output removed after testing. No Git mutation or KEEP marker.
