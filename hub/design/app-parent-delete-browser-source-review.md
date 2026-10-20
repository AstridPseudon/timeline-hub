# Parent-delete browser source review

**HOLD.** The positive journey is credible source preparation, but the required real parent-delete guard-conflict/draft-retention case is absent. Strengthen the native claim assertions before composed qualification. This review is complete; no product or test files were edited. There is no browser-pass or writer-retirement claim.

Reviewed App `11a9e3236c9172933774397e193a4692fddbc0d4`, tree `2646c6e086f73ce374072e1d03cd904edc2776e7`, against `cee68b807017efc8669c7d75318cf51aa70ec855`; PLAN, `design/app-current013-parent-delete-browser-source.md`, approved product slice `8ecefbd8e6a2726971b9e5a62cf457746a7e10a4`, and actual Agent S2 `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`. Retained Agent and Runtime producer checkouts were clean at the documented d874/`2c4ac180c2220bdad966bc01e95ad230e99ce26a` pins.

**Findings requiring follow-up**

1. **P1 — required parent-delete conflict journey missing.** The sole test (`tests/e2e/local/clip-delete-command.spec.ts:136`) accepts deletion before creating a disjoint Agent track. It cannot encounter a conflicting original delete guard. The source note explicitly calls the omitted case optional (`design/app-current013-parent-delete-browser-source.md:17`), whereas this review brief requires it. Existing M1 move and label conflicts remain useful but do not exercise a captured whole-row deletion against a changed target/collection. Add a separate real UI delete case: hold its original request before Runtime acceptance, make a relevant Agent edit, release it to obtain an actual non-stale-head guard conflict, and verify visible refusal, unchanged remote head/history, and retention of the original delete intent/guards/request body/key across reload and explicit recovery. Require zero legacy writes and no recapture or snapshot fallback. Keep the positive journey intact.

2. **P2 — recorded read/selection/binding claims are underasserted.** Lines 177–182 check only nonempty reads/selections and equality of the stored command. They do not check the actual whole-row read, exact collection selections, command bindings/created IDs, or the separate record reads/selections/bindings. Runtime native acceptance is a meaningful safeguard, but these assertions do not independently pin the requested recorder contract. Add assertions from the actual S2 values below, including tagged collection reads and original whole-row read; compare the record claims as well as its embedded command. Do not invent a parent-owner binding or reuse an occurrence-free golden's empty binding map for this seed.

**Actual S2 contract, verified offline**

The approved App fixture at `8ece:src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_delete.json` is byte-equal to d874's `tests/editing_conformance/fixtures/recipe_clip_delete.json`: SHA-256 `091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa`. Native capture/execute reproduced its complete command, records and after-bundle. That portable fixture deliberately has no occurrences and has `bindings: {}`.

The new browser seed contains `f2-occurrence`, so its actual native command has:

```json
{"bindings":{"collection.owner:collection.clips":"occurrence:f2-occurrence"},"created":[]}
```

Its record binding is exactly `{"key":"collection.owner:collection.clips","ref":"occurrence:f2-occurrence","policy":"fixed","dependencies":[]}`. Native `_recording.py:79–87` binds a collection owner only when it differs from `parent`. There is no parent-owner binding, and no `None` binding assertion is appropriate.

The three selections have `query_version: 1`, `policy: "guard-membership"`, with members/order/boundaries equal to the following ordered lists:

| Key | Owner | Members/order/boundaries |
| --- | --- | --- |
| `collection.clips` | `parent` | `parent/clip:f2-app-clip`, `parent/clip:f2-transition-clip` |
| `collection.occurrences` | `parent` | `occurrence:f2-occurrence` |
| `collection.clips` | `occurrence:f2-occurrence` | `occurrence:f2-occurrence/clip:f2-plate`, `occurrence:f2-occurrence/clip:f2-agent-clip`, `occurrence:f2-occurrence/clip:f2-agent-clear-clip` |

The new-seed command has 221 native reads, including the present complete raw target at path `[]`, both parent collection reads, the occurrence clip collection read, occurrence/shot identity reads and declared dependency reads. The complete result is saved in this worker's `notes/native-command.json`; use actual read contents, rather than hard-coding the read count as a behavioral assertion. Its whole-row expect and root absent write match the new browser assertions exactly.

An offline probe constructed the closure from the actual seed-builder output with local immutable digests, then ran S2 capture/execute, disjoint native track creation and guarded inverse. It verified exact raw deletion, both mirrors, unchanged registry/opaque payload and child closure/manifest, and exact original payload restoration plus the independent track. This proves pure command compatibility only; it does not certify a Runtime publication or UI path.

All Python symbols used by the unchanged `AstridCli.commitCaptured` helper resolve to the pinned d874 source: `capture_move`, `capture_track_create`, `capture_track_set` (the compatibility export exists), and `bundle_from_document`. No substitute provider or helper implementation was installed.

**Positive source assessment**

- The test clicks the rendered raw parent clip and presses Delete. `route.fetch({maxRetries: 0})` reaches the actual Runtime; only the first accepted response is withheld/aborted. It requires a real accepted `clip.delete` v1, receipt, history command/root absent write and immutable readback. No response is manufactured.
- The persisted IndexedDB request is checked against the first network body/key/method/path and original intent. Reload and a real Runtime restart in the same realm preserve that request. Explicit owner-specific recovery must resend identical bytes/identity and return the identical accepted result/receipt without an extra delete publication.
- Both clip mirrors lose only the target. Complete parent-payload equality preserves registry, unrelated clip/occurrence/config/opaque JSON, while child revisions and manifest are compared separately. Raw seed checks include own `__proto__`, `constructor`, `prototype`, nulls and ordered arrays.
- Real UI Undo must submit `timeline.inverse` for the delete publication, accept on the intervening Agent head, restore the complete raw payload plus the independent track, and survive reload. Legacy mutation observation begins before opening the page and is attached to the reopened page; composition/revision/restore mutation traffic must stay zero.
- This App tree contains no native delete product port. Missing composition cannot falsely pass: the first required actual `clip.delete` acceptance at lines 167–175 fails even if a legacy writer runs. The approved 8ece single-delete branch returns after capture/submit failure, so it has no post-capture fallback. Group/multi-delete remain separate and unchanged.
- Both original journey files, shared Astrid/App/build helper bodies, current013 wrapper/tests, group-delete test file, package/lock/runtime lock and public12 archive are byte-equal to cee68. The group-test file, including positive 261, retains SHA-256 `1beea75106b059db7462b080059253688c47a77db16d55ecfbaf438c62ba9fce`.
- Only the explicit `parent-delete` fixture variant changes target opaque data and removes the sibling transition. Removing that transition agrees with native conservative dependency refusal. A deterministic in-memory seed probe proved the ordinary default output identical to base, and the variant identical outside those two changes. Normal main composition seeding still runs before switching startup to `--authoring-profile astrid`; no untrusted statement provider is introduced.
- The new launcher reuses the existing source guards, pins d874/Runtime13/public12, disallows caller dist overrides, checks both source boundaries and propagates failure. Its distinct cache key binds the final App tree and launcher/helper bytes. The normal hosted build helper is unchanged.

**Commands and results**

All commands ran from the assigned App worktree. Definitions below abbreviate the exact absolute paths:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/app-m2-parent-delete-browser-source-review
AGENT=/home/user/work/wt/app-m3-agent013-current-pair-source

node --experimental-vm-modules scripts/testing/current013-parent-delete.test.mjs
# exit 0: 7 passed; experimental VM warning only
node scripts/testing/current013-integration.test.mjs
# exit 0: 15 passed; delegated browser/vendor operations mocked

node node_modules/eslint/bin/eslint.js tests/e2e/local/clip-delete-command.spec.ts tests/e2e/local/support/harness.ts playwright.clip-delete.config.ts scripts/testing/current013-parent-delete.mjs scripts/testing/current013-parent-delete.test.mjs
# exit 0, no diagnostics
env PWTEST_CACHE_DIR=$WORKER/playwright-cache node node_modules/playwright/cli.js test --config playwright.clip-delete.config.ts --list
# exit 0: 1 case, 1 file
env PWTEST_CACHE_DIR=$WORKER/playwright-cache node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
# exit 0: original 7 cases, 1 file
env PWTEST_CACHE_DIR=$WORKER/playwright-cache node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list
# exit 0: original 4 cases including cold-open, 1 file

git show cee68b807:tests/e2e/local/support/harness.ts > $WORKER/notes/base-harness.ts
git show 8ecefbd8e6a2726971b9e5a62cf457746a7e10a4:src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_delete.json > $WORKER/notes/approved-delete-golden.json
git -C $AGENT rev-parse HEAD > $WORKER/notes/agent-head.txt
node $WORKER/notes/probe-seed.mjs
# exit 0: byte-preserved ordinary method/default output and bounded variant
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$AGENT /home/user/work/venv-agent/bin/python $WORKER/notes/probe-native.py
# exit 0: exact approved golden, real helper exports, native seed claims/delete/track/inverse

git diff --exit-code cee68b807017efc8669c7d75318cf51aa70ec855 HEAD -- tests/e2e/local/three-products.spec.ts tests/e2e/local/track-label-command.spec.ts tests/e2e/local/support/astrid.ts tests/e2e/local/support/app.ts tests/e2e/local/global-setup.ts scripts/testing/current013-integration.mjs scripts/testing/current013-integration.test.mjs src/tools/video-editor/hooks/useClipEditing.test.ts package.json package-lock.json runtime.lock.json vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
# exit 0: unchanged; separate byte/hash audit saved notes/preserved-source.json
git diff --check cee68b807 HEAD
git diff --check
git status --short
# all exit 0; no whitespace errors; worktree clean
```

Scoped lint/discovery used public12 through this worker's own temporary `node_modules` link to `/tmp/app-coherent-deps12/node_modules`; the original `/home/user/work/app/node_modules` link was restored. No shared dependency file/link/cache, venv or retained source was written. Playwright compilation cache is worker-owned. The seed probe transpiles only extracted helper text in memory, without typechecking or building the App.

Probe development initially hit a Node synchronous Git subprocess `EPERM`, then two errors in the review-only seed probe (local variable shadowing and module export handling); a dependent native attempt consequently lacked `seed.json`. Inputs were subsequently read from the explicit shell Git captures above, the review probe was corrected, and both final probes passed. No product/test assertion changed to obtain a pass. An initial short `git show d874:...` was ambiguous; all conclusions use the full pinned SHA and clean retained checkout.

**Remaining work and limits**

Add the missing parent-delete conflict source case and precise S2 recorder assertions, then re-review. Compose the approved native product ports in the separately authorized product step after the current tuple's qualification. Register a distinct central parent-delete gate using the final clean composed App tree, literal d874 Agent / `2c4ac180` Runtime pins, client13, the exact public12 archive/count and the recomputed `parentDeleteCacheIdentity`. Run `node scripts/testing/current013-parent-delete.mjs` through that central service. Preserve all 7 M1/4 label cases and group 261; do not reuse their prior result as delete evidence.

No actual browser, localhost/socket, Runtime acceptance, restart/recovery, mounted conflict, UI inverse, build, tsc, full suite or install ran in this review. Positive behavior and zero legacy traffic remain unverified until the later composed central run. No PLAN decision was changed; no execution blocker prevents completion of this read-only review. No KEEP artifact was created.
