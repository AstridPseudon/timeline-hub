# D141 documentary qualification: PASS; zero-REG qualification: FAIL

One product regression is proved for the preserved caller-load predicate. `normal-033-shot-group-pack` is cut FAIL / pristine PASS, not `nonREG-both`. The corrected immutable-input join has 33 distinct IDs: 32 `nonREG-own-test`, one `productREG`, zero `nonREG-both`, and a separate `UNKNOWN` collection error. There is no REG0 claim.

## Decisive shot-group evidence

All Git citations below are read from `/home/user/work/app` objects, not the Composition hosting checkout. Cut is `867cb2737af1b46dc608c7cd37c349e920fe9422`; pristine is `7ca61bb3280beca21d98a854af266a382f7ce5df`.

The production editor calls this function: cut `src/tools/video-editor/components/AstridTimelineEditor.tsx:348-363` passes the selected timeline ID, version and locator to `duplicateShotGroup`. Both trees have the identical `src/tools/video-editor/lib/shot-group-pack-commands.ts` blob `015ce2d5f182ed711ba51ea8f8bb44af7edd2d0a`: the initial version-check load is at line 388, the no-final-video branch avoids task admission, and mutation is at lines 410-418.

Pristine `src/shared/lib/placement/placementService.ts:78-106,119-138` makes one initial `loadTimeline` call and one mutation-cycle `loadTimeline` call: two counted reads. Cut `placementService.ts:233-243,247-279,341-369` makes the initial read, then two unconditional basis reads at lines 252 and 259 before dispatch: three counted reads. The second basis read belongs to production's local-staleness check at lines 257-263.

The mock delta does not account for the extra count. Cut `src/tools/video-editor/lib/shot-group-pack-commands.test.ts:37-49,68-74` increments for both load methods; its reply-assembly read increments once and immediately subtracts once. Its net effect is zero. Pristine mock save at lines 48-65 has no load. The source delta is limited to mock migration, mock globals, and hooks; the exact input and protected assertion remain at pristine lines 320-343 and cut lines 377-400. Cut real `src/integrations/runtime/dataProvider.ts:746-767` sends the request/key and consumes the returned closure without a new head read; its basis loader at lines 885-906 performs an actual history read. This is a production caller change, not an invented mock-only side effect.

Exact receipts under `ORCH/tests/`:

- `app-full-1026004326-12174/log.txt:39012-39028`: same full title, `expected 3 to be 2`, assertion at cut test line 397. File summary at line 37172: six tests, one failed.
- `app-D141-pristine-receiver-0007-full-1026010029-23581/log.txt:32`: that file passes all **six** tests. The prior join's claim of eight is also corrected. The exact title is present in pristine source, and none of its IDs appears in the pristine failed-ID list.

Preserved input: `documentFixture`, remove final-video key, project `demo-project`, active non-default timeline, version 7, source `shot-source`/`V1`, destination `shot-copy`, same wait callback. Preserved predicates: lineage, ordered source/copy IDs, two loads, one `rev-2` publication, no task requests and no relational path. Assertions after the load-count failure were not reached in the cut receipt; they receive no execution credit here.

For manager allocation only, the smallest product root is the second basis read in `createDocumentStore.load`, cut `placementService.ts:259`, within guard lines 257-263. The qualified affected set is exactly `normal-033-shot-group-pack`. This proves a regression of the protected caller-load count; it does not prove corrupt duplicate output. No author is assigned, no fix is proposed, and no additional consumers are declared affected.

## Complete finite membership and counts

Every one of the 33 exact file/title pairs matches exactly one terminal normal `FAIL` record. Ours-only membership was rechecked against pristine Git objects: two A3 IDs and three runtime-elements IDs have absent files; the 20 generated prepared-video IDs and seven Undo IDs have no counterpart in pristine's older eight-test `useTimelineSave.test.tsx`. Their absence is recorded as `absent`, never PASS or `nonREG-both`. This is membership qualification only; stopped own-test investigations were not reopened.

Normal terminal receipt: FAIL exit 1; Test Files 5 failed / 1356 passed / 1361 total; Tests 33 failed / 19734 passed / 19767 total (`log.txt:39032-39033`). **Four files carry failed test IDs; the fifth is the collection error.** Pristine: FAIL exit 1; Test Files 3 failed / 1276 passed / 1279 total; Tests 18 failed / 17856 passed / 17874 total (`log.txt:18920-18921`). Node is NOTRUN in both, not zero or PASS.

Separate normal collection error: `src/tools/video-editor/commands/commitSession.genericPatch.test.ts:7`, raw normal log lines 38802-38814. Expected schema digest `sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2`; received `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`. The file is absent upstream; no test ID executed. It remains separate `UNKNOWN`, without diagnosis, adaptation or behavior credit.

## Pristine dependency seam and finite next receipt

All 18 exact pristine failures match their terminal records. Fifteen share the first frame `TimelineRenderer.tsx:1594:25`; one has the assertion frame `TimelineRenderer.public-host.qualification.test.tsx:272:14` with the same renderer error; two have missing registry values at `TimelineRenderer.test.tsx:23:23` and `:32:19`. Thus 16 IDs share the renderer error, including the assertion-frame ID; the prior prose's arithmetic was ambiguous.

The existing generic runner selects worker-local `node_modules`, otherwise shared App dependencies (`bin/test-run:198-200`). The old receiver currently has no `node_modules`. Shared composition is 0.0.10 and shared theme is absent. Pristine package/lock bytes instead require file-linked vendor composition 0.0.2 and theme 0.1.0. Pristine Vitest config lines 18-33 and 45-79 select composition registry/theme API by install paths, including fallback stubs. The dependency mismatch is real; the claim that it explains all 18 failures remains provisional. Historical receipts did not emit a complete install/environment manifest. Current observations corroborate the prior packet, rather than proving all historical install bytes.

`pristine-targeted-recipe.json` gives the existing **targeted**, three-file route and all 18 IDs/frames. Those files contain 27 tests (12 public-host, 12 shots, three registry); file selection runs these 27, not exactly 18 by title. It must reconcile the original 18 plus nine neighbors. A future ordinary App worker can own a fresh lock-derived pristine install; generic service selection then uses that worker's install. No package substitution, shared dependency mutation, source adaptation, install or submission occurred here. The recipe records service cache and actual runner-environment limitations. No repeat full is justified.

## Custody and scope

Both original raw result directories, KEEP material, 0043 controller packet and 0120 packet remain unchanged. Source tree equivalence is sufficient for this source-based finite finding; no HEAD-only rerun is requested. The observed pristine synthetic commit `4bb696aceae83a3843df47ff1ff99c9717a3e0aa` has tree `974de7cd08900872eeb0bd6f6004d44323e01fab` and parent `7ca61bb3280beca21d98a854af266a382f7ce5df`, independently verified with `git cat-file -p`. It is not the pristine commit identity. No HEAD-dependent failure was observed. Normal source tree is `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`. Its cut merge has two parents: `263b728f014040afc9c6b3fdfb54963b93b757eb` and `9ada0d906a2efc5cf98b18b112d2d4e9d0657098`; 0120 listed only the first. No removed snapshot post-cleanup guard is invented.

The PLAN U3/A2/A3/F and C0 sections 1-5 and 7 boundary remains unchanged. No writer, product, test, fixture, mock, assertion, generated file, kit, hub, pin or Git metadata changed. D141 own-test/B022/Element/SWAP/profile investigations stay stopped; D130 remains on absolute hold. Node qualification is a separate authorized phase after journeys. This source-unchanged evidence repair adds no semantic review gate.
