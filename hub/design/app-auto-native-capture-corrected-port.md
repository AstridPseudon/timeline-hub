# Corrected native automatic capture — bounded inactive source port

Completed the source unit on App base `a103f3ca2e8e66f2837a85c0ddd007962eca66ac`. This does **not** activate automatic placement or qualify a Runtime release. No requester/outbox, UI, root/pin, producer authority, generated type or dependency files changed.

## Source pins and matching goldens

- Native source: Agent **`80f5149631bb2b08c0569a2a53192e14442991e7`**, read by immutable `git show`/`git archive`, including the corrected timing/lane/exclusive-owner handlers and the subsequent pool-absence/legacy-eligibility guards. Source paths: `astrid/sdk/timeline/{native_auto_placement,native_occurrence_media_commands,native_placement_commands,_recording,_command_state,_collections,capture}.py` and `astrid/core/timeline/duration.py`.
- Its canonical schema SHA256 is `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224`. `PlacementCreateArgs`, `OccurrenceAddMediaArgs` (including optional closed `consumed`) and `MediaSelection` are structurally identical to approved 22-op generation source **`0a0ac7baaa74e15485b10bcbaa80eda1afe48c00`**, schema SHA256 `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd`. This establishes the source contract only; no generated DTO adoption is claimed. The existing generic `EditCommand` carries these published native args; no generated fields/types were manufactured.
- Exact same-source native fixture `tests/editing_conformance/fixtures/recipe_m2_auto_placement.json`: SHA256 `89b59a831a8e1b4996ce2ff50b535f8ce2109f167293acf99bf11bde4624b766`.
- Exact same-source native fixture `tests/editing_conformance/fixtures/recipe_m2_shared_auto_placement.json`: SHA256 `888513d3ddbac837f74d27adfd2000e3bd75cbdf5c2c52044ddb1a2cf2309f5e`.
- The two ORCH `handoff-agent-expanded-*` JSONs differ from these fixtures **structurally as well as bytewise**. Their hashes are respectively `2d79b76b4c54339460f0f5d1bd45083f83e2784b9dd45b683824362bc2cd1efa` and `68934bfe05399636f54122149ac0aab8fce50e6a68c593c3938ec9af35fb7410`; they were not used as expected results.
- `workers/app-m2-auto-native-capture-corrected-port/export_vectors.py` executes the unchanged pinned native builders, verifies all eight original fixture cases, and exports complete commands/capture/records/after bundles. Four additional native vectors cover image/video saved fallback and preferred lanes. Native replay and inverse are asserted during export; redo is additionally asserted for the eight original cases. Retained `vectors.json` SHA256: `ad0a0d423d513cf22d201d450ebb9aaeb5402f7a2a397b5613a832271bb7f8ae`. The App suite embeds the exact original bundles, native capture explanations and twelve complete command/record/after hashes. Hashing sorts object keys only, retaining array order and binary64 values.

## Allowlist and size

| Path under `src/tools/video-editor/commands/` | Change |
| --- | --- |
| `autoCapture.ts` | New, 238 lines / 16,486 bytes: original-basis snapshot, completion/shared pure resolution and guarded birth execution. |
| `autoCapture.test.ts` | New, 256 lines / 59,507 bytes including compact native input data and golden values. |
| `clipMovePrimitives.ts` | +85/-1 lines: existing state/recorder gains native occurrence/clip/track collection queries, exclusive-owner query, asset access and whole-row births. No second recorder. |
| `clipMoveCapture.ts` | Four existing numeric/rational/origin functions exported; implementations unchanged. |

Net product increase: **322 lines**; tests: 256 lines. No new dependency, command/op, query key, API, journal or writer activation.

## Behavior and guard vectors

`captureAutoBasis` freezes the caller's explicit original approval and authored bundle. `finishAutoCapture` receives a required five-field completed-media selection plus the detached `VerifiedMedia` result; it accepts no current head. `executeAutoBirth` verifies original read/selection claims before executing and compares every authoritative capture field afterward. Same original basis/pin/IDs yields identical commands/records, including through JSON persistence. A changed head is never substituted into the approved capture.

The resolution follows native completion 5 seconds (image ignores explicit duration, video uses 0..5 unless explicitly approved otherwise), saved fallback/preferred lane, lane-end fallback only when no saved time exists, shared 4 seconds, whole-shot extent, inherited anchor lane, start-frame collision shift and overlap policy. Rational frame quantization uses the existing exact Fraction-to-binary64 helper; start and duration round separately. Registry births create or require the exact binding, without overwriting opaque/mismatched entries; raw reserved IDs, including colons and Object-prototype asset names, are preserved.

The adversarial suite covers image/video modes, anchor timing/source window/speed, membership/order/member-ID collision, parent/child fps, occurrence origin/extent, chosen-lane validity, exclusive-owner retarget, pool absence, migration eligibility and reserved registry changes. It also covers inherited-lane changes, collision-start occupation, absent-anchor membership on saved fallback, changed five-field pins, invalid verified facts, short-source refusal, exact registry reuse, same-ID retry and tampered guards/consumed IDs. Saved fallback remains literal under unrelated clip-timing/name edits. Input bundles and saved commands remain unchanged on refusal.

## Exact validation

All commands ran from `/home/user/work/wt/app-m2-auto-native-capture-corrected-port`, except the native archive execution, whose imports are explicitly pinned below. These shell abbreviations expand to the exact absolute paths used:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-native-capture-corrected-port
N=$W/native
P=/home/user/work/venv-agent/bin/python
```

Final App targeted command:

```sh
node --require $W/snapshot-vitest-runner.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**7 files / 561 tests passed; exit 0**, 20.55 seconds. Log: `$W/vitest-final.log`. Earlier four-file run: 334 passed, before the final additional raw-ID/lane/image-duration controls. Original passing neighboring tests were unchanged.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$N $P $W/export_vectors.py
```

**12 native golden/record/after vectors exported; exit 0**, with matching fixtures and replay/inverse/redo checks described above.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$N $P -m pytest -q -c /dev/null -p no:cacheprovider --basetemp=$W/pytest-native $N/tests/editing_conformance/test_recipe_m2_auto_placement.py $N/tests/editing_conformance/test_recipe_m2_shared_auto_placement.py $N/tests/editing_conformance/test_recipe_occurrence_media.py $N/tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
```

**213 passed; exit 0**, 11.59 seconds, one unknown `integration` marker warning from an imported fixture module because the isolated invocation does not load the repository marker config. No integration/socket test was selected. These are the original native tests at the pinned source; their detached ABI fixture is not a current Runtime pairing. Initial source extraction needed the unchanged `tests/timeline` fixture dependency as well as `astrid`, `tests/sdk`, `tests/editing_conformance` and `tests/__init__.py`; the initial import-only attempt without it failed, then extraction was corrected. The temporary archive and pytest scratch are removed after validation; regenerate them with read-only `git archive` from the SHA above when rerunning.

```sh
/tmp/app-coherent-deps12/node_modules/.bin/eslint src/tools/video-editor/commands/autoCapture.ts src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.ts src/tools/video-editor/commands/clipMoveCapture.ts --no-cache
node $W/check-types.cjs
git diff --check
```

**All exit 0.** Scoped TypeScript compiler-API check: **0 diagnostics**, strict/noEmit, only the four files plus their import closure; no project tsc. Its first run found three ordinary typing errors, fixed before the final run. `$W/types-final.log` retains the final result. The runner uses read-only physical deps12, a private runner file, `--no-cache`, `--configLoader=runner` and one worker. Shared dependencies/caches/venvs were not written. No install, full suite, build, browser, localhost/socket, commit, merge, checkout or push was run.

## Open pair/activation gate and exact limits

1. **Normal Runtime 22-op generation/release is staging.** The closed 14-op Runtime 0.2.9 tuple cannot qualify these automatic births/consumed guards. Require the orchestrator's frozen normal Agent/schema/Runtime/client tuple and actual selected/verified-media/acceptance rechecks before adoption. No pin/type changes belong to this source unit.
2. **The original requester callback is still inactive.** Existing outbox/requester task admission bytes/key, approval/head/closure/owner/anchor/lane/fallback/policy/output/created IDs and async identity fences were inherited unchanged and passed their targeted tests. This module has no task/attempt/publication authority. It does not invent a decoder binding the opaque `OutboxPlacementInput.readClosure`/`policy` JSON to the new local pure basis. The authorized ingress must supply the actual original authored closure and exact native approved fields; the host must read `getProjectVerifiedMedia` from the SAME bound client as selection and retain its lifecycle fences. That adapter/public host-read work is separate, as assigned. Pure tuple equality cannot prove transport/client provenance.
3. **Pool promotion/pool-only/keepAsPooled are not ported.** A shared request whose asset is already pooled is held explicitly because this App base has no `shot.pool` semantic executor. The native source and its guards are finished; the omitted executor is a concrete App follow-up. This port adds no alternative snapshot writer or second queue.
4. Parent-owned births, growing fixed occurrence extent, video unplace, legacy-group migration and owner-approved short-video/default-style preservation remain outside the qualified subset. Native short-source refusal is documented as a pre-existing difference from legacy behavior, not closure of a lost positive requirement. Existing manual/gallery/recovery and anonymous-task presentation are untouched; no retrospective automatic approval or “not placed” inference is introduced.
5. Native conformance proves exact inverse/redo and existing guarded inverse machinery was untouched. This port does not implement a client inverse or claim real Runtime strict-ABA, restart/idempotency, browser durability, accepted canonical reload or zero-legacy-traffic qualification. Pair and execute those original requirements before activation or writer retirement.

No settled policy was changed. The bounded inactive source unit is complete; the open gates above remain explicit recommended next work. DONE denotes this source task only.
