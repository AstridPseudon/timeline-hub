# Parent swap native record repair

Repaired the existing staged `clip.swap-media` v1 parent carrier. Fresh App output is accepted by the actual private014 SDK with structurally identical command, complete record, and authored result. Authority: Agent `3c4f6de4`, schema SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, matching the brief's ordinary014 a0/f021/6ba source pair. This is pure source qualification, not renewed Runtime/artifact qualification.

## Changes and decisions

- Corrected `resolved` to the selected parent clip; removed swap-only fps/source-window reads and occurrence selection/ownership reads. Native records seven reads in order: clip collection, selected clip, track collection, selected track, asset collection, old asset, new asset. Selections are only clips/tracks.
- Matched native registry rules: guard complete old authored binding; preserve opaque fields and equal direct/nested mirrors; require an existing new alias to equal the exact native four-field binding; otherwise create that binding and its recorded ID. Removed the unsupported same-alias rewrite and sibling traversal. Old registry identity codecs refused by native remain refused.
- Both exact Runtime-verified inputs are mandatory. Both original and replacement intrinsic durations must cover the raw source window. Incoming transitions, absent/null video hold (derived for validation only), and null speed survive without authored normalization. Standin restrictions match the native recipe. No Runtime authority, cap, clamp, or normalization was changed.
- Main's ordinary four-field binding lacks a catalog digest. The pure capture helper now optionally accepts the exact old selection, checks its authored identity, and freezes it with the original bundle. It never fabricates a catalog digest. Missing old pin still throws visibly with input unchanged. `finishParentClipSwapMedia` now consumes the old/new verified-input array. These are row-local helper changes; no wire API/DTO changed.
- The existing swap implementation resides in `parentClipAddCapture.ts`; only its swap/selection helpers and necessary shared pure validation were repaired there. Add-media behavior remains covered by its six unchanged tests. No session/Provider/outbox/core/schema/DTO/API/artifact/lock/pin edit or adapter activation occurred. The private intent has a local type assertion because the unchanged public013 DTO excludes parent ownership; this does not enable public013.

**Correction to the review evidence:** the report's proposed opaque-field projection is wrong for this source. Actual `3c4f6de4` native reads retain the complete old asset binding, including `catalog_digest` and opaque content. The fresh command/record equality test proves this; stripping those fields would introduce another mismatch. No policy decision was changed.

## Exact validation

Run from `/home/user/work/wt/ap2-m2-parent-swap-native-record-repair`:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-swap-native-record-repair/verify.sh
```

**PASS, exit 0:** 2 Vitest files / 14 tests; four exact App/native command, record and authored-bundle comparisons (replacement, incoming transition with absent/null hold and null speed, Main four-field registry with explicit old pin and unrelated occurrence lane). The pure Python bridge submits actual App JSON to `capture_parent_swap_media` and `execute`, then consumes the App JSON record for exact inverse, deterministic replay and replay preserving a disjoint peer edit. Stale source, wrong old/new catalog selections, occupied alias and short original source refuse atomically with native error kinds.

The script retains the exact commands, makes one isolated Agent archive at a time in this worktree, and removes it and the JSON export with an EXIT trap. Its substantive invocations are:

```sh
PARENT_SWAP_PARITY_OUTPUT="$PWD/.parent-swap-parity.json" node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/.parent-swap-native-agent" /home/user/work/venv-app2-native/bin/python src/tools/video-editor/commands/fixtures/parent_clip_swap_parity.py "$PWD/.parent-swap-parity.json"
```

Additional checks, all **exit 0**:

```sh
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-swap-native-record-repair/typecheck.mjs
npm run typecheck:strict-islands -- --pretty false
node node_modules/eslint/bin/eslint.js --no-cache src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts
git diff --check
```

The targeted TypeScript script uses the repository compiler options with strict checking and the touched helpers/test as roots. An initial bare runner-config attempt failed because existing config uses `__dirname`; the final process-only preload supplies it, without changing config/shared dependencies. An initial targeted strict probe exposed public013 intent typing and an existing callback-narrowing issue; both are resolved locally. No tests were weakened, skipped, disabled, deleted, or converted to refusal.

## Limits and handoff

No code blocker remains. All normal Main shapes exercised here are native-positive; no native refusal gap was found in those cases. This is synthetic pure authored-state coverage, not owner-film or live acceptance qualification. The shared adapter remains unactivated. Before activating its existing flat proposal, its owner must pass an exact old pin for four-field bindings and both verified old/new inputs; its previous new-input-only finish call is insufficient. Keep visible draft refusal when these are unavailable, and retain the public013 refusal boundary.

Per brief: no request-test, HTTP/provider/Door/browser/socket/full run, package install, shared dependency mutation, or git mutation. Temporary proof copy/export are absent. Next: owner review/integration of this bounded repair, then separately authorized adapter work and paired live qualification.
