Goal

Close the remaining B-only App-suite failures classified by `diag-cdelta-0910`, without masking the staging baseline. Inspect each failure against pristine `staging/timeline-v2.1` and classify it as a B regression or an expectation made stale by the shot-layering authored-data boundary; fix only B-owned issues while preserving the behavior each test protects.

Files in the reported delta

- `src/tools/video-editor/data/ShotTimelinePreview.full-caller.a3.test.tsx`
- `src/tools/video-editor/data/ShotTimelinePreview.integration.test.tsx`
- `src/tools/video-editor/data/VideoEditorProvider.staging.test.tsx`
- `src/tools/video-editor/data/useTimelineSave.test.tsx`

Exact acceptance tests

- Run the listed test files directly with the repository's Node/Vitest command and report each file's result.
- Request the central targeted lane for exactly the changed/listed test files and report the exact result.
- `git diff --check`.

The final failures in these files must be either fixed or demonstrated to be the same pristine-staging baseline, with no B-only failure left. Preserve recovery/canonical-head, authored-data, persistence, and save semantics. Never remove, weaken, skip, or xfail assertions merely to match green. Keep any C-owned failures out of this task.

Out of scope

- No changes to C-owned implementation or tests, no shared fixture digest changes, no full suite, browser suite, or render.

Evidence

Put evidence files in `$ORCH/workers/B-reopen-preview-regressions-11/evidence/`, never inside the worktree. Finish with `DONE` and a conventional commit message as usual.
