# Media-only completion fence: normal API reachability

Result: **DEN for the proposed same-attempt invalidation counterexample on frozen Runtime `8609333456b9537339ee1a5dfc7ffd9609242de8`.** No tested normal transition leaves a completed managed-media task attached to the same attempt while changing its executor, lease fence or task epoch. Cancellation after completion is a no-op. Retry invalidates the selection immediately, before reclaim. Restart advances the global boot epoch while preserving completed historical task/attempt identity; the original media remains eligible correctly.

Recommend that Runtime **ACK the existing `MediaReads.selected` verifier and its acceptance-time revalidation as sufficient for this media-only completion authority**, before the requester adapter is unblocked. No new guard, App epoch/provenance field, proposal pin or Runtime product fix is justified by this experiment. This report does not itself activate the adapter or qualify full native commit acceptance.

## Frozen sources and retained experiment

All artifacts are under:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-media-completion-fence-reachability
```

| Input | Exact source / use |
| --- | --- |
| Runtime | `8609333456b9537339ee1a5dfc7ffd9609242de8`, archived from `/home/user/banodoco/banodoco-workspace-runtime` into `$W/sources/runtime`; every Runtime import resolves to that archive. No newer mutable integration source was substituted. |
| Native placement | Agent `80f5149631bb2b08c0569a2a53192e14442991e7`, archived `astrid/`, the native completion/shared fixture modules and fixture directory, and `pyproject.toml` into `$W/sources`. Read the actual native builder and private conformance fixtures. |
| Producer contract | Agent `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00:astrid/sdk/timeline/producer.py`, retained as `$W/sources/producer-0a0ac7b.py`; Runtime's producer verifier and private producer fixtures come from the frozen Runtime archive. |
| Original native bundle fixture | Private copy `$W/native-vectors.json`, from the corrected-port worker's export of Agent `80f5149`; SHA-256 `ad0a0d423d513cf22d201d450ebb9aaeb5402f7a2a397b5613a832271bb7f8ae`. This bundle is trusted fixture data, not a newly authenticated Runtime timeline basis. |
| Executable probe | `$W/test_reachability.py`; real `RealmStore.initialize`, `RuntimeService` startup admission, public create/register/claim/settle/cancel/retry/read methods, private per-test DB/CAS. The existing Runtime publication fixture supplies admission and settlement, without monkeypatching authority or seeding SQL. |

Sources were extracted using `git archive` / `git show`, then made non-writable. `$W/source-integrity.log` verifies all **407 Runtime and 1,377 Agent archived regular files** byte-equal to the original archives, plus the separate producer file. `PYTHONDONTWRITEBYTECODE=1` was used for every Python run. No shared venv, dependency, runtime, cache or other worker source was written.

The fixture publishes both a real PNG and a real two-second MP4 through `generation.publish_v1`, with declared intrinsic metadata, real CAS bytes, generated catalog variants and Runtime-authored output associations. Public five-field selections are captured only after successful completion. Each subsequent read checks both the public `get_project_verified_media` response and the actual `MediaReads.selected` result; they agree, retain the original pin, and do not write the DB. SQL in normal probes only inspects state. Two expiry tests replace the store clock to advance past the real lease deadline; no row is injected.

## Executed normal transitions

The final private probe run contains **27 non-corruption cases and 6 explicitly injected corruption cases**. Every normal authority case verifies both image and video outputs from the same real completed attempt. The two native cases separately exercise image/video semantics.

| Transition | Observed result |
| --- | --- |
| Complete, canonical cancel; complete, legacy cancel | Task and attempt rows remain byte-for-byte equal to their completed snapshots. Original selections still verify. Canonical cancel may record its normal command receipt; it does not revoke completed media. |
| Complete, cancel run / retry run | Both refuse the completed run with `ConflictError`; original selections remain eligible. |
| Complete, claim by same executor or a new registered executor | No task claimed. Completed task/attempt identity unchanged. |
| Complete, re-register executor with no capabilities | Executor registration changes; completed task/attempt rows and media eligibility do not. The request includes the required current registration epoch. |
| Complete, heartbeat / fail / prepare reboot / new settlement key | `LeaseError`; settled attempt cannot become live again. Changing the supplied heartbeat fence also refuses. |
| Complete, exact original settlement replay | Returns the original receipt without changing task/attempt identity. |
| Complete, advance past original attempt deadline, claim | No reclaim. Completed task has no lease deadline; its settled historical attempt remains unchanged. |
| Complete, close and reopen `RuntimeService` | Global epoch increases, but completed task/attempt rows and original selections are unchanged. Also passes with normal `runtime_epoch_floor=100` startup, without bypassing admission. |
| Cancel task / cancel run while running, then settle old attempt | Old settlement refuses; no managed outputs or catalog variants are published. |
| Restart while running, then settle old attempt | Old epoch settlement refuses; no outputs/variants are published. |
| Let running lease expire through normal claim/reaper, then settle old attempt | Old settlement refuses; no outputs/variants are published. |
| Complete, retry task | Task becomes queued with null current attempt, executor and result. Old image/video selections immediately refuse with `ConflictError`. |
| Then reclaim | A different attempt ID and a larger fence are allocated. Old selections still refuse. |
| Then replay the original settlement ACK | Original receipt is returned, while current task remains running on the new attempt. Old selections still refuse. Replay does not restore obsolete authority. |
| Complete, lifecycle `pin` / `promote` | Normal versioned lifecycle mutations succeed; original selection digests refuse. |
| Complete, lifecycle `expire` / `reclaim` | Durable available outputs cannot take these transitions; calls refuse and original selections remain eligible. |
| Feed public verified-media response into native completion capture and execute | Pure native image `placement.create` and video `occurrence.add-media` both succeed over the original private bundle fixture, using the actual Runtime selection and metadata. No `producer.guard` or proposal is supplied; no Runtime timeline publication is performed. |

**Separate Runtime limitation found:** after the completed `generation.publish_v1` task is retried and reclaimed, attempting its second publication raises `sqlite3.IntegrityError: UNIQUE constraint failed: generations.id` at `store.py:4781`. Generation IDs derive from task ID + group key, and publication uses `INSERT`. The probe reproduces the error through `settle_attempt`, verifies DB rollback, task still running and original selections still refused. It does **not** claim to have successfully completed this second publication. No SQL repair was used to manufacture that state. This is a retry/publication follow-up for Runtime, not an accepted media-fence counterexample. No passing behavior test was changed to expect refusal.

## Why the omitted equality is not normally reachable here

Code references below are relative to `$W/sources/runtime`, at the frozen SHA.

1. `service.py:6552` (`settle_attempt`) validates the current epoch, live unsettled attempt, running task, current attempt ID, lease token and fence before publication. `store.py:5540` atomically sets completed status, stores the settled result, marks the attempt settled and releases reservations. It preserves task executor/fence/epoch and current attempt ID.
2. `store.py:5748` (`cancel_task`) returns completed tasks unchanged. Run cancellation checks run state (`5820`) and skips terminal children (`5826`). `store.py:3414` / `3431` likewise exclude completed children from cancellation/orphan-delegation containment.
3. `service.py:6181` (`retry_task`) is the ordinary post-completion supersession path. Its transaction clears task status/result/attempt/executor (`6214`) before another claim. `claim_next` selects only queued tasks (`6430` vicinity); `_claim_task` refuses a completed task (`store.py:3778`) and allocates a larger fence only while claiming queued work (`3849`). A new canonical claim inserts a new attempt and updates task attempt ID (`service.py:6511`).
4. Restart recovery selects only running/cancel-requested tasks (`store.py:1176`); lease reaping likewise selects those statuses with a non-null task deadline (`3476`). Advancing the global epoch does not rewrite completed task/attempt epoch fields. Requiring completed media to equal the **new global boot epoch** would reject valid historical media after restart; that is a different condition from comparing the task's historical epoch with its settled attempt.
5. `_validate_attempt_lease` (`service.py:7537`) rejects settled attempts. New heartbeat/failure/checkpoint/reboot operations cannot mutate their authority. Authorized checkpoint resume claims queued/recoverable work and inserts a new attempt (`7819`); placement recovery requires failed/cancelled task state (`5930`). The import claim path also goes through `_claim_task` (`4143`). There is no reviewed normal setter that changes only a completed task's executor/fence/epoch while preserving its same completed current attempt.

`$W/task-write-sites.txt` retains the search of all Runtime `UPDATE tasks SET` / `UPDATE attempts SET` sites used to check this argument, including recovery, import, delegated containment and spec-retirement paths. Attempt executor/fence/epoch have no update site in the frozen product; claims insert them. This is a source-backed invariant for the inspected lifecycle, not an exhaustive state-machine model check or an HTTP concurrency stress test.

## Existing guard coverage and its limits

| Authority condition | Existing implementation / evidence |
| --- | --- |
| Exact request realm/project and five-field media identity | `service.py:2489` / `2500` / `2508`; `MediaReads.selected`, `timeline_commit_port.py:803`. Unchanged targeted tests cover foreign scope, missing/extra/malformed fields, object and digest mismatch and authorization recheck. |
| Completed generation, managed object, intrinsic metadata | `_selected_project_media`, `timeline_commit_port.py:709`; joins generation/variant/object/project ownership and validates metadata/duration. Real image/video positive probes and unchanged negative metadata tests. |
| Unique eligible durable association and exact registered variant | `_output_selection_binding`, `timeline_commit_port.py:653`; verifies project, lifecycle, variant binding, object identity and ambiguity. Version/catalog changes are caught without selecting a newer variant. |
| Completed task + current association attempt + settled attempt | `timeline_commit_port.py:677`–`707`; requires exact completed settlement, matching output tuple/digest/size/type/role, current task attempt ID, matching attempt task, settled state and nonempty attempt lease ID. Normal retry/reclaim and pre-completion invalidation probes demonstrate refusal. |
| Association provenance equals historical attempt | Same block compares task/attempt/capability/executor/fence/epoch provenance. Injecting only an attempt field rejects selection. |
| Task executor/fence/epoch equals historical attempt | **Not directly checked by `MediaReads.selected`.** Source invariant above is the normal-API reason those columns agree at completion and stay agreed until current-attempt eligibility is removed. |
| Revalidation after capture | `RequestCommitPort.selected_media` (`timeline_commit_port.py:264`) privately captures the selection; `validate` (`387`–`401`) re-runs `MediaReads.selected`. `TimelineCommitStore.accept` (`timeline_commit_store.py:672`) invokes validation under the store mutex and `BEGIN IMMEDIATE` transaction (`store.py:806`). Therefore a normal retry/lifecycle mutation before acceptance is re-read; a mutation after acceptance does not retroactively invalidate that accepted timeline revision. This conclusion is code evidence, not a newly executed native commit race. |

Producer guard is a different contract. Agent's frozen `build_producer_batch` / `capture_producer` requires the original proposal batch. Runtime `timeline_commit_producer.py:223`–`274` requires admitted `authoring_proposal`, actual settled JSON bytes, exact target, commands, rationale and producer pin. Its `_current_attempt` (`119`) checks task/attempt equality for executor/fence/epoch (also for selected continuation children). Private producer fixtures explicitly distinguish completed cancellation no-op from retry supersession (`tests/test_timeline_producer_guards.py:320`–`361`). These checks cannot be borrowed by inventing a media task proposal or appending arbitrary births.

**Injected tests are separate:** three cases directly update only `tasks.executor_id`, `tasks.lease_fence` or `tasks.runtime_epoch` while leaving completed/current-attempt/result/association rows intact. Media verification still succeeds, while the actual producer `_current_attempt` helper returns false. Three other cases update only the corresponding attempt column; media verification refuses because provenance no longer matches. These demonstrate the exact defense-in-depth difference. They are deliberately corrupted private DBs, not normal API transitions, and establish no accepted normal race.

The media verifier also supports legacy catalog entries without managed output associations. This experiment's completion-authority conclusion concerns **Runtime-bound managed task outputs**, not a new blanket guarantee for every historical/imported catalog row.

## Exact tests and results

Run from `$W`, using only the read-only Runtime dependency venv. No full suite, server, localhost, HTTP socket, browser, build, install or tsc was run or requested.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD/sources/runtime:$PWD/sources/runtime/tests:$PWD/sources /home/user/work/venv-runtime/bin/python -m pytest -q -c /dev/null -p no:cacheprovider --basetemp=$PWD/tmp-probe test_reachability.py > probe-final.log 2>&1
```

**PASS: 33 passed in 6.81s, exit 0**, `$W/probe-final.log`. These are worker-only reachability probes, not shipped product regression tests.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD/sources/runtime:$PWD/sources/runtime/tests /home/user/work/venv-runtime/bin/python -m pytest -q -c sources/runtime/pyproject.toml -p no:cacheprovider --basetemp=$PWD/tmp-main sources/runtime/tests/test_generation_publish_v1_settlement.py sources/runtime/tests/test_timeline_media_selection.py sources/runtime/tests/test_timeline_verified_media.py > targeted-main.log 2>&1
```

**PASS: 50 passed in 5.49s, exit 0**, `$W/targeted-main.log`. These are the **unchanged main-suite tests in the frozen source**, including public verification authorization/metadata checks and publication rollback/idempotency. Existing media acceptance tests use the repository's `PreparedProvider`; their acceptance-race cases inject SQL. They are not evidence of full native Agent acceptance or a normal task-fence race. Route handler tests here are in-process objects; none opens a socket.

The initial exploratory run (`probe-first.log`) had **27 passed / 2 failed**: re-registration omitted its required epoch, and the attempted second publication hit the real duplicate-generation limitation. The registration request was corrected. The unachieved second-publication hypothesis was replaced with an explicit reproduction of the observed product error and rollback, as described above; no existing passing behavior expectation was weakened. `probe-second.log` passed 33/33; the final run tightened negative probes to require `ConflictError` specifically.

`git -C /home/user/work/wt/app-m2-media-completion-fence-reachability diff --check` passes; the assigned App worktree is clean at `7bb885b638838588a0dff81b64b7c34960ac07f3`. No Runtime/Agent/App product or repository test changes, commits, branch operations or integration-worktree edits were made. Temporary probe DBs were removed after results were retained; archives, reproducible probes, original bundle fixture and logs remain in the worker folder.

## Recommendation and open qualification

Runtime should ACK that, for bound completed image/video outputs, existing selected-media capture plus transaction-time revalidation supplies the required historical task/attempt completion authority. Do not demand a new App-generated epoch, provenance or digest, and do not fabricate `producer.guard`. An extra task/attempt equality check could be defense in depth against corruption, but this experiment supplies no reachable counterexample requiring that product change.

After that ACK, the adapter owner can remove the specific unconditional missing-media-guard refusal in its own authorized unit and retain the original saved basis, approval, five-field selection and birth IDs through the existing requester/outbox. Same-host verified-media forwarding, approval codec/original read binding, the normal current registry/release tuple and full successful native placement/lost-ACK/restart/undo qualification remain open as identified in the adapter-stage report. No startup bypass or widened provider authority was used here. Full native commit acceptance was optional and was not attempted; the native tests prove pure capture/execution only. Runtime should separately triage completed `generation.publish_v1` retry/republication failure. Re-run these probes against any later source before citing this result for that tuple.
