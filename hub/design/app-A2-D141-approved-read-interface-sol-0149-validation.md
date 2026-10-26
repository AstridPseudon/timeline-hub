# A2 D141 REG validation

Base `867cb2737af1b46dc608c7cd37c349e920fe9422`, tree `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`. Expected candidate tree `af51793b7cc9b2d0426e629bce1d9e4529a7edb6` (computed without Git writes; confirm actual harness commit/tree/parent). Node `/opt/node20/bin/node --version`: `v20.20.0`. Dependencies resolve to `/home/user/work/app/node_modules` and were read-only. All scratch/cache/build output is under `/tmp/w-fb50658194`; no shared caches/install/venvs changed.

## Authenticated RED retained

Sol0130 `evidence/validation.md` records the exact same original 6+16 file run on the same frozen base: 21/22 PASS, shot-group duplicate FAIL expected 2 got 3; all16 Workspace controls PASS. Controlling independent packets are `workers/app-F-D141-reg-join-sol-0126/evidence/{shot-group-verdict.json,join.json}` and `workers/app-F-D141-shot-group-wholepath-0126/evidence/{verdict.json,source-map.json,findings.md}`: cut full12174 FAIL versus pristine23581 exact case PASS. This classification is accepted; no duplicate-output-corruption claim or rebaseline.

## Candidate commands and results

- `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run src/tools/video-editor/lib/shot-group-pack-commands.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts --maxWorkers=3 --no-cache --configLoader=runner --config /tmp/w-fb50658194/vitest-d141.config.mjs` -> exit 0, **2 files / 22 tests PASS**: shot-group 6/6, Workspace16/16. Final duration 2.89s. Run after final interface-support edit. Earlier initial candidate execution also passed22/22 (5.02s); repeat was justified by making the new mock refuse an across-await pair mismatch. No other suite files ran.
- `PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.app.json` -> exit 0, zero diagnostics (initial and final after last mock edit).
- `PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.node.json` -> exit 0, zero diagnostics.
- `PATH=/opt/node20/bin:$PATH npx --no-install eslint src/integrations/runtime/dataProvider.ts src/tools/video-editor/data/DataProvider.ts src/shared/lib/placement/placementService.ts src/tools/video-editor/lib/shot-group-pack-commands.ts src/tools/video-editor/lib/shot-group-pack-commands.test.ts` -> exit 0, zero diagnostics, including final mock edit.
- `git diff --check` -> exit 0, no output.
- Python byte-conservation audit: removing just the added combined-reader mock method restores the WHOLE upstream test to original SHA256 `73c55e476ded3c40bedb4176f9e56624b9cce26bf6b3d0e749f151622a079eb2`. All original titles/inputs/assertions/counters and loads=2 are byte-exact; no original mock changed. Workspace guard file and all traced P1/P2/P3 specs, LocalSaveSession/outbox and mounted caller remain byte-exact (blobs in source-manifest).

No full, browser, live socket/service, journey, core, profile, swap/element or other own-failure investigation was run. Parent full evidence remains immutable. No source merge or Git write.

## Faithful private runner wrapper

Existing Sol0130 __dirname workaround; no repository config/setup/aliases/tests modified for runner execution. Both existing config helper roots resolve ../.. to this worktree; all plugins/reporters/setup are inherited. --no-cache and private cacheDir prevent shared install writes.

```js
globalThis.__dirname = "/home/user/work/wt/app-A2-D141-approved-read-interface-sol-0149/config/testing";
const { default: config } = await import("/home/user/work/wt/app-A2-D141-approved-read-interface-sol-0149/config/testing/vitest.config.ts");
export default { ...config, cacheDir: "/tmp/w-fb50658194/vite-cache", test: { ...config.test, cache: false } };
```

Final exact targeted output:

```text

 RUN  v4.1.5 /home/user/work/wt/app-A2-D141-approved-read-interface-sol-0149

 ✓ src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts (16 tests) 876ms
     ✓ places a generation by publishing a new head revision  699ms
 ✓ src/tools/video-editor/lib/shot-group-pack-commands.test.ts (6 tests) 64ms

 Test Files  2 passed (2)
      Tests  22 passed (22)
   Start at  01:55:59
   Duration  2.89s (transform 1.66s, setup 624ms, import 1.72s, tests 941ms, environment 1.70s)

```

## Focused cold/await production-source exercise

Private source-path exercise only, not an extra Vitest suite, a live Runtime/authentication proof, or a successful final-video pack proof. The real RuntimeDataProvider full closure reader, combined reader, actual display/version reader, preparation/continuation, full authoring validation, and duplicateShotGroup run unchanged. Only low-level AstridRuntimeClient read endpoints use explicit fixtures. getRecoverableIdentity deliberately throws at the boundary, so a stable cold caller reaches it but stale cases cannot create any owner/intent or run the transform. It does not replace main-suite evidence above.

Exact build command (after writing the verbatim probe source below):

```sh
/opt/node20/bin/node --input-type=module - <<'JS'
import { build } from './node_modules/esbuild/lib/main.js';
await build({entryPoints:['/tmp/w-fb50658194/ordering-probe.ts'],outfile:'/tmp/w-fb50658194/ordering-probe.cjs',bundle:true,platform:'node',format:'cjs',target:'node20',tsconfig:'tsconfig.app.json',alias:{'@':process.cwd()+'/src','@astrid/editor-sdk':process.cwd()+'/src/sdk/index.ts','@banodoco/timeline-schema':process.cwd()+'/src/test/shims/banodoco/timeline-schema.ts'},define:{'import.meta.env':JSON.stringify({DEV:false,PROD:true,BASE_URL:'/'})},logLevel:'warning'});
JS
/opt/node20/bin/node /tmp/w-fb50658194/ordering-probe.cjs
```

Build exit0; exercise exit0, **six focused controls PASS**. One earlier private build failed before source execution because esbuild requires a JSON literal for define; fixed only the private build invocation with JSON.stringify. No test/product/config edit was made for the probe.

```json
{
  "status": "PASS",
  "controls": 6,
  "trace": [
    "history:revision-1:publication-1",
    "parent:revision-1",
    "inspect:revision-1:publication-1",
    "parent:revision-1",
    "history:revision-1:publication-2",
    "parent:revision-1",
    "inspect:revision-1:publication-2",
    "parent:revision-1",
    "PASS:cold-provider-actual-version",
    "history:revision-1:publication-2",
    "parent:revision-1",
    "publish-during-combined-await",
    "inspect:revision-1:publication-3",
    "parent:revision-1",
    "PASS:combined-publication-mismatch",
    "history:revision-1:publication-3",
    "parent:revision-1",
    "inspect:revision-1:publication-3",
    "parent:revision-1",
    "history:revision-1:publication-3",
    "parent:revision-1",
    "identity-boundary",
    "PASS:cold-production-caller-two-basis-reads",
    "history:revision-1:publication-3",
    "parent:revision-1",
    "inspect:revision-1:publication-3",
    "parent:revision-1",
    "publish-after-preflight-await:revision",
    "history:revision-1-next:publication-3",
    "parent:revision-1-next",
    "PASS:awaited-revision-mismatch-no-owner",
    "history:revision-1-next:publication-3",
    "parent:revision-1-next",
    "inspect:revision-1-next:publication-3",
    "parent:revision-1-next",
    "publish-after-preflight-await:publication",
    "history:revision-1-next:publication-3-next",
    "parent:revision-1-next",
    "PASS:awaited-publication-mismatch-no-owner",
    "history:revision-1-next:publication-3-next",
    "parent:revision-1-next",
    "inspect:revision-1-next:publication-3-next",
    "parent:revision-1-next",
    "publish-at-validation-await",
    "history:revision-1-next:publication-3-next-validation",
    "parent:revision-1-next",
    "PASS:post-validation-await-no-owner"
  ]
}
```

Verbatim source (SHA256 `7f8cd065701f02f21611d8d3dacc25143eb407d336720316a722fd8b36552767`):

```ts
import assert from 'node:assert/strict';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { prepareTimelineDocumentMutation } from '@/shared/lib/placement/placementService.ts';
import { duplicateShotGroup } from '@/tools/video-editor/lib/shot-group-pack-commands.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';

// Read-boundary fixture only: production readers, closure validation, caller and
// continuation execute unchanged. No network, save owner or Runtime mutation.
const project = 'cold-project';
const timeline = 'active-non-default';
let revision = 'revision-1';
let publication = 'publication-1';
let afterParent: undefined | (() => void);
let identities = 0;
let mutations = 0;
const trace: string[] = [];
const config = { ...createDefaultTimelineConfig(), pinnedShotGroups: [
  { shotId: 'source', trackId: 'V1', clipIds: [], name: 'Source' },
] };
const payload = { config, registry: { assets: {} }, occurrences: [] };
const manifest = { shots: [], internal_timelines: [], media: [], documents: [] };
const client = AstridRuntimeClient.prototype as any;
client.listTimelineCommits = async () => {
  trace.push(`history:${revision}:${publication}`);
  return { head: { revision_id: revision, publication_id: publication }, items: [], next_cursor: null };
};
client.getProjectParentCompositionRevision = async (_project: string, _timeline: string, pin: string) => {
  trace.push(`parent:${pin}`);
  const record = { project_id: project, timeline_id: timeline, revision_id: pin,
    content_digest: fixtureDigest(payload), payload: structuredClone(payload), dependency_manifest: manifest };
  const hook = afterParent; afterParent = undefined; hook?.();
  return record;
};
client.inspectTimeline = async () => {
  trace.push(`inspect:${revision}:${publication}`);
  return { project_id: project, timeline_id: timeline, head_revision_id: revision, revision_id: revision,
    representation: 'canonical_head', authority: 'runtime_parent_composition', is_current_head: true };
};
client.getProjectTimeline = async () => ({ project_id: project, timeline_id: timeline,
  head_revision_id: revision, head_publication_id: publication });
client.getRecoverableIdentity = async () => { identities++; trace.push('identity-boundary'); throw new Error('probe identity boundary'); };
async function main() {
  // A genuinely cold provider obtains its counter from the existing display read.
  const provider = new RuntimeDataProvider({ projectId: project });
  const first = await provider.loadTimelineCommandBasisWithDisplay(timeline);
  assert.equal(first.timeline.configVersion, 1);
  assert.equal(first.basis.head.publicationId, publication);
  publication = 'publication-2';
  const second = await provider.loadTimelineCommandBasisWithDisplay(timeline);
  assert.equal(second.timeline.configVersion, 2); // Same revision, distinct publication.
  assert.equal(second.basis.head.publicationId, publication);
  trace.push('PASS:cold-provider-actual-version');

  // Head moves across the await between immutable assembly and display observation.
  afterParent = () => { publication = 'publication-3'; trace.push('publish-during-combined-await'); };
  await assert.rejects(new RuntimeDataProvider({ projectId: project }).loadTimelineCommandBasisWithDisplay(timeline),
    /changed while pairing authoring basis and display/);
  trace.push('PASS:combined-publication-mismatch');

  // The real production caller uses the prepared continuation from a cold provider.
  identities = 0;
  const start = trace.length;
  await assert.rejects(duplicateShotGroup({ projectSlug: project, timelineRef: timeline, configVersion: 1,
    source: { shotId: 'source', trackId: 'V1' }, destinationShotId: 'copy' }), /probe identity boundary/);
  assert.equal(trace.slice(start).filter((event) => event.startsWith('history:')).length, 2);
  assert.equal(identities, 1);
  trace.push('PASS:cold-production-caller-two-basis-reads');

  // Awaited preflight can never authorize a stale captured pair (both dimensions).
  for (const dimension of ['revision', 'publication']) {
    identities = 0;
    const prepared = await prepareTimelineDocumentMutation({ projectSlug: project, timelineRef: timeline, configVersion: 1 });
    await Promise.resolve().then(() => {
      if (dimension === 'revision') revision += '-next'; else publication += '-next';
      trace.push(`publish-after-preflight-await:${dimension}`);
    });
    await assert.rejects(prepared.mutate(() => { mutations++; }), /changed before placement authoring/);
    assert.equal(identities, 0);
    assert.equal(mutations, 0);
    await assert.rejects(prepared.mutate(() => { mutations++; }), /already consumed/);
    trace.push(`PASS:awaited-${dimension}-mismatch-no-owner`);
  }

  // The post-validation read is after the validation await, not before it.
  identities = 0;
  const prepared = await prepareTimelineDocumentMutation({ projectSlug: project, timelineRef: timeline, configVersion: 1 });
  queueMicrotask(() => { publication += '-validation'; trace.push('publish-at-validation-await'); });
  await assert.rejects(prepared.mutate(() => { mutations++; }), /changed before placement authoring/);
  assert.equal(identities, 0);
  assert.equal(mutations, 0);
  trace.push('PASS:post-validation-await-no-owner');
  console.log(JSON.stringify({ status: 'PASS', controls: 6, trace }, null, 2));
}
main().catch((error) => { console.error(error); process.exitCode = 1; });
```

## Limits and handoff

Only required local source/test qualification is claimed. ONE independent protected review is still mandatory before normal merge. Existing Runtime notes owner must install the proposed ledger/ZIP-note text via canonical owner routes. Manager must record actual harness commit/tree and re-prove affected integrated-head P1/P2/P3 paths/selectors; no whole-App full repeat. D130 absolute hold, D141 other-failure stops and private/raw KEEP remain unchanged.
