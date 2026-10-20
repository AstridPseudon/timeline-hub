# Manual native ADD independent review — HOLD

Reviewed App **ace8a84e075c5967605d0c27d61f19df5afef454** against original chooser **bcd610db8e530454da7029e0479fe81e52bbd156**. Read PLAN.md, the owner/manual recovery policy, chooser authority/fix reviews and the adapter worker report. No product or repository test changes. No settled decision changed.

## Blocking finding: attempted handoff is mistaken for a submitted command

**P2 — a pre-capture cancellation or atomic native refusal permanently strands the retained choice.** [runtimeRecoveryPlacement.ts](/home/user/work/wt/app-m2-manual-native-add-independent-review/src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.ts:93) sets `reserved.submitted = true` BEFORE awaiting the session. The session still awaits basis conversion, checks cancellation/readiness/idle ownership and runs native capture before enqueue ([commitSession.ts](/home/user/work/wt/app-m2-manual-native-add-independent-review/src/tools/video-editor/commands/commitSession.ts:295)). Any of those steps can refuse without creating an intent. The adapter then rejects every subsequent call at line 49, including a corrected choice, directing the user to Retry/recovery although no command exists there. `finally` clears only `pending`.

Two ordinary failing assertions reproduce this using the real session and fake IndexedDB (public client reads/send are mocked, as in the worker's adapter tests):

1. Original valid video draft (`on=8.125`, source `[2,6)`). Abort its signal at the session handoff, then call the original session method. Its post-conversion cancellation check refuses. Assert zero sends and empty outbox intents. Retry the unchanged draft with a fresh signal, expecting success and the original reserved child ID: **FAIL**, `Manual choice already submitted; use the command owner’s Retry or recovery, keeping the original request`.
2. Set only source `to=7` while verified duration is 6. Native capture refuses atomically; assert zero sends and empty intents. Restore `to=6` and request again: **FAIL**, same error. Changing the choice cannot release the latch because the unconditional submitted check precedes its key comparison.

Repros: [adapter-controls.test.ts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review/adapter-controls.test.ts:207); final log: [controls-final.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review/controls-final.log). These remain normal failing behavior expectations, with no skip/xfail or refused-behavior substitution. Existing positive tests remain intact.

Recommended correction: let the existing session distinguish **no enqueue occurred** from **ownership of an intent was transferred**. Keep the reserved ID available for unchanged choices after a pre-enqueue refusal/cancellation. Once an intent is transferred, preserve its original IDs/body/key and direct retry/recovery through that owner. Do not indiscriminately clear `submitted` in a catch: persistence/network failures after enqueue must remain protected. No new queue/coordinator is needed. Add the two cases to the normal adapter suite, then re-review the bounded change.

## Requirements traced

| Requirement | Evidence and limit |
| --- | --- |
| Explicit original identity | Adapter validates project/timeline, raw occurrence, shot and internal revision, original parent lane and explicit child track against the original canonical document; display names/IDs are not parsed. Session compares original head/publication, accepted document and reconstructed bundle. No latest/default timeline fallback. |
| Explicit time and pin | Chooser's original blank `on/from/to` fields and validations remain. Adapter requires an authored occurrence start, computes child `at = on - start_ms/1000`, and uses explicit `hold=to-from`; video keeps `[from,to)`, image requires `from=0` and emits hold without window fields. No legacy four-second/append/collision default or inferred anchor. Exact five-field selection is retained and compared with same-client VerifiedMedia. Native capture refuses unsupported maps/ownership/window/track shapes. These explicit time semantics are documented as a proposal, not parity with the old append action. |
| Existing owner only | `createRuntimeRecoveryPlacement` only calls `getBinding()`; it creates no sessions, outboxes or locks. Missing/replaced/client-mismatched/scoped/actor bindings refuse. Actual session checks stopped/readiness, dirty/sending/pending appends/intents and original head/bundle before enqueue. Private controls prove a closed session sends nothing and creates no owner, and a second chooser on an actual retry-busy session leaves its existing pending body/key/intent unchanged. Existing narrow session/hook suites cover close/switch and dirty suffix preservation. |
| Cancellation and uncertainty | UI edits/unmount abort the supplied signal; session rechecks after asynchronous basis conversion. The **pre-enqueue retry latch defect above remains blocking**. After enqueue, existing tests prove unknown outcomes retain one durable intent and retry the exact body/key/IDs. Definitive Runtime conflict retains its intent/draft. |
| Accepted state | Adapter emits no Placed notification or optimistic preview. It uses existing enqueue/persist/pump and accepted closure projection; the supplied detached acceptance fixture is not a real Runtime proof. |
| Owner/manual policy | Unknown historical placement remains “Placement unconfirmed”; “Not placed” still requires the exact readable retirement evidence. No task-authority inference, automatic placement or media-only producer guard was added. |
| Original chooser behavior | Diff against bcd adds only two cancellation cases to its test file. Every original test input/assertion remains. Both duplicate keyboard cases pass, and all eight original private authority controls pass, including same-label tracks, cross-occurrence collisions, pointer/keyboard routing, stale draft and five-field pins. Private controls adapt only displayed ordinal-prefixed names, retaining raw chosen identities and original media/source. |

The binding remains **unqualified**: TasksPane passes no callback; `useTimelineCommandSession` owns its session privately and this factory has no production host connection. Its supplied `{client, session}` must be a stable binding from the actual existing owner, invalidated on switch/close. Matching the supplied client object does not independently prove how the session's send closure was constructed. The normal opener outside an editor is also unqualified: existing owner-specific outbox locks cannot be assumed to exclude a second owner for the timeline. This patch does not attempt that fallback.

## Actual frozen native parity and provenance

Executed **unmodified archived source** independently at BOTH:

- S2: `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`.
- Candidate: `905a4f0f1dcadf92a226b1da0baba50b8a37178d`.

The private [native-parity.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review/native-parity.py) supplies plain commands to each frozen Agent's own `execute`, capture builders, replay, inverse and canonical document exporter. It compares every command claim, record and entire authored bundle/document against the checked-in App fixtures. **Each revision passes 17 complete command/record/bundle cases (2 original + 15 own-key cases), 12 occupied-alias refusals and 12 changed-membership/reservation replay refusals.** Successful cases also pass native replay and inverse; refused cases preserve caller state. Both exported complete results hash to SHA256 `8f94caa1db92508d052b47544c25a2de43919ac865c5caed5995101c9859f0ae`.

Additional fixture provenance: S2's original `recipe_m2_occurrence_media.json` SHA256 is `761153bb5c9de335d212c033bce976315a6846c4bde456b1d32f6aeb35919ad6`; its complete parsed add/swap fixture equals the App fixture, including all inputs, verified media, outputs, commands and records. Candidate905's compact fixture SHA256 is `cf9650d82a3171236dd72a14ca1df2fabee8184edbef63d2020f5eeebcc15d69`; its shared inputs/verified media, outputs and commands match (record factoring is covered by execution above).

Thus the new exclusive-owner, pool/group absence/presence and earlier child membership claims come from canonical native execution, not an invented App guard table. The frozen native handler itself calls `_exclusive`, reads pool/pinnedShotGroups and selects clips even when `consumed` is empty. The S2→905 handler difference is only automatic consumed-clip reads (whole row→specific timing/lane fields); this manual path sends no consumed list. The worker's later `cf7448ed` was **not assumed equivalent** to either target.

Own-key checks cover `__proto__`, `constructor`, `toString`, own descriptors/prototype preservation, tagged absence/null, clone/JSON roundtrip, immutable claims and unrelated opaque authored data. Complete bundle equality/native inverse ensures unknown fields survive. Narrow App tests additionally cover malformed codecs and non-JSON inputs.

Source minimality: 13 changed paths, net +5057 lines (product net +475; tests +683; fixtures +3899). Recipe/primitive difference from retained App `938e454b5` is only the 15-line owner/pool/group/member delta. The rest carries the existing recipe/tests plus bounded adapter, session ingress and chooser cancellation. No whole staged root/hook/proxy/automatic cohort, generated/client/pin edits, legacy fallback writer, receipts, attestation or second coordinator was imported. Retained pure SWAP is tested but not exposed by this manual ingress.

## Runtime correction and qualification boundary

The worker report's unresolved `0132c4` shorthand is **not a missing API**. Published producer **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`** exists. Its `packages/typescript/src/generated.ts:181` exposes `getProjectVerifiedMedia(projectId: string, selection: MediaSelection): Promise<VerifiedMedia>` at the normal five-field `/media-selection/verified` read. Read this exact source and the published runtime-current-tuple document; no Runtime mutation/test was performed.

This App still pins `182a7dd8446456162a452a25c8493256c5da29fe` and exposes the needed operation only as a local structural capability. Normal generated-client/pin adoption and same authenticated host/client/session wiring are pending, with actual Runtime acceptance, raw reload, inverse/redo, restart/retry, mixed edits and zero-legacy traffic **OPEN**. No browser or activation qualification is inferred from these mocked transport/session tests.

## Exact commands and results

Run from `/home/user/work/wt/app-m2-manual-native-add-independent-review`. `REVIEW` below is this worker's named private scratch; config root/aliases/setup are based on repository config, with runner-compatible paths, private cacheDir and extra private test include. Private `node_modules` link points read-only to `/home/user/work/app/node_modules` solely for resolving external review tests. No shared dependency/cache files were changed.

```sh
REVIEW=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review
VITEST=/home/user/work/app/node_modules/vitest/vitest.mjs
node "$VITEST" run --config "$REVIEW/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.test.ts \
  src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx \
  src/tools/video-editor/commands/occurrenceMediaCapture.test.ts \
  src/tools/video-editor/commands/occurrenceMediaPrimitives.test.ts \
  src/tools/video-editor/commands/occurrenceMediaOwnKeysCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
```

**8 files / 361 passed; exit 0; 24.77s.** [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review/targeted-consistent.log).

```sh
node "$VITEST" run --config "$REVIEW/vitest.config.mts" --configLoader runner --no-file-parallelism --maxWorkers=1 --no-cache \
  "$REVIEW/adapter-controls.test.ts" "$REVIEW/authority-controls.test.tsx"
```

**42 tests: 40 passed / 2 failed; exit 1; 7.06s.** Adapter private copy retains all 30 original tests, plus four independent controls (two pass/two fail); authority controls 8/8 pass. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-manual-native-add-independent-review/controls-final.log).

```sh
for ref in 26ef2bbb 905a4f0f; do
  mkdir -p "$REVIEW/agent-$ref"
  git -C /home/user/peteromallet/astrid-agent archive "$ref" astrid tests/editing_conformance/fixtures pyproject.toml | tar -x -C "$REVIEW/agent-$ref"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$REVIEW/agent-$ref" \
    /home/user/work/venv-agent/bin/python -B "$REVIEW/native-parity.py" "$ref"
done
git diff --check HEAD^ HEAD
git diff --check
git status --porcelain=v1
```

**Both frozen native executions exit 0**, results above. Git checks exit 0; worktree clean. Native archives were extracted from read-only `git archive <ref> astrid tests/editing_conformance/fixtures pyproject.toml`; shared venv supplies dependencies only and `-B` prevents bytecode writes.

Environment issues, not hidden: initial 8-file run used CLI/config from `/tmp/app-coherent-deps12` while test imports resolved this worktree's shared App dependency tree; it reported 347 passed/14 missing Chai DOM matchers. Aligning runner/config with the existing shared App tree fixed all 361 without changing tests/dependencies. First external-control run additionally could not resolve `@testing-library/react`; adding only the private scratch dependency link fixed collection. Its two retry failures persisted. Final run added one busy-owner control; no broad test loop.

No full suite, build, tsc, browser, localhost/socket, install, shared dependency/venv/cache mutation, product/test edit, git commit/merge/rebase/checkout/push or branch/ref change. Private reproductions, exported result JSON and logs are retained outside the worktree; temporary native archives/cache were removed after verification. The native command above recreates its archives. No build/temp output remains in the worktree.

## Decision and next step

**HOLD** the source candidate for the single pre-enqueue/submitted-state defect. Fix that boundary minimally while preserving all original positive and uncertain-retry expectations, re-run these narrow controls, and obtain independent re-review. Separately perform normal published client/host binding adoption and its authorized real-pair qualification. There is no external blocker to completing this review; DONE marks the review complete, not product approval. No KEEP requested.
