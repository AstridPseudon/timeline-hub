# D09 source-bound coverage adapter: exact missing carrier

**BLOCKED at the existing caller boundary; no product patch proposed.**

Branch: `tl/vw-m3-d09-bound-coverage-adapter-1306`.
Base/unchanged HEAD: `a086cc6db7928dc4a3516d304dd9a472b050f1cf`.
Flatpatch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-bound-coverage-adapter-1306.flat.patch` (0 bytes, deliberately empty).
Worktree: `/home/user/work/wt/vw-m3-d09-bound-coverage-adapter-1306`.

Read PLAN.md first and the independent `handoff-vw-m3-d09-onscreen-cut-review-1258-REPORT.md`; used rejected `a5cc85cc7` only as a read-only donor/control. No checkout, commit, merge, branch/ref mutation, push, or integration-worktree write occurred.

## Exact missing carrier

`astrid/sdk/timeline/check.py:93–119` reconstructs tracks and visual clips and calls:

```python
onscreen.coverage({"tracks": tracks, "clips": clips}, self.fps, canvas, elements,
                  start_frame=0, end_frame=end_frame)
```

That dictionary contains neither the retained timeline/registry paths nor the verified-source attribute, prepared Root props/theme/asset registry, or compiled occurrence/address identity. The existing `coverage` signature at `astrid/core/timeline/onscreen.py:366` has no other source argument. `_on_screen` also rewrites clip timing and addresses, so the dictionary is not the retained render config.

The existing source-bound adapter is `astrid/core/rendering/scene_answers.py:127`, `_prepared_host_frames_at(timeline_path, assets_path, frames, *, ...)`. It validates the inherited source against the exact prepared path pair and evaluates inside `prepared_scene_root`, using the actual Root timeline/assets/theme and resolved profile. `inherited_source` and `source_for_timeline` require a timeline path; a plain coverage dictionary cannot supply their binding. `frames_at`/`host_frames_at` are low-level transports, not source-authority admission for an arbitrary authored dictionary.

The offline probe uses the existing real Runtime fixture graph (CAS admission, claim, GenericPackHost materialization), then opens a Checkout for that same saved revision. It validates the actual host-minted source, hands it off through `PreparedTimelineInputs.handoff_source`, and verifies `inherited_source` returns it. While fencing Scene queries, process launch and sockets around the old caller, it observes:

```text
Actual Checkout._on_screen -> coverage:
  type=dict; keys=['clips', 'tracks']; kwargs=['end_frame', 'start_frame']
Retained compiled IDs=['direct', 'occ-1:picture-1', 'occ-1:voice-1']
Fallback IDs=['picture-1']
```

This fixture has an available retained source, not an environment/setup failure. The source still does not cross the selected old caller. Reading an ambient binding without associating this rewritten input with its exact compiled occurrence/source would guess authority. Rebuilding a Scene registry/transition planner or projector here would violate the task. Changing the SDK caller or adding a new carrier/signature is outside the allowed paths/constraints.

Connected checkouts already select `_managed_scene_spans` before this fallback (`check.py:654–656`). That route does not give the detached fallback a retained source. Reusing it would require a caller migration outside the assigned product paths.

## Original positive and assertion disposition

An identical cropped outgoing / adjacent incoming `am-footage` pair, with a four-frame `cross-fade`, produces through the existing `onscreen.coverage` entry:

```text
retained: [(0,26,GAP,None), (26,30,DIP,None), (30,60,COVERED,CONTENT)]
rejected a5cc85cc7: [(0,30,GAP,None), (30,60,COVERED,CONTENT)]
```

The probe loads the donor module in memory using `git show`, without changing files. It confirms the independent review's loss and does not claim a public replacement.

| Assertions | Disposition |
| --- | --- |
| Original core coverage/fade/RLE positives | Unchanged; passing on retained implementation. |
| Original SDK EMPTY, deliberate hold, inset/translucency GAP and declared DIP positives | Unchanged; passing on retained implementation. |
| Cropped transition positive above | Reproduced through old coverage entry; donor loses DIP. |
| Existing explicit source-unavailable and prepared Root lifetime tests | Passing; source/evaluation are doubled in these two unit tests. |
| One-to-one no-source conversions | None. No assertion edits, weakening, skip or xfail. |
| Same original positives through source-bound public old-caller path | **Unverified and blocked by the missing carrier above.** |

Static roles, `_timing_evaluators`, private PNG crop/statistics and all product files remain untouched. The base already pins actual Composition 0.0.14 in `remotion/package.json`/lock; this worker neither activates a capability nor changes/repackages any release. A package pin cannot repair this source handoff.

## Exact commands and results

Run from the worker worktree:

```sh
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-bound-coverage-adapter-1306/probe_bound_coverage.py
```

**Exit 0**, prints the exact transition comparison and real-source caller observations above. Diagnostic script retained in the worker folder only; it is not a new main-suite behaviour contract or a public evaluator proof. Its temporary Runtime realm/materialization is automatically removed.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-bound-coverage-adapter-1306/pytest-temp tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py tests/sdk/test_scene_public_summary_rle.py tests/sdk/test_scene_summary_projection.py tests/packs/rendering/test_scene_only_executor.py::test_scene_only_missing_source_is_explicitly_unavailable tests/packs/rendering/test_scene_only_executor.py::test_prepared_scene_query_keeps_root_alive_and_validates_source
```

**28 passed in 0.96s**, no skip/xfail. The 26 original core/SDK neighbours are included. Temporary pytest output removed after completion.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/core/timeline/onscreen.py astrid/core/rendering/scene_answers.py
git diff --check
git diff --stat
git status --porcelain=v1
```

Ruff: **All checks passed**. Diff check: **exit 0**. Diff/stat/status: **empty**. No full suite, browser, localhost/live socket, renderer/Node helper, install, shared dependency write, copied package graph, physical PNG/audio or public14 capability proof ran. No environment failure is being represented as a pass.

## Decision and next step

Preserve the transition branch and original assertions. Returning blanket UNAVAILABLE for this old entry would silently remove successful detached checks without the required matching public success, so no such conversion was made.

The source owner must bridge this exact `_on_screen -> coverage` boundary with the existing retained source/prepared inputs and occurrence map, or authorize a narrow SDK caller migration using the existing managed Scene route. Then prove the original positives through that caller and explicit unavailability for absent/stale source before removing the transition branch. This report does not reopen the one-evaluator decision; it identifies its missing consumer prerequisite.

Worker handoff: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-bound-coverage-adapter-1306/report.md`, `commit-msg`, `BLOCKED`. No DONE marker; no product commit should be created from the empty patch.
