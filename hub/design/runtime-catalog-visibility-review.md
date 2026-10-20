# BLOCK — Runtime catalog timeline visibility review

Date: 2026-10-20 UTC  
Candidate: `ca1f1b6df9a4df9a7febd03c4d3b3f9cd2260b99` versus `2ef92e46535e5dddf9db62342824986d9de5b9ec`  
Scope: independent data-safety and authorized assertion-conversion review.

## Decision

**BLOCK.** Historical-version refusal is safe for a newly submitted request,
but an explicit `version` equal to the current catalog version can replay an
old legacy `timeline.recover` receipt. This violates the settled boundary that
legacy historical recover receipts are not replayed and can return stale legacy
flat-film data as if it were the current visibility result.

## Concrete finding

`runtime_protocol/service.py:3904-3938` only performs the receipt/event
provenance check when `target is not None and target != current["version"]`.
For `target == current["version"]`, it falls through to the ordinary
`_command_replay` at lines 3933-3936.

I reproduced this in a private temporary realm (no worktree or product-file
changes): create a project/timeline, archive it, insert a receipt matching the
old implementation's request hash with a `timeline.recovered` event carrying
`target_version`, then retry `recover_timeline` with that current target. The
call returned the legacy receipt (`data.archived == False`) instead of the
required visible 410 refusal. The old implementation's event shape is
confirmed at `/home/user/banodoco/banodoco-workspace-runtime/runtime_protocol/service.py:4435`.

## Minimal fix

Before the normal `_command_replay` branch, inspect an exact existing
`timeline.recover` receipt and its event. Replay only a receipt positively
identified as produced by the new visibility-only implementation (the
`timeline.recovered` event has no `target_version`). Refuse legacy or
unidentifiable receipts with the existing 410 `timeline_restore_required`
error and `timeline.restore` replacement details. Preserve exact replay for
new visibility-only receipts, including a current-target retry after a later
catalog-version change; keep absent/current requests visibility-only.

## Verified properties

- The HTTP route remains the existing client shape and requires authenticated
  `projects:write` plus an idempotency key (`runtime_protocol/server.py:641-646`).
  The service derives the project from the timeline row, applies
  `expected_version`, and records the mutation through the existing durable
  transaction, event, and project-scoped receipt paths.
- The patch changes only `runtime_protocol/service.py` and two lifecycle test
  files. The archive/recover implementation updates only `timelines`, appends
  the existing timeline event, and records the existing receipt. It does not
  call timeline-revision snapshot writers, legacy-flat recovery, canonical
  closure/document/CAS writers, or film commit-history writers.
- For a newly submitted non-current target, the implementation reads the
  timeline and any exact receipt/event evidence, then raises 410 before any
  write or ordinary replay. The new service and HTTP refusal assertions pass.
- Missing/current visibility semantics are live-tested. The live test checks
  archive/unarchive state, shots/references, canonical head/publication,
  unchanged closure, unchanged `timeline_commit_history`, and exact retries.
- The real Agent-provider canonical restore positives remain named and ran:
  `test_service_actual_bootstrap_command_restore_and_exact_retries` and
  `test_http_actual_create_command_restore_rename_and_ordinary_artifact_metadata`.
  Their `restore_provider` fixture imports `astrid.sdk.timeline.commit` from
  `/home/user/work/agent` and asserts that import is from that checkout.
- No new xfail was added by this patch. The pre-existing broad retirement
  xfail was narrowed to the still-retired direct timeline/shot/reference
  writers; the new visibility and refusal tests are live.

## Test evidence

- Central final `restore-integration` run (with actual Agent checkout):
  `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_runtime_domains.py tests/test_timeline_legacy_authority.py`
  — **59 passed, 3 xfailed** in 54.03s.
- Local collection audit:
  `ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest --collect-only -q -p no:cacheprovider tests/test_runtime_domains.py tests/test_timeline_legacy_authority.py`
  — **62 tests collected**.
- Local marker audit with `-m integration` — **0 selected, 62 deselected**.
  The final 59-pass run used the `restore-integration` command without
  `-m integration`; no marked integration tests are claimed as executed.
- `git diff --check` — **passed**.
- No full suite was run or requested, per task instructions.

## Required next step

Apply the minimal receipt-provenance guard above, add one focused regression
for a legacy receipt whose target equals the current catalog version, rerun
the two named targeted files through the actual-provider `restore-integration`
lane, and repeat this review.
