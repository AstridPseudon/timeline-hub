# P1 terminal-chain disposition: one oracle mismatch established; second cause evidence-blocked

## Result

**P1 FAIL; H3 NO-GO.** Service `ap2-P1-P3-ops-identity-return-1015-ap2-P1-chain-h6-1023101921-28486` remains **2 failed / exit 1**. No journey rerun, source/test/fixture/ops/pin change, or substituted passing body.

| Actual failure | Independent classification | Smallest correct next action |
| --- | --- | --- |
| First case, spec:448, expected hold 5 / actual 6 | **Classification PASS: wrong oracle boundary for this numeric-held Source In edit.** Actual result agrees with the reviewed UI transform and explicit hold preservation; this is not evidence of a product duration bug. Original test still FAIL. | Proof P1 owner: separately propose and independently review a test-only expectation based on the original split's explicit hold and the actual from-only gesture, preserving every other guard/assertion. No silent expected-6 substitution and no passing-body claim. |
| Second case, spec:519, expected two POSTs / actual one | **P1 refusal proof FAIL; exact causal classification BLOCKED.** Proven failure is missing second App dispatch, with no observed Runtime refusal. The retained artifacts cannot establish whether capture legitimately refused a changed basis or lost a valid stale intent. | OPS/service evidence owner: recover the exact 28486 trace/error-context artifacts first; A2/P1 then identify the concrete thrown error and displayed/raw/outbox state. No unchanged body retry or product fix before that evidence. |

## Exact identity and scope

Read PLAN first, especially §3 P1/A2, C0 §§1–5, reviewed 0959 composition and 1004 review, Source In 0913/0932/0939 evidence, production callers, mounted regression, helper, and actual 28486 log/manifests. Repository CLAUDE.md was read as repository context.

This worktree is exactly `0cdc76782833d594776452e07706acb406c51553` / tree `654a66946da8a4da65248576a9eb5e32a9e8d382`. `git diff --exit-code 1117c15f7e37a087a1175ea0e923958ce8a4132d HEAD` exited 0. The service `snap` names the same tree. The following SHA-256 values match the service command guards:

- `useTimelineSave.test.tsx`: `3c967d0b4ac5de8541656ab185a68f88c02ba820ffa850fc59b8389de1031834`.
- `useTimelineCommit.ts`: `edee1fad387e3952736cf0bb99c2dd7a9b92133290b1dbdfea40db8a14d7cbfe`.
- `serialize.ts`: `a4c4c01fbfd21ab080876d6daf3ae6eee83dd60717568917cea89509b51de309`.
- `serialize.test.ts`: `d206079fd18c2e6a02dc0634e5891b5f02fa934e6fcb9291f79467f4c3f68e76`.
- P1 original spec: `06104227304e7bab77e8f3f2de131ef26a949db437d02c2b2d7e20a25c057518`.
- Python helper: `02a42eb29b122599301b04a26360ad9676f09dcf4e3fa81d21f898aeb379710e`.

Read-only pin checks: Agent `b8e5076250cc37cadf88c1ce699f2a05511fb909` / tree `eee66dc206817b16f0621087a12505389ec41630`; Runtime `a5d4258312c979024865ee704da2d632ca5b2730` / tree `f74b016ea837f8148db4a602c972073a226ed177`. These agree with the service's command guards. Its `ext` manifest separately reports integration-repo heads ef851b22/c6c69f36; that does not replace the command's exact mounted b8/a5d pins. No Python imports or new runtime/provider execution were performed here. Current-head alignment 1022 and source author 1014 Session metadata remain separately owned and untouched.

All product, test, fixture, support, operational, generated, dependency, and pin files stayed read-only. No Git writes, service submission, browser, localhost/socket, HTTP/native14, build, full suite, daemon, hub, dispatcher, or upstream operation. Reports and completion metadata only are written under the assigned ORCH paths; diagnostic config/logs are in the assigned `/tmp/w-7ba3d777ad` temp directory.

## First case: why explicit hold 6 is correct here

Actual retained log: `orch/tests/ap2-P1-P3-ops-identity-return-1015-ap2-P1-chain-h6-1023101921-28486/log.txt:125–148`. The sole diff at the failure is hold 5 versus 6; exact new ID, at 2, from 3, and to 8 match.

The original seed (`tests/e2e/local/three-products.p1-chain.spec.ts:97`) explicitly authors `clipType: media, from: 0, to: 8, speed: 1, hold: 8`. This is a numeric-held clip in the existing editor despite the media descriptor. `lib/editor-utils.ts:138` classifies hold by numeric `hold`; its split branch at :306 spreads the original clip, sets left hold 2, and creates the right ID with at 2 / hold 6 while retaining from 0 / to 8 / speed 1. The spec's already-evaluated full split equality at :413–414 requires exactly that behavior. It does not split the source window.

The inspector's Source In handler (`components/PropertiesPanel/ClipPanelBody.tsx:150, :384`) calls `onChange({from: value})`. It does not request a hold change. `hooks/useClipEditing.ts:235` captures the actual current config/registry as trim basis and changes that selected clip's metadata. `lib/clip-editing-utils.ts:11` recalculates the action end using numeric hold before source span: with at 2 / hold 6 / speed 1, the action still ends at 8. Thus the **current row's duration remains 6**, even though the inspector's media-derived source-span display can compute `(8-3)/1 = 5`. A derived display number is not an authored change to hold.

`hooks/useTimelineCommit.ts:316` materializes the current rows through `rowsToConfig` and then `withHeldClipSourceFields`. `lib/timeline-data.ts:367` serializes the held row duration as hold 6. The reviewed helper (`lib/serialize.ts:147`) restores only supplied from/to/speed metadata and leaves hold untouched. The 0959/1004 reviewed intent explicitly requires that behavior. The exact mounted regression (`hooks/useTimelineSave.test.tsx:168–268`, the reviewed 108-line addition on the composed base) preserves two persisted intents and canonical predecessor adoption, asserts raw from-before 0 and declared from-read 0, and expects the final right clip to retain hold 6 / to 8 / speed 1 with from 3. The existing serializer test `serializes a held media Source In edit without changing its duration, Source Out, speed or app timing` asserts this boundary directly. Both pass in this worker's bounded run.

C0 §2 says `doc.patch` performs explicit guarded changes and does not clear/default unspecified fields; §1 preserves the captured operands/reads and original created IDs; §4 makes the complete merged canonical result authoritative. Nothing in C0 makes a from-only patch implicitly rewrite an explicitly held duration as source-out minus source-in. Changing product hold to 5 merely to satisfy line 448 would contradict the actual requested transform and reviewed mounted behavior.

**No weakening decision:** a permissible later test-only correction must assert unchanged numeric hold from the exact split baseline, rather than derive it from the source span. Keep exact from 0→3, ID, at, to, speed, full raw/opaque/null/absent/closure comparisons, both mirrors, declared dependencies, complete replies, key/raw retry bytes, accepted/merged/refused, lost ACK, restart, and undo coverage. Independently review all later oracle assumptions against the actual chosen gesture; do not remove them to get past the next failure. In particular the later `app.astrid` absence assertion at :454 was not reached and is not cleared by this finding. The helper's existing explicit app.for/app.until removal capability is not proof that this inspector gesture requested their removal. No fixture changes are proposed in this slice.

Actual evaluated proof stops at :448. The full raw closure/opaque assertions after that, lost ACK abortion/recovery, Runtime restart, exact replay, and final history assertions remain protected but are **unverified in this actual run**. The merged response's HTTP 200, `status: merged`, canonical presence, receipt equality, step dependencies, rebased-onto Agent pair, and preceding trim guard/base-pair assertions were reached successfully before this failure; this is partial live progress, not H3 credit.

## Second case: established boundary and missing causal evidence

Actual retained log :160–185 fails at spec :519 after 90 seconds, `traffic.posts.length === 1`. Therefore the preceding statements completed: split response checks; genuine newline-fixed `commitCaptured(... kind: move, on: 3 ...)`; Agent accepted/unrebased result; exact unchanged left clip; right clip's ID/at 3/from 0/to 8/hold 6; and its exact app `astrid: {fixed_start: true, for: 6}` baseline checks. The actual inspector helper completed Source In fill 3 / Enter / Tab. Only the split POST was observed by the page traffic recorder. The Runtime 409 assertions at :521 onward were never evaluated.

`support/astrid.ts:214–253` now joins Python with real newline characters. It reads the exact scoped historical base and closure, calls native `capture_move`, then real `client.timelines.commit`. It does not fabricate an App refusal. This removes the prior Python SyntaxError as this run's cause.

The following is **source control-flow evidence, not a claim about which branch 28486 took**:

1. Display transform is the real Source In → selected clip handler → materialization path above. It should retain a nonempty from-only delta for this held clip if its current value is 0. The first actual case and mounted regression demonstrate that path under their own ordering; they do not prove second-case capture after ACK/poll/Agent activity.
2. `hooks/useTimelinePersistence.ts:1009` captures each local document before debounce and stores the capture promise. At :676 it awaits that promise **before** invoking the save mutation/flush. A capture error can therefore yield zero additional POSTs.
3. `hooks/timelineLocalSaveHandoff.ts:61–105, :206–241` checks the exact verified source/head, raw entity binding, mirrors, unchanged session document, and exact gesture config/registry against the original local authoring input. Concrete existing refusal messages include `original verified authoring head is unavailable`, `upstream source differs from the verified authored parent`, and `gesture read basis differs from the original local authoring input`. These guards must not be bypassed or recaptured from a newer head to manufacture a request.
4. Existing tests explicitly verify that stale gesture bases and refreshed/foreign/missing publication heads refuse without changing the session document or dispatching. A same-document/no-change capture also appends no intent (`documentPatchIntent.ts:216`, `localSaveSession.ts:282–288`). Current input value, actual basis, or outbox state from 28486 is required to distinguish those cases.
5. `useTimelinePersistence.ts:846–876` routes a local `TimelineVersionConflictError` into diverged/draft retention; it does not create an HTTP 409. `localSaveSession.ts:102–121` has a different rollback path, requiring an existing pending outbox outcome of `rejected` from transport before it loads/adopts canonical. Neither rollback nor a visible message can be inferred solely from POST count 1. The actual App display, message, thrown error, pending state and rollback were not retained in the accessible log.
6. A clean poll can retire and reassemble the owner (`useTimelineSave.ts:131–144`), while dirty chains retain original physical bindings. Whether any poll adopted the Agent head before the inspector edit is unknown; no source-only argument can resolve this ordering.

**Artifact blocker:** the advertised directory
`/home/user/work/wt/.test-ap2-P1-P3-ops-identity-return-1015-ap2-P1-chain-h6-1023101921-28486`
is absent (`ls -la` exit 2). Its two named subdirectories `three-products.p1-chain-P1-412c2-ACK-restart-and-exact-retry` and `three-products.p1-chain-P1-c924b-p-rolls-back-with-a-message` are therefore unavailable. Read-only searches under `/tmp` and `/home/user/work` found the 28486 service log/manifests only, with no matching snapshot/trace/error-context copy. The service result directory has request/snap/ext/status/exit/summary/runner.log/log.txt, no browser output. The retained log names trace attachments but contains no browser console error, snapshot, outbox dump, raw commit body, or full reply payload. I requested an alternate retained location asynchronously; no alternate is available at report time. No trace inspection or exact full live request/reply reconstruction is claimed.

Thus **do not classify this as a successful/legitimate local prevalidation rollback**, and **do not classify it as a proven product loss of stale intent**. Both need the absent actual state/error evidence. What is proven is a pre-response dispatch gap and the missing real-refusal proof. Increasing the poll timeout or retrying this unchanged body provides no causal repair.

## C0 refusal semantics and next bounded ownership

Reviewed the full-v2 request construction (`localSaveSession.ts:160–179`), structured reply checks (`three-products.p1-chain.spec.ts:34–92` and Runtime data provider), C0 request/reply/undo rules, and original second-case guards. Retain ABI 1, project/timeline IDs, exact base revision/publication, nonempty label and steps, command ordinals/per-step patches, merge and real reads, dry_run false, idempotency key, stable allocated IDs, async persisted queue, complete canonical adoption before dependent dispatch, provider-only dependencies, and accepted/merged/error envelope validation. No fabricated reads/guards or force save.

A further **unevaluated source/oracle concern**, not a third observed failure: original second-case :538–542 requires `atomic_scope_changed` at parent root. An inspector trim that carries its existing real gesture basis supplies precise timing reads and `merge: fields` (`timelineLocalSaveHandoff.ts:251–305`). C0 §§1/3 and b8 `_commit_patch.py:227, :778` select atomic fallback only for omitted request reads (or explicit atomic); fields-mode overlapping field reads produce a field conflict, not necessarily parent-root atomic. If the actual trim request is eventually recovered/dispatched, review its real merge/read boundary before adjudicating that specific assertion. **Do not remove or rewrite the original 409/root assertions now, omit reads to force atomic, invent an error, or count a local refusal as a Runtime 409.**

Bounded next steps:

1. **OPS/service evidence owner (1015 / service custodian):** recover only the exact 28486 trace ZIPs, error contexts and any retained App/runtime logs to a durable worker evidence path. No body rerun, row edits, dependency edits, pin changes, or daemon work requested here. This is the immediate blocker for the second classification.
2. **Proof P1 owner:** independently reviewed test-only proposal for first-case held-duration oracle, justified by the exact source transform above. Preserve all later assertions and no-weakening review. It remains a failing journey until actually executed through its full original obligations on the accepted integrated source.
3. **A2/P1 diagnostic owner after artifact recovery:** correlate gesture input, displayed head/current rows, original authoringSource, raw canonical clip, handoff error, queued/pending/rejected record, and message with Agent-move timing. If a valid captured stale request is lost, create the smallest causal mounted regression and assign a source repair through the normal App owner. If exact source correctly refuses an incompatible local basis, assign a separately reviewed fixture/scheduling proposal that still gets a truthful stale intent to real Runtime and verifies its real 409. These are conditional ownership boundaries, not fixes authorized or implemented here.
4. Do not overlap 1014 Session metadata or 1022 alignment. No H3 GO, no full/P1/P3/P4/browser/build/service retry in this slice.

## Commands and results

All testing used this exact read-only worktree and existing main-suite files. Scratch config/logs only were written outside it. The config keeps normal suite setup/plugin/aliases, uses read-only private Composition 0.0.14 exports, and sets cacheDir to `/tmp/w-7ba3d777ad/vite-cache`. Shared `node_modules` resolved to `/home/user/work/app/node_modules`; no shared files/caches were written. No test assertion, source, fixture, installed dependency, or generated file changed.

Exact test command (same command for the three attempts below):

```bash
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-7ba3d777ad/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts
```

- First attempt: exit 1, private runner-config startup error `__dirname is not defined`; no tests executed. Log `/tmp/w-7ba3d777ad/focused.log`.
- Second attempt: exit 1, three suites collected no tests because the private alias map's root entry preceded subpath entries and intercepted theme-api. Only the private config was corrected. Log `/tmp/w-7ba3d777ad/focused-fixed.log`.
- Final attempt: **exit 0; 3 files / 86 tests PASS; 11.89 seconds.** Log `/tmp/w-7ba3d777ad/focused-final.log`. The existing mounted dependent trim, serializer duration/source-preservation checks, stale-basis/source/head/invalid guards, and accepted/merged/conflict/invalid/restart/dependent unit coverage were not weakened. These mocked transport/unit results do not qualify real 409, lost ACK or restart in service28486.

Other exact checks:

```bash
git rev-parse HEAD HEAD^{tree}
git diff --exit-code 1117c15f7e37a087a1175ea0e923958ce8a4132d HEAD
git -C /home/user/work/wt/agt-pin-b8e50762 rev-parse HEAD HEAD^{tree}
git -C /home/user/work/wt/rt-pin-a5d42583 rev-parse HEAD HEAD^{tree}
sha256sum src/tools/video-editor/{hooks/useTimelineSave.test.tsx,hooks/useTimelineCommit.ts,lib/serialize.ts,lib/serialize.test.ts} tests/e2e/local/{three-products.p1-chain.spec.ts,support/astrid.ts}
git diff --check
git status --short
```

All exit 0; identities/hashes are recorded above, diff check clean, status empty. No new type/lint/full/live evidence claimed. Original service command/result is retained in the service summary; it was not rerun.
