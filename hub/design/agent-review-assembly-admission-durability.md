# Changes requested — assembler admission durability

Independent read-only review, 2026-10-20. **One P2 correction is required before composition: request-kind dispatch is not strict.** The normal assembler admission durability path is otherwise supported by source inspection, independent local tests, reproduced private artifacts, and the inspected real-HTTP central evidence. No integration activation is approved by this report.

## Exact source

- Reviewed branch `tl/agt-m2-assembly-admission-durable-flight`, commit **`ed39c027f9f21b824c763610f18343b2bf0d682e`**, tree **`a0650c21b268f879969a9420bdb2921e4008289b`**.
- Already-reviewed base `32d6de6a8a50f05032a9b1f110ff1ac5a8975f4f`, tree `4c000d64c9048910889266f00fd4036a47ffebd3`.
- Assigned checkout/integration observed at `4ef1391c2c104d5d11b3a27265035c51be296045`, tree `afb2ed8506a99a088d7be3dbadaf593338d2fb5a`. It was not modified. Tests ran archived reviewed source, not this different revision.
- Product delta **+78/-16**: only `astrid/sdk/timeline/assembly.py` and `sync.py`. Three test files also change; total five files, +338/-31. `outbox.py`, wire contracts, generated clients, public locks/schema/artifacts, pack declaration and STITCH mapping are unchanged against the base.
- SHA256: `assembly.py` `e5faf15b139c4da8463da3b01dedd6c746f9d8ef41ba8927eddec30cef7ef346`; `sync.py` `6c82655db96e8ff6d15fb08eacb2263683af2f55664acef79992db3f79e79781`; unchanged `outbox.py` `dfb1e46123be49539cf053a9e49060d9c8ad1ec73f15393a3a1d3427dac95a99`.

Read PLAN.md first, then the absolute handoff/report, complete committed delta, relevant outbox/capture/transport/generated serializer, current integration stage guards, private cohort helper/schema and Runtime admission/authority/replay code. No decision was changed or relitigated.

## P2: reject every unrecognized flight kind before dispatch or mutation

Candidate `sync.py:365` only excludes `kind == 'assembly-admission'` from `flush`. `_flight_body` (`:431`) never checks the discriminator. `_stage` (`:319`) similarly treats every other tag as a commit prefix. Thus any explicitly tagged but unrecognized flight with otherwise valid commit fields is replayed as a commit and its outbox state is acknowledged/cleared. Untagged legacy commits should be supported; arbitrary tags should not silently receive that interpretation.

Independent probe: create a valid lost-ACK commit flight, add `kind: null`, `kind: 'assembly-admission-v2'`, or `kind: 'commit'`, reopen and flush. All three cases send a second commit and clear/update the outbox. Observed `(refused, transport_calls, file_unchanged)` is **`(False, 2, False)`**, whereas strict dispatch requires `(True, 1, True)`. These are fake generated-transport probes with the real command engine, not HTTP/security-exploit claims. A genuine admission-shaped unknown flight currently fails incidental commit-shape validation, so this finding does **not** demonstrate duplicate assembler tasks or an actor bypass.

Recommended narrow fix: validate the local discriminator wherever state is admitted for processing, before any local mutation/network dispatch. Only an absent tag may mean the legacy commit format; the one recognized admission tag selects admission behavior. Unknown/malformed tags must raise `TimelineEditError` and retain the file. Keep legacy unfenced/untagged commit recovery. No new wire DTO, journal, schema, framework or accepted-history cache is needed. Add regressions to the main test suites; the review-only probe is retained beside this report.

## Durability and authority findings

1. **One crash-safe outbox.** Fresh admission captures the original base, parent closure, exact ordered association/object/integer-version selectors, media/verified-media rows, replacement membership and rationale. Normal `prepare_admission` completes arguments once. The seven-field projection matches the actual generated createTask serializer for this bounded assembler request, including field order, defaults, escaped Unicode and numeric JSON representations. The existing writer fsyncs the temporary file, atomically replaces it, then fsyncs the directory before dispatch. Independent probes confirm this order and that either file or directory fsync failure prevents POST. Directory-fsync failure after replace leaves a replayable original flight.
2. **Exact recovery.** Saved request body/key are reused through normal `dispatch_admission`, with current credentials; retry does not recapture, prepare again, open a current composition, read history/head, or fetch current association/media inputs. Scope-only resolution still performs normal metadata reads. Changed key/digest/child/version/order/replacement/rationale and foreign realm/actor/project/timeline refuse while preserving the original flight. No client credential/header is persisted. Realm/actor scope values identify ownership, not authentication authority.
3. **Task ACK is not timeline publication.** Matching ACK cleanup removes only that admission flight and preserves original session base plus newer pending commands. Flush/undo refuse a recognized admission flight. The original admitted task may be queued and execute before ACK handling; this code neither delays dispatch nor assumes completion. Runtime replay can return the original admission snapshot/status; ordinary fresh getTask still reads current task state. No durable accepted-task cache or accepted timeline history is added. The new HTTP recovery tests leave the task queued; execution-before-ACK is source-inspected, not an independently executed new scenario.
4. **Normal Runtime authority remains intact.** HTTP admission still requires Runtime bearer `tasks:write` authority and ordinary project/body handling. Fresh same-actor credentials use that path; the outbox independently refuses a fully authenticated foreign actor. There is no credential-renewal bypass. The saved flight is not a tamper-proof authority store.
5. **Existing commit/requester semantics survive in the qualified cohort.** Untagged legacy commit exact retry, suffix retention, guarded inverse/undo and producer guard tests pass. Explicit STITCH aliases remain `travel_stitch` / `join_final_stitch` -> `rendering.render`. Native proposal acceptance is separate from admission durability.
6. **Compose narrow hunks.** Candidate `_stage` retains original sheet-base and producer-pending guards, but its source is older than current integration. Current `sync.py` has the additional `trim` method and checks sheet basis before producer-pending state. Do not replace the whole file. Preserve current methods and guards while porting the admission branch and prefix handling; rerun composed current-source tests. Current sync SHA256 observed: `99d37f6e80f81746948956a0fddca0d7ffa7e4f5a206e21a826c79c22933e1ad`.

## Independent commands and results

Set:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-assembly-admission-durability
```

`$W/source` was a `git archive ed39c027f9f21b824c763610f18343b2bf0d682e` extraction. No source edit or git mutation was made. In that directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/packs/rendering/test_runtime_stitch.py tests/packs/rendering/test_assemble_timeline.py
```

**133 passed in 22.68s; exit 0.** This independently reproduces the reported local cohort, including the original ACK-loss positive.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$W/probe-tmp $W/notes/test_review_durability.py
```

**3 failed, 8 passed in 1.99s; exit 1.** All failures are the strict-discriminator finding above. Passing probes cover actual outbox fsync/replace ordering, directory-fsync refusal/exact retry, legacy untagged and unfenced commit recovery plus undo, four foreign scopes and preservation of an unknown admission-shaped flight on flush/admit refusal. Final output is retained in `notes/adversarial.log`. A preliminary run with the same expectations also gave 3 failed/8 passed in 1.70s; the final assertion adds explicit observed call/file-state diagnostics.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py
```

**70 passed in 6.21s; exit 0.**

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/banodoco/banodoco-workspace-runtime /home/user/work/venv-agent/bin/python $W/notes/prepare_pair_review.py
```

**Exit 0.** Uses the unchanged candidate `prepare_pair` helper; only its git-archive repository locator is redirected to the assigned read-only repository because an extracted source archive has no `.git`. All sources, overlays and normal Python/TypeScript generators/checks remain exact. Output retained in `notes/pair-generation.log`.

Private tuple: Agent parent **`b5cfce5096f91f39bfb86d39823f97f0f59ce8a2`**, complete candidate overlays, Runtime **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`**, contract **`0.2.14`**. Whole candidate schema/full S2 floor: **53 definitions**, SHA256 **`fafb1985a326e6121aa8c9fb34bbda196edc3dfaf462352070372e631bea1f52`**. Normally generated whole manifest **`sha256:48c7b6533e2774a70e36517948a18fd5cee07f4d30e8f339776be9b3ec74ed4e`**; **all 75 artifact hashes** independently rechecked. Public S2/0.2.13 files are unchanged by this delta; no public release identity or activation is inferred from private generation.

In `$W/pair/agent`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_producer_guard.py tests/editing_conformance/test_producer_insertion.py
```

**81 passed in 14.62s; exit 0.** Existing producer requester/outbox/guard/rebase/inverse conformance; no HTTP claim for this local run.

In `$W/source`:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/assembly.py astrid/sdk/timeline/sync.py tests/sdk/test_timeline_assembly.py tests/packs/rendering/test_registered_assembler_admission.py tests/packs/rendering/test_registered_native_pair.py
```

**All checks passed; exit 0.** In the assigned git checkout, `git diff --check 32d6de6a ed39c027` also passes. No full/full* suite, browser, live socket or new central run was requested/executed by this reviewer. Shared dependencies/caches were not modified.

## Existing central HTTP evidence inspected, not rerun

[Summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-assembly-admission-durable-flight-identity-pin94114269-integration-1020131041-30429/summary) and [raw log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-assembly-admission-durable-flight-identity-pin94114269-integration-1020131041-30429/log.txt): exit 0, inner **15 passed / 2 unchanged held legacy xfailed**, outer **4 passed**. Service 235s. The exact recorded command is:

```sh
test "$(git -C /home/user/work/wt/rt-pin-94114269 rev-parse HEAD)" = 94114269d1ce23ab3224d7eca5a85138ce2b5fed && env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-94114269 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_identity.py tests/packs/rendering/test_registered_native_pair.py
```

Central tree **`4ffb60245f1dd3e723073da3e0a957ee6e09b3d9`** differs from the committed reviewed tree ONLY by the subsequently removed three-line local strict-xfail decorator. Product and HTTP test bytes are identical. Verified directly with `git diff 4ffb60245f1dd3e723073da3e0a957ee6e09b3d9 ed39c027`. The retry expectation remains; the marker changed only after the central pass.

The wrapper uses the exact private native tuple above, not the outer identity controls' Runtime pin. I inspected the actual test logic: it intercepts the real Runtime HTTP handler's deferred send, compares `_prefetched_body` with the already-persisted outbox body and header key, then drops the ACK after successful durable acceptance. It does not mock createTask. Both lost ACK and ACK-before-cleanup failure run with distinct/duplicate CAS. It advances accepted head to C and association lifecycle to V2, stops/recreates the daemon on the same realm/port with a changed instance ID, opens a fresh credential/client/session, forbids recapture/preparation/media reads, and compares the two observed HTTP bodies byte-for-byte. It checks the original task ID/receipt, unchanged stored task/spec, exactly three total tasks (two children, one assembler), unchanged history and preserved pending suffix. Restart here is persistent daemon recreation and requester reopening; no separate killed requester subprocess or power-loss test is claimed.

The other inner cases include unchanged native producer/requester positives and two existing regular commit HTTP lost-ACK/restart/suffix/inverse journeys. The unrelated exploratory archived M1 visualize call's missing `create_timeline_view(..., idempotency_key=...)` remains a reported failure, not accepted green evidence. No passing behavior test was weakened in this delta.

## Disposition and next steps

Review is complete; **not blocked**. Ask the implementation owner for the narrow strict-kind correction and suite regression, then compose only the reviewed hunks into current source and requalify the resulting tuple. The requested correction follows the brief; it requires no PLAN change. Public native activation, renderer/legacy completion restoration, D13 deletion, historical render, decoded-film/pixel/audio and macOS remain held/unverified. Existing video-labelled byte fixtures are not film/render proof.

No source/git/shared-environment mutation occurred. Disposable archives, generated private pair and probe temporary files were removed after recording evidence. Reports, review scripts and logs remain in the named shared worker/design paths; commit message and DONE are supplied for the harness.
