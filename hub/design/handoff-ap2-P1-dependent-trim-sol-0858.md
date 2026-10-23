# P1 dependent trim resume: source cause established; correction blocked by scope

Resumed exact WIP `679efb0b0fdb3b542edb210d15991784a51cf3f4`, tree `e87e26728653da3056f57039738f6b4aa50fb4bf`, from `tl/ap2-P1-dependent-trim-sol-0858`. Parent is `c24dfb33e` / original-spec tree `7821bc8430c85190f00e52c2a8d6db91ecca8c7d`. No restart, checkout, commit, merge, push, dependency install, shared-install write, service request, browser, socket, HTTP, build, or full run.

## Result and delta

No functional source fix and no causal green claimed. The mounted regression is retained byte-for-byte from WIP, including two durable intents, predecessor basis, exact raw previous value, and declared read assertions. It remains a normal failing test, not skipped, weakened, or converted to an expected failure. The sole delta from WIP is deleting the temporary `DEPENDENT DIAGNOSTIC` product console warning in `timelineLocalSaveHandoff.ts` (one line). Against c24 the final delta is the inherited 66-line mounted regression only. All other product behavior, wire fields, raw provenance e900, provider guards, and generated artifacts are unchanged.

Original spec remains SHA256 `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`. Original spec/support/helper files are untouched.

## Causal evidence

1. Reproduced the exact mounted RED on this worker: split is sent once and held; the newly selected split ID is used for `handleSelectedClipChange({ from: 3 })`; the durable owner has one intent, not two, before acceptance. See `/tmp/w-c057b906fd/causal-red.log` and final `/tmp/w-c057b906fd/focused.log`.
2. Temporary test-only observation, removed after capture, is retained in `/tmp/w-c057b906fd/diagnostic.log`. Before trim the new clip has `clipType: media`, `at: 2`, `hold: 6`, `from: 0`, `to: 8`, `speed: 1`. After the real trim handler and commit funnel, both local config clips omit `from`, `to`, and `speed`; their hold values remain 2 and 6. The owner remains saving with the held first request. No handoff diagnostic/refusal is emitted.
3. `useClipEditing.ts:235` handles the timing patch and emits the real rows mutation with gesture basis. `useTimelineCommit.ts:305` materializes rows through `rowsToConfig`. `lib/timeline-data.ts:373` classifies every numeric-hold clip as hold timing and explicitly deletes `from`, `to`, and `speed`, independent of `clipType`. This discards the explicit Source In edit before the handoff can encode it.
4. `timelineLocalSaveHandoff.ts:151` correctly treats omitted display fields as partial, preserving the original raw fields instead of clearing them. All remaining values are unchanged. `documentPatchIntent.ts:216` returns null for no changes; `localSaveSession.ts:287` returns without appending an intent. Thus there is no second intent for canonical acceptance or dependent revalidation to send. This is upstream authored-state loss, not a demonstrated Runtime consumed-read refusal, outbox predecessor race, or fixture selector targeting the wrong control.
5. The normal inspector exposes Source In for the registered media descriptor (`ClipPanelBody.tsx:378`), while the serializer selects timing mode from numeric hold. This explains why the original mixed media-plus-hold fixture reaches a real editable control yet its edit has no effect. Changing UI input sequencing, longer waits, or outbox guards cannot restore a field already lost in row materialization.

## Decision evidence requiring the orchestrator

The minimal causal location is `src/tools/video-editor/lib/timeline-data.ts`, which is outside the task's allowed product files. I did not force timing fields back into a downstream handoff/commit path or change the clip fixture to avoid numeric hold. App A2 should own a reviewed correction of media/hold timing precedence across the existing editor, serializer and duration behavior, with this mounted RED retained.

There is also a separate incompatible assertion in the fixed original spec: seed line 98 authors `from: 0`; passing split assertions at lines 410–412 require the right clip to equal the original except ID/at/hold, hence still `from: 0`; line 431 subsequently expects the trim patch previous value to be `SPLIT_AT` (2). The mounted regression correctly retains `before.value: 0`. A missing-second-intent fix alone cannot make both original assertions true. I did not change them; Proof P1/orchestrator must resolve this evidence under the settled-plan process. This is a report of a contradiction, not a substituted acceptance criterion.

## Retained service2754 evidence and limits

Read the retained service2754 log, summary and snapshot manifest in `orch/tests/ap2-P1-provenance-original-spec-port-0820-ap2-P1-chain-h6-1023085133-2754/`. It records two failures: first case line 423 expected two posts, received one after 90 seconds, after split acceptance/new-ID/raw closure assertions; second case fails in the Python helper with literal backslash-newline SyntaxError. The helper is separately owned and untouched.

The advertised snapshot `/home/user/work/wt/.test-ap2-P1-provenance-original-spec-port-0820-ap2-P1-chain-h6-1023085133-2754` no longer exists. Prior worker searches also found no retained P1 trace ZIP/error context. Therefore no service2754 browser-trace inspection is claimed. The mounted source causal evidence is local and does not prove a repaired original HTTP journey, later merged/refused replies, lost ACK, or restart. H3 remains NO-GO.

## Commands and results

All commands ran from `/home/user/work/wt/ap2-P1-dependent-trim-resume-sol-0905`. Logs/configs are private in `/tmp/w-c057b906fd`, the actual directory named by this worker's `tmpdir` file.

- `ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-c057b906fd/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx -t 'persists an inspector trim'`: exit 1, exact expected-two/got-one RED. Diagnostic rerun with the temporary observations reproduced the same failure.
- `ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-c057b906fd/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts`: exit 1; 108 passed, 1 failed, 6 files (5 pass, 1 fails). Sole failure is the retained mounted regression at line 196. Existing strict negatives and accepted/merged/conflict/invalid/restart/dependent/late-reply/strict mounted cases pass. Log `focused.log`.
- `timeout 45s node node_modules/typescript/bin/tsc -p /tmp/w-c057b906fd/tsconfig.app.json`: exit 124 twice, no diagnostics before each 45-second ceiling. App typecheck is unverified; no larger timeout used.
- `timeout 45s node node_modules/typescript/bin/tsc -p /tmp/w-c057b906fd/tsconfig.node.json`: initial exit 2 (private config could not resolve `vite/client` through typeRoots); corrected only the private config to name `/home/user/work/app/node_modules/vite/client`, rerun exit 0. Logs `type-node.log`, `type-node-fixed.log`.
- `timeout 45s node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx`: exit 0, no diagnostics (`lint.log`).
- `git diff --check`: exit 0.
- `sha256sum tests/e2e/local/three-products.p1-chain.spec.ts`: unchanged exact d727 digest above.

The private Vitest/TS configs were copied from the prior working config and repointed to this worktree and this worker's temp directory, reusing its import-loader fix. Vitest config SHA256 `38e43e4eb2a0c77491b94be74763a12ff72d8278070f5d6e103ab74cfc726165`. Composition aliases reuse the existing private extracted graph in `orch/workers/ap2-P3-env-final-0407/record/private/node_modules/@banodoco/timeline-composition`, whose retained graph manifest identifies archive SHA256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. The original archive path is now absent, so I did not reattest archive equality. No shared package files were written. `node_modules` resolves to `/home/user/work/app/node_modules`; caches are private and `--no-cache` was supplied.

Read-only exact pin checks: Agent checkout `b8e5076250cc37cadf88c1ce699f2a05511fb909`; Runtime checkout `a5d4258312c979024865ee704da2d632ca5b2730`. No Python Agent/Runtime modules were imported by this worker. The separate normal-34e environment was not run; do not infer its qualification from this JS test run.

## Next steps

1. Independent review of this causal classification and original-spec contradiction.
2. App A2: authorize and correct the actual row serializer/timing-mode boundary with existing behavioral coverage; preserve raw/opaque fields and real consumed reads. Keep the mounted two-intent assertion.
3. Proof P1/orchestrator: resolve the incompatible previous-from assertion without silently weakening original behavior, incorporate the separately reviewed helper fix, and own the original real-body journey after source review.
4. Re-run the same mounted regression for causal green, then the permitted App typecheck in its normal runner. No P1/H3 pass until integrated original accepted/merged/refused/lost-ACK/restart behavior is proven.
