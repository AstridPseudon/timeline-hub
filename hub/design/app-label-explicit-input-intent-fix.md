# App label explicit input intention fix

Base verified: `eac3e87d5c2d1f2ad4cb528412f8285a7f49d154` (`tl/app-m3-root-label-clean-focus-fix`). Worktree: `/home/user/work/wt/app-m3-label-explicit-input-intent-fix`.

## Change and decision

`TrackLabel.tsx` replaces final-value equality with an input-activity boolean in its existing edit ref. Focus starts clean; actual input changes mark it dirty. Untouched completion releases its draft to the latest prop. Dirty completion uses the original callback even when the final name equals the initial name. Success releases the capture; refusal retains it, the draft and visible error for an explicit retry. This is the requested UI intention distinction; no server semantics or wire fields change.

Only `TrackLabel.tsx` and its direct `TrackListRenderer.test.tsx` change. All existing row/canvas/session/supersession assertions remain. Phone/tablet remain agent-owned with no name input or capture. Empty string remains an explicit value. The only expected-failure markers remain the three pre-existing drag markers.

## Native proof completed before implementation

Used immutable native source identified by the existing App golden: Agent `77b1f0f7177174571edd7b13b3c010377432597d`, extracted with `git archive` into this worker's notes directory. This executes the actual native implementation, rather than the TypeScript adapter.

Frozen source locations:

- `astrid/sdk/timeline/_scalar_commands.py:12`: reads raw track ID, binds `scalar.target`, records original parent source pin.
- `_scalar_commands.py:41`: `track_set` unconditionally writes every supplied value, including same values.
- `_recording.py:64,125`: records writes even when before equals after; generates original tagged expectation and direct authorship.
- `commands.py:100,135`: verifies supplied expectations and reads before invoking the handler.
- `rebase.py:replay`: replays the original recorded commands through that verifier.

Executable proof: `workers/app-m3-label-explicit-input-intent-fix/notes/native-proof.py`; output in sibling `native-proof.log`.

1. Captured existing App `recipe_m2_app_track_label.json` input with native `capture_track_set`; asserted entire command and after-bundle equal the checked-in golden.
2. Set authored parent track label to `Original`; captured `track.set` with `values: {label: 'Original'}, clear: []`.
3. Asserted exact expectation `parent/track:picture::label = {state: 'present', value: 'Original'}`, direct authorship, and read `{ref: 'parent/track:picture', path: ['id'], state: {state: 'present', value: 'picture'}}`.
4. Asserted one native write with before/after both Original, unchanged output bundle, and successful replay on unchanged state.
5. Replayed that SAME original plan on a copy changed to Remote: native `CommandError`, `kind: dependency_changed`, base Original, theirs Remote, label path; no partial mutation.
6. Replayed on replaced raw ID: native refusal and no partial mutation. Its reported label guard sees an absent original target; the captured ID read also remains unchanged.

Explicit SAME Original is therefore represented by the existing native API and guarded against Remote. No recapture onto Remote, metadata, or policy change is needed. Frozen source extraction was removed after proof; script and log remain.

## Old/new case mapping

| Sequence | Before this fix | After this fix |
| --- | --- | --- |
| Focus Original; remote prop Remote; blur without typing | Shows Remote, no finish | Same; existing clean test retained and strengthened with no presentation callback |
| Original → Temporary → Original; unchanged props; blur | Drops explicit intention | Original callback receives Original exactly once |
| Original → Temporary → Original; remote prop Remote; Enter then blur | Drops intention and shows Remote | Original callback receives Original exactly once; later callback unused |
| Same remote sequence; original finish refuses; refocus/Enter | Never attempts finish, loses draft | Keeps Original and error; retry uses original capture without recapture |
| Empty string, ordinary dirty input across remote props, capture refusal, mounted runtime without port | Existing behavior | Preserved |
| Phone/tablet selection | No label input/capture | Preserved |

Both positive SAME cases also send another Enter after blur and assert no second successful finish. As in the unchanged existing refusal test, a deliberate retry can call the original finish again after it throws; this is not a successful submission and never refreshes guards.

## Exact validation commands and results

Run from the worktree. In the following commands:

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-label-explicit-input-intent-fix/notes
```

Native extraction and probe:

```sh
mkdir -p "$N/native77"
git -C /home/user/peteromallet/astrid-agent archive 77b1f0f7177174571edd7b13b3c010377432597d astrid | tar -x -C "$N/native77"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$N/native77" /home/user/work/venv-agent/bin/python "$N/native-proof.py"
```

PASS: exact native golden, direct same-value recording/unchanged replay, Remote label refusal and identity replacement refusal. Python dependencies stayed read-only; no install or bytecode writes.

For Vitest/lint only, the worktree's own `node_modules` link temporarily pointed at existing read-only `/tmp/app-coherent-deps12/node_modules` (Composition 0.0.12, Vitest 4.1.5). No contents or symlinks inside any dependency tree changed. Own link is restored to `/home/user/work/app/node_modules`. The private config imports the repository config and sets `cacheDir` to `$N/vite-cache`; `--no-cache` disables test cache writes.

Before product change, with new normal positive tests:

```sh
PYTHONDONTWRITEBYTECODE=1 node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
```

Expected RED: exit 1, **32 passed / 3 failed**. Each new case saw zero finish calls instead of Original. Log: `$N/before-fix.log`. No expected-failure marker was used.

After final product change:

```sh
PYTHONDONTWRITEBYTECODE=1 node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/commands/trackLabelCapture.test.ts
```

PASS: exit 0, **4 files / 202 tests**, 23.27 seconds. Log: `$N/targeted.log`. Row suite now has 35 tests versus base's 32; all original tests remain.

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx --no-cache
node scripts/quality/check-known-failures.mjs
git diff --check
git diff --numstat
git status --short
```

All exit 0. ESLint emitted no diagnostics. Known failures: **3 authorized existing drag markers / 0 forbidden**. Diff check clean; status contains exactly the two intended modified source/test files.

## Size, limits and handoff

`git diff --numstat` against verified base:

- Product: 6 added / 5 removed = **+1 net LOC**.
- Direct tests: 61 added / 1 removed = **+60 net LOC**.
- Total: 67 added / 6 removed = **+61 net LOC**, two files.

Source-only result. Actual Runtime pair and browser verification remain **OPEN**. No full suite, build, browser, socket/live Runtime test, project TypeScript check, install, commit, merge, checkout or push ran. No build output/temp file remains in the worktree. No KEEP marker is issued. No blocker or settled-decision deviation was found. Recommended next step: review the two-file fix, then have the orchestrator qualify the actual Runtime/browser pair when that lane is available.
