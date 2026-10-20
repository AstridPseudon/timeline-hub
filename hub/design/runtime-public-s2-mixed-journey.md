# Runtime public S2 mixed CLI journey

Worker: `rt-m2-public-s2-mixed-cli-journey`, 2026-10-20.

Outcome: **strong failing acceptance case retained; mixed journey not qualified**.
The real current CLI refuses capture on the retained music film before POST:
`timeline_edit_error: clip.trim applies to media clips`. The original Runtime
restart/exact-retry control passes on the same central run. This does not show
that trim fails on supported literal-media input; it identifies the missing
path from this historical film to that supported input.

## Change

Only `tests/test_timeline_public_s2_mixed_cli_journey.py` is added to Runtime.
It reuses the existing `music-documents` duplicate, `Editing`, readback/store
checks, and real `_start_door` startup. There are no new fixture archives,
Agent/App product edits, schema overlays, provider substitutes, positive SQL
history writes, renderer calls, new CLI APIs or flags, installs, or public pin
changes. `ASTRID_RUNTIME_DATA_ROOT` is the existing M1 outbox isolation setting.

The acceptance test retains the requested sequence: ordinary CLI trim at H0;
pause the actual prefetched HTTP POST outside the SQLite lock; commit a native
Python track label under a separate authenticated actor; release stale trim;
drop its durable ACK at the existing `RuntimeHandler._send` seam; restart;
repeat the same ordinary CLI invocation; compare original outbox path/body/key
and receipt, unchanged store/history, and forbid provider execution on retry;
undo through CLI/Runtime; compare the whole labelled closure, opaque rows and
media pins; identify accepted and undo revisions through show/layers/native
inputs visualize, including the accepted revision after undo advances HEAD.

Renderer tripwires follow the public M1 policy: pure readable timing helpers
under `packs.rendering` may load, while scene/evaluator imports and Runtime
scene evaluation remain unavailable. The stricter server-only integration
fixture blocks the public read helper itself and cannot be reused unchanged.

## Exact observed gap

The retained `music-bed` row has `clipType: audio`. Its registry asset has an
object pin and `type: audio`, but no authored duration. Current Agent native
`_trim_commands.py:46` accepts only absent/`media` clip type; line 65 also
requires a positive authored registry duration. `cli_native.commit_trim`
surfaces the native error for the explicit `parent/clip:music-bed` identity.

The final run opened real owner/peer HTTP SDK connections, verified retained
history and full closure, and captured the native label command. CLI then
returned exit 1 with `ok: false`, `receipt: null`, and the error above. The
failure assertion verifies an unchanged complete SQLite dump and no outbox
flight. **No trim POST was sent.** The label acceptance, pause/rebase, lost trim
ACK/recovery, trim inverse, and public revision views were not reached.

The historical audio row and missing source duration are not repaired in test
setup. That would need a supported guarded authoring/migration path or a real
captured supported film, rather than weakening trim or inventing accepted
history. No decision in PLAN.md was overridden.

## Sources and evidence

Runtime base: `129493b2aff614560d9b7ac2577957e799cf30ec`, base tree
`330ea3969cb9cce77271404f31793c21abd5993f`. Final central source tree:
`e58385c0731795b20b40d6a7ae26591564c3811e`.

Agent recorded by the central runner: `ce363f6d6d60e504dbd4d79803c2d6299f648ade`,
tree `78af007de1d7c5a59f86fffacd9823de355cd260`. Actual normal013 lock:
Runtime producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, contract/client
`0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.

Agent HEAD was subsequently observed at
`4ef1391c2c104d5d11b3a27265035c51be296045`, tree
`afb2ed8506a99a088d7be3dbadaf593338d2fb5a`. Its only change from the recorded
source is the verified-source host extraction (three files); timeline SDK,
CLI, remote/client, generated client and normal013 lock have no diff. The
central service snapshots Runtime, not the external Agent checkout, so this
is not a claim of a frozen cross-repo tree throughout execution. The refusing
trim source is byte-identical at both Agent heads.

Exact final submission and wait commands:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-test" rt-m2-public-s2-mixed-cli-journey capture-legacy-integration --files 'tests/test_timeline_public_s2_mixed_cli_journey.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider'
"$ORCH/bin/wait-test" rt-m2-public-s2-mixed-cli-journey-capture-legacy-integration-1020131143-26042 1
```

Actual central command, from its Runtime snapshot:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_public_s2_mixed_cli_journey.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
```

Result: **1 failed, 1 passed in 7.26s**, exit 1. The named suite's historical
`capture-legacy-integration` name does not enable a legacy or overlay path;
its complete command is reproduced above. `git diff --check` and final module
AST parsing pass. No full, browser, renderer, App Gate 5, all-writer or delivery
qualification was requested or claimed.

Logs and complete setup-attempt accounting:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-public-s2-mixed-cli-journey/DetailedReport.md`.

## Owner handoff

Agent owns supported capture/authoring for the historical audio/media shape
and trustworthy duration. Runtime owns this journey. Resolve that prerequisite
or provide an appropriate provenance-preserving captured literal-media film,
then rerun this exact module and control. Keep the acceptance expectation and
native guards. The red test is an explicitly authorized gap deliverable; it
must not be reported as a completed mixed-editing qualification.
