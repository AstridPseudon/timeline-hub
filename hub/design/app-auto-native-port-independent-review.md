# Independent review: corrected native automatic capture

**APPROVE — bounded inactive source unit only.** No blocking findings. This does not approve activation, writer retirement, requester integration, pool promotion or a normal Runtime release.

Reviewed App **`ca51f422597adea38e5f5bd981b7f12fab38fff4`**, branch `tl/app-m2-auto-native-capture-corrected-port`, against **`a103f3ca2e8e66f2837a85c0ddd007962eca66ac`**. The review worktree starts at `7bb885b638838588a0dff81b64b7c34960ac07f3`; the candidate was read through a separate immutable archive, never checked out over the integration or another worker. Only `notes/auto-native-review/` was added in the review worktree. Product code was read-only.

Native pin: Agent **`80f5149631bb2b08c0569a2a53192e14442991e7`**, explicitly archived from `/home/user/peteromallet/astrid-agent`. Review follows PLAN.md and the bounded contract in `design/app-auto-native-capture-corrected-port.md`.

## Findings by candidate line

- `autoCapture.ts:169–182,186–207`: original explicit approval, occurrence owner, reserved clip identity, anchor, preferred lane and saved fallback are copied and deeply frozen. Finishing accepts the saved basis and exact media input; it has no current-head parameter. Completion resolves anchor-after, then saved fallback, then lane-end only without a saved time. JSON-persisted bases reproduce identical results. This is a pure basis, not authenticated task approval; the existing requester still owns the original task/head/output/policy/lifecycle fields.
- `autoCapture.ts:209–237`: shared placement uses whole-shot extent, the anchor's lane and start-frame collision shifting, allowing interval overlap. Completion uses 5 seconds, shared uses 4; video authors literal source bounds and refuses short verified media. The image completion default ignores an explicit duration as native does. Pool promotion refuses explicitly. No owner-approved legacy short-video/default-style preservation is established by this port.
- `autoCapture.ts:58–115,128–164`: corrected guards are produced by actual execution. They retain occurrence timing/map/extent, parent and child fps, source-window absence, exclusive owners, collection shape/order/membership, whole consumed rows, chosen track, pool state, legacy-group eligibility and reserved registry binding. Replay checks original claims before execution and compares all authoritative capture fields afterward. It does not re-resolve placement on a changed head. Whole-row consumed guards, including opaque fields, are intentional native semantics; no stale field-trimmed fixture was accepted.
- `clipMovePrimitives.ts:136–144,193–203,223–243,279–307,337–349`: asset access, tagged collection shapes, collection queries, exclusive-owner query and whole-row births extend the existing state/recording implementation. Complete native record comparisons include query version, members, order, boundaries, reads, bindings, created identities, writes, dependencies and derived writes. Exact existing registry binding is reused; opaque/mismatched bindings refuse; reserved IDs are retained. Original candidate tests also cover colon/prototype-name aliases. No second state store, recorder, compiler, journal or wire operation was introduced.
- `autoCapture.ts:29–40`: `VerifiedMedia` checks structural five-field pin equality, media kind/size and video duration. These checks **do not authenticate a read or prove client provenance**. The future host must obtain selected and verified media through the same actually bound client and preserve invalidation/task/attempt/publication fences. Local or producer metadata cannot supply that authority.
- Inactivity checked by the complete four-file diff and import search: `autoCapture.ts` is consumed only by its test. Runtime files, generated declarations, dependency pins, UI, requester and outbox are unchanged relative to the candidate base. Base generated metadata still says **0.2.8**; its existing generic `EditCommand` can represent these args, which does not qualify their acceptance by the normal server.

Nonblocking size observation: +322 net product lines; 256 test lines / 59,507 bytes in the new test file. The test embeds two large native input bundles and command/record/after hashes, not twelve whole expected bundles. Small helper duplication exists (`MAP_FIELDS` at `autoCapture.ts:20` and `clipMoveCapture.ts:18`, active predicate at `autoCapture.ts:25` and `clipMovePrimitives.ts:49`). This is evidence for later simplification, not grounds to rewrite this port during review.

## Frozen contract and fixture verification

Independently reproduced schema SHA256 `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224` from `astrid/core/timeline/schema/edit-command.schema.json` at the native pin. `PlacementCreateArgs`, `OccurrenceAddMediaArgs` (including `consumed`) and `MediaSelection` are structurally equal to Agent `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00`, whose schema hash is `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd`. These are frozen source contracts, not a final normal Agent/schema/Runtime/client release.

Exact frozen ordinary/shared fixture SHA256 values reproduced:

- `recipe_m2_auto_placement.json`: `89b59a831a8e1b4996ce2ff50b535f8ce2109f167293acf99bf11bde4624b766`.
- `recipe_m2_shared_auto_placement.json`: `888513d3ddbac837f74d27adfd2000e3bd75cbdf5c2c52044ddb1a2cf2309f5e`.

The ORCH expanded handoffs were independently confirmed structurally different (hashes `2d79b76b4c54339460f0f5d1bd45083f83e2784b9dd45b683824362bc2cd1efa` and `68934bfe05399636f54122149ac0aab8fce50e6a68c593c3938ec9af35fb7410`); they were not expected results.

The retained portable exporter imports the frozen native builders, verifies all eight original fixture cases, then independently generates full native commands/capture/records/bundles. Positive births assert native replay, inverse and redo. The App review compares objects directly, without candidate hash expectations or row trimming. Its 164 vectors cover original ordinary/shared cases, preferred/saved image/video policy, fractional trims/speed, at-ms timing, empty owners, exact/opaque registry reuse, source windows, output tracks, exclusive ownership, consumed opaque fields, collection edits, fps/extents, inherited lane and positive unrelated-parent/sibling edits. Forty-eight focused replay counterexamples isolate pool and eligibility changes with an already-bound exact alias across absent/empty pool and absent/null/empty eligibility states. One additional test checks missing approval and five-field contract shapes. Candidate tests separately reproduce all original guard/collision/lifecycle cases.

## Exact commands and results

Executed on 2026-10-20, with these exact path abbreviations:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-native-port-independent-review
C=$W/candidate
N=$W/native
P=/home/user/work/venv-agent/bin/python
D=/tmp/app-coherent-deps12/node_modules
REVIEW=/home/user/work/wt/app-m2-auto-native-port-independent-review
```

Archive setup (directories private to this worker; dependency symlink created only in the private candidate):

```sh
mkdir -p "$C" "$N"
git archive ca51f422597adea38e5f5bd981b7f12fab38fff4 | tar -x -C "$C"
git -C /home/user/peteromallet/astrid-agent archive 80f5149631bb2b08c0569a2a53192e14442991e7 astrid tests/sdk tests/timeline tests/editing_conformance tests/__init__.py | tar -x -C "$N"
ln -s "$D" "$C/node_modules"
```

Private `$W/runner.cjs` sets `globalThis.__dirname = require('node:path').join(process.cwd(), 'config', 'testing');` for the existing runner-loaded config. From `$C`:

```sh
node --require "$W/runner.cjs" "$D/vitest/vitest.mjs" run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**PASS: 7 files / 561 tests, exit 0**, 16.10 s. Log: `$W/candidate-vitest.log`.

From `$REVIEW`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$N" "$P" -m pytest -q -c /dev/null -p no:cacheprovider --basetemp="$W/pytest-native" "$N/tests/editing_conformance/test_recipe_m2_auto_placement.py" "$N/tests/editing_conformance/test_recipe_m2_shared_auto_placement.py" "$N/tests/editing_conformance/test_recipe_occurrence_media.py" "$N/tests/editing_conformance/test_recipe_m2_placement_create_unplace.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$N" "$P" notes/auto-native-review/export.py "$W/independent-vectors.json"
AUTO_NATIVE_CANDIDATE="$C" AUTO_NATIVE_VECTORS="$W/independent-vectors.json" AUTO_NATIVE_CACHE="$W/vite-cache" node "$D/vitest/vitest.mjs" run --config notes/auto-native-review/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1
```

**PASS: 213 native tests, exit 0**, 11.40 s (`$W/native-pytest.log`). One unknown integration-marker warning from an imported fixture; no integration/socket test selected. **PASS: 164 independent vectors exported, exit 0** (`$W/export.log`); **PASS: 165 App crosschecks, exit 0**, 1.44 s (`$W/independent-vitest.log`). An initial smaller 117-test crosscheck run also passed before adding the isolated pool/eligibility matrix.

From `$C`:

```sh
"$D/.bin/eslint" src/tools/video-editor/commands/autoCapture.ts src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.ts src/tools/video-editor/commands/clipMoveCapture.ts --no-cache
```

**PASS, exit 0** (`$W/eslint-candidate.log`). `git diff --check` in `$REVIEW`: **PASS, exit 0**. Read-only `git show` schema structural assertions and frozen/handoff fixture assertions: **PASS, exit 0**.

Private runner/config, `--no-cache`, one worker, no bytecode and pytest cache disabled throughout. No shared dependency, venv or cache was modified; deps12 `.vite`/`.vite-temp` had no files newer than this review's start. Temporary archives/vector output/pytest scratch were removed after validation; regenerate with the commands above. Logs and the portable review sources remain.

## Candidate gaps and next steps

No settled decision was changed. This approval covers the pure inactive port. Before activation the orchestrator must supply the frozen normal release tuple, join the original requester closure/policy to this basis, and add actual same-client verified-media reads with lifecycle fencing. The requester still exposes a generic capture callback and does not implement this adapter. Do not infer retrospective approval for anonymous/recovered tasks or source authority from local metadata.

Pool-only/promotion/keepAsPooled, parent births, fixed-extent growth, legacy-group migration, video unplace and owner-approved short-video/style behavior remain explicit follow-ups. Native tests prove native inverse/redo and strict intervening-write/registry ABA refusal; this App module does not implement client inverse or history-based ABA checks. Real Runtime acceptance, strict ABA through actual accepted history, restart/idempotency/durability, canonical reload and zero legacy writer traffic remain unverified integration requirements.

No full suite, build, browser, socket, project tsc, install, activation, commit, checkout, merge or push was run. No block prevents completing this review.
