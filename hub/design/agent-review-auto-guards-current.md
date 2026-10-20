# Agent automatic-placement guard review

2026-10-20. Reviewed `5c6467da34f53ce8d5111c0162eca5ff614380ed` against `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e`, PLAN, Agent AGENTS.md, orchestrator Agent INBOX 08:46, and `design/app-automatic-capture-contract-review.md`.

**Recommendation: APPROVE the bounded timing/lane/exclusive-owner correction in 5c6467da.** No remaining stale-position or occurrence-isolation blocker was reproduced in the requested branches. The answer to an unrestricted “EVERY builder read?” is still **no**: shared pool-promotion and legacy-group eligibility have pre-existing unrecorded reads, detailed below. Those belong to the explicitly separate pool/migration work; do not treat this approval as qualification of those behaviors or production automatic adoption.

**Runtime generation is pending. This is Agent-only source/conformance evidence, NOT actual paired qualification.** No Runtime process, acceptance transaction, generated artifact pair, task/attempt fence, App outbox, browser, or pixels were exercised. No full suite was requested or run. No product, test-suite, integration-worktree, dependency, or git-ref edits were made.

## Guard coverage and observed results

Resolution arithmetic still happens in the pure builder, outside `Recording`. However, the emitted birth re-reads its consumed state through the existing recorder on that same supplied bundle. Merely observing that the arithmetic is outside the recorder is not a counterexample: the returned commands contain authoritative original-value reads, and execution verifies them before running the handler. No additional recorder is needed.

| Read/branch | Authoritative guard and targeted evidence |
| --- | --- |
| Output fps | `native_occurrence_media_commands._owner` reads parent `config.output.fps` and child `output.fps` (lines 33–35). Independently changing either refuses across all eight image/video placement modes. |
| Occurrence identity, start, home lane, extent, activity/map | `_owner` reads occurrence/shot identity and `capture.MAP_FIELDS`, including `placement.start_ms`, `at_ms`, `track`, `placement.track`, `duration_ms`, mapping and activity. Origin, home-lane and duration changes refuse in the matrix. These were already guarded before this patch. |
| Anchor membership/absence and clip order | `_consume` always selects `collection.clips`, including when `consumed` is empty for saved fallback. `ctx.create` also selects the collection. Deletion, reordering, and inserting a previously absent named anchor refuse. Saved fallback does not discard the absence guard. |
| Anchor timing / inherited lane / lane-end / shot extent / occupied starts | `_consume` records whole rows for the anchor (completion anchor mode) or all clips (completion lane-end/shared). Existing suites cover anchor movement and inherited lane change. Scratch probes use actual intervening native `placement.move` commands and their records for the three numeric cases below. |
| Chosen track validity | `_clip` selects child tracks and reads the selected whole track (lines 120–126), checking active visual output status. Deleted, disabled, changed-kind and changed-role tracks refuse across the matrix. Saved nonhome image births use `occurrence.add-media` and receive the same checks. |
| Exclusive owner | `add_media` unconditionally calls `_exclusive` before any media branch (lines 129–133). `placement.create` also checks it. Sixteen image/video mode combinations reject retargeting via `selection_changed`; fresh builder and raw handler calls reject with `unsupported_ownership`. Covers home/nonhome images, all videos, completion anchor/fallback/lane-end, and shared append/explicit/inherited lane. |
| Public `consumed` args | IDs are membership-checked, values come from `ctx.read`, not caller-supplied snapshots. Omitting/replacing/adding IDs while retaining original capture claims refuses on the original basis; on a moved head, original reads refuse before handler execution. Raw commands captured on the original basis regenerate the same guards, which then refuse stale replay. No refreshed-guard bypass was reproduced. |

The guard matrix has 176 cases: image/video × eight modes × eleven changes (parent fps, child fps, origin, home, duration, track kind/role/disabled/deletion, anchor membership, clip order). Each first verifies identical-record replay on the unchanged basis. Capture explanations are never used as commit authority.

| Actual intervening native move | Before | Fresh result | Original command on changed head |
| --- | --- | --- | --- |
| Shared explicit request 390; move clip-a onto its previously selected start | Request 390 shifted to 391 | 392, skipping 390 and 391 | `dependency_changed`, image and video |
| Completion lane-end; move clip-b from global 13 s to 14 s | 450 | 480 | `dependency_changed`, image and video |
| Shared append; move overlay clip-c from global 9 s to 10 s | 510 | 540 | `dependency_changed`, image and video |

On exact 931d7ec5, the same six positive stale-conflict requirements fail because replay accepts. Among ten compatible retarget cases on that base, six fail because replay accepts (all videos and shared inherited-lane image), while four existing home-image controls pass. Current source passes these cases. Intervening native-move fixtures widen occ-a and move the sibling to 100 s **before capture** so the tests measure guards rather than unrelated occurrence-boundary refusal. Retarget and the general mutation matrix use explicit changed-head fixtures; they do not establish a live Runtime retarget acceptance path.

## Saved policy, duration and retry

Missing anchor plus saved `fallback_at=22.25` and `fallback_track='overlay'` authors global frame 667 on overlay, rather than recalculating lane end. A sibling timing change rebases with the same start. Present anchor plus `preferred_track='overlay'` wins over the separately saved picture fallback, at frame 330. Deleted saved track refuses `dependency_changed`; invalid saved time outside the occurrence refuses `occurrence_boundary`. Track validity changes after capture refuse through existing reads. These are visible refusals, not implicit moves to another lane or hidden re-evaluations. With no saved time, lane-end computation remains available and guarded.

An unchanged-basis replay is identical. A conflict is not authority to silently refresh the approved continuation: re-running the builder on a new head is a **new capture/re-evaluation**, to be retained and approved according to the requester policy. Existing docs saying “caller rebuilds” must not be interpreted as rewriting an in-flight request. Stripping all recorder claims and authoring a different explicit birth remains possible by design; it is not an exact retry of the captured request. No claim of server receipt/idempotency or restart proof is made here.

Completion image remains 5 s (even with a supplied duration); completion video defaults to 5 s with source window 0..5, not the verified full 6 s; explicit video duration 3 uses 0..3. Shared image/video remain 4 s. A verified 3 s video refuses `unsupported_timing` for default completion and shared placement; explicit completion duration 3 succeeds. This short-source refusal **already exists in 931d7ec5** and remains an observable difference from old App behavior, not a newly qualified preservation policy. Keep old positive behavior requirements and the short-video/default-style follow-up open; do not rewrite success requirements to permanent refusal. Parent births, append growth, pool/keepAsPooled and video unplace are not closed by this review.

## Nonblocking findings for this bounded patch

1. **P2: whole-row reads overconflict with unrelated clip fields.** In completion anchor/lane-end and shared append/explicit modes, an actual native `clip.set-params` of clip-a to `params.unrelated=1` leaves the new builder's full capture identical but original replay refuses `dependency_changed`. Changing only `volume` to 0.5 in a changed-head fixture does the same. This is safe refusal, not stale placement or data loss, but exceeds PLAN's “only real clashes” goal. Minimal safe follow-up: replace `_consume`'s `ctx.read(ref)` with field-path reads for the timing and lane inputs (including absent fields, `at_ms` fallback, `hold`/trim/speed precedence and validation); retain collection guards. Conservatively guarding those fields for every consumed clip works without changing the public arg or adding a recorder. Add a positive unrelated-field rebase test while retaining all stale-conflict cases. Target-track whole-row reads are similarly conservative.

2. **Pre-existing pool read remains outside the birth guard (separate pool item).** `native_auto_placement.py:196` reads pool membership to decide whether to emit `shot.pool remove`. Concrete counterexample: start with the reserved asset already bound to the exact registry pin, absent from pool and clips; capture shared append (one birth command); concurrently execute ordinary `shot.pool add` for that asset. Original birth replay accepts and leaves the asset **both pooled and placed**. Fresh capture emits birth plus removal (`promoted=true`). The diagnostic passes on both base and candidate, so this is not introduced by 5c6467da. Minimal correction in the pool cohort is a recorded pool read, including absence, using the existing recorder in shared placement's birth path, with matching browser goldens. This blocks blanket pool-promotion qualification, not the explicitly bounded timing/owner correction.

3. **Pre-existing legacy eligibility read remains outside guards.** `native_auto_placement.py:158` checks `parent.config.pinnedShotGroups` only in the builder. Capturing on no groups, then changing that field to a nonempty legacy group permits original replay; a fresh builder refuses `migration_needed`. Same result on base and candidate. This is a changed-head fixture diagnostic; no supported concurrent migration/restore sequence or actual accepted Runtime legacy head was established, so it is not elevated to a new production blocker here. Preserve the migration hold; guard that precondition in the existing recorder when qualifying mixed legacy/canonical flows. A different recorder or whole-document guard is unnecessary.

Documentation follow-up: the opening completion signature omits the new saved arguments and “New clip goes on the occurrence lane” is stale when a saved lane is used. The 08:46 contract itself need not change.

## Exact commands and results

Paths abbreviated below only for readability; they expand to the actual commands run:

```sh
REVIEW=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-auto-guards
SOURCE=/home/user/work/wt/agt-review-auto-guards
PYTHON=/home/user/work/venv-agent/bin/python
```

From `$SOURCE`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$SOURCE $PYTHON -m pytest -q -p no:cacheprovider --basetemp=$REVIEW/pytest-targeted tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
```

**173 passed in 10.06 s; exit 0**, `targeted.log`. Includes the unchanged main-suite portable goldens, exact inverse/redo and detached-provider tests. Their existing `runtime_abi` fixture supplies detached ABI exceptions/metadata; it is not a real Runtime pair.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$SOURCE $PYTHON -m pytest -q -c /dev/null -p no:cacheprovider $REVIEW/scratch/test_review.py
```

**223 passed in 12.06 s; exit 0**, `probes.log`, before adding the independent pool diagnostic and direct raw-handler retarget assertions. No original requirement test was replaced. Two supplementary targeted runs on the final probe:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$SOURCE $PYTHON -m pytest -q -c /dev/null -p no:cacheprovider $REVIEW/scratch/test_review.py -k pool_precondition
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$SOURCE $PYTHON -m pytest -q -c /dev/null -p no:cacheprovider $REVIEW/scratch/test_review.py -k retarget
```

Pool: **1 passed, 223 deselected in 2.00 s; exit 0**, `pool-probe.log`. Retarget: **16 passed, 208 deselected in 2.74 s; exit 0**, `handler-retarget.log`. The scratch diagnostic tests intentionally describe observed overconflicts/precondition gaps; their green status is not conformance approval of those behaviors.

Base comparison extracted only tracked `astrid`, `tests`, and `pyproject.toml` from 931d7ec5 using `git archive`/`git show`, without switching any worktree/ref. From `$REVIEW/scratch/base`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD $PYTHON -m pytest -q -c /dev/null -p no:cacheprovider ../test_review.py -k 'stale_native_move or (retarget and not anchor-overlay and not fallback)'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD $PYTHON -m pytest -q -c /dev/null -p no:cacheprovider ../test_review.py -k precondition_diagnostic
```

**12 failed, 4 passed, 208 deselected in 3.05 s; exit 1**, `baseline-focused.log`: all twelve failures are the intended positive `DID NOT RAISE` regressions described above. **2 passed, 222 deselected in 2.19 s; exit 0**, `baseline-preconditions.log`, confirms both precondition gaps predate this patch. Development-only broad baseline run included six unsupported-new-keyword failures and was narrowed; an initial extraction omitted `pyproject.toml`, causing one collection error before correction. Neither is counted as defect evidence. Scratch pytest runs report one harmless unregistered `integration` marker warning because `-c /dev/null` avoids loading repo-wide configuration/conftest.

`git diff --check 931d7ec5 5c6467da` and final `git diff --check`: **exit 0**. `git status --short`: **empty**. Shared dependencies remained read-only. Extracted baseline source and pytest temp output are removed after review; the small repro and logs remain under this worker's scratch/report directory.

## Handoff

No execution blocker for this read-only task. Recommend accepting the bounded source fix, tracking the minimal field-read refinement and existing pool/migration gaps separately, and keeping production activation held for Runtime's normal regeneration/attempt-fence qualification and App's original-approval/outbox journey. No commit is required: repository tree is unchanged; worker `commit-msg` is empty. No merge, push or integration edit was performed.
