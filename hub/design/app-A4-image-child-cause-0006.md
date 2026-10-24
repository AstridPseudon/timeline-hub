## A4 report — image child guard source/callgraph classification

No product, test, fixture, dependency, graph, row, kit, pin, or deletion changes. Worktree remains clean at `4ded7eefdbcbeaf0d6cecc58e55f7083004167d2`.

Conclusion: the refusal is not caused by generic capture and is not bridge-only. The exact same production handoff guard rejects this canonical document before prepared-media command encoding.

Evidence:

- Fixture entry: [`preparedImageRequestProducer.ts:184-198`](</home/user/work/wt/app-A4-image-child-cause-0006/src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.ts:184>)
- Real UI preview/apply path: [`useTimelineCommandsService.ts:499-508`](</home/user/work/wt/app-A4-image-child-cause-0006/src/tools/video-editor/hooks/useTimelineCommandsService.ts:499>)
- Production prepared-media handoff: [`useTimelineCommit.ts:428-450`](</home/user/work/wt/app-A4-image-child-cause-0006/src/tools/video-editor/hooks/useTimelineCommit.ts:428>)
- Production capture call: [`useTimelinePersistence.ts:1010-1015`](</home/user/work/wt/app-A4-image-child-cause-0006/src/tools/video-editor/hooks/useTimelinePersistence.ts:1010>)
- Exact first refusal: [`timelineLocalSaveHandoff.ts:218-221`](</home/user/work/wt/app-A4-image-child-cause-0006/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:218>)

Observed refusal:

- Class: `TimelineVersionConflictError`
- Code: `timeline_version_conflict`
- Message: `Local document save retained: child ownership/fork mapping is unavailable`
- First return: `timelineLocalSaveHandoff.ts:221`

Input:

- File: `agent-A4-image-valid-2348-input.json`
- Bytes: `8,965`
- SHA-256: `8f6655383b67cc7b07ae66ecba6c851027c0e0e9db13632e2cf0f8d3f7e0e0`
- Canonical root: parent revision plus 3 shot revisions and 3 internal-timeline revisions
- Parent payload: 1 clip, 3 tracks, 3 occurrences, 1 registry asset
- Target command scope: `select: 'parent'`
- Prepared asset is not already registered, so the prepared-media handoff is selected
- Closed five-field media selection and parent/timeline/head mappings are structurally valid

Generic-capture classification:

- `preparedImageRequestProducer.ts` does not import or call `genericPatchCapture`.
- The prepared branch creates `clip.add-media` with `select: 'parent'` at handoff lines 278–279.
- Generic `doc.patch` encoding is only reached when no semantic command is available; this path is rejected earlier at the child-ownership guard.

RED/GREEN proposal:

- RED: current mixed parent/child canonical input deterministically refuses at the guard above.
- GREEN candidate: a genuinely parent-only canonical fixture with no child closure should reach subsequent prepared-media checks. Preserve child/parent canonical data and pins; do not weaken the guard. A child-target save would require a separate authored assembly/ownership mapping, which is outside this task.

Limits:

- Downstream checks after the first guard were not observed.
- No production acceptance, Runtime response, browser, HTTP, backend, full suite, or test-service run was performed.
- `git diff --check` passed.
- Completion marker and no-op commit message were recorded.