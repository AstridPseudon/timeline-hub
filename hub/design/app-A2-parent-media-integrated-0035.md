## A2 integrated qualification: PASS

- Integration head: `22efcda3da4005f8663c078439ff0edbfade69be`
- Tree: `3387c860ec236c8631d64e5f979588bd6071e33a`
- Worktree remained clean; no product edits made.

Lineage verified:

- All 3 donor blobs from `1b0428db7d` match exactly.
- Projection `32e2597c10` implementation blobs match exactly.
- Three overlapping projection files are intentionally superseded by the donor successor blobs; no whole-tree equality claimed.

Evidence:

- Targeted suite: **14 files, 299 tests passed**
- Root/App/Node TypeScript checks: passed
- Scoped ESLint (`--max-warnings 0`): passed
- `git diff --check`: passed
- Input: 8,965 bytes, SHA-256 `8f6655383b67cc7b07ae66ecac6b851027c0e0e9db13632e2cf0f8d3f7e0e0`
- Producer output: 1,371 bytes, SHA-256 `94de1a0605e9b9c171558d1012e6c3c70d3f46d3ffaba762b66b251e7f8bd1f5`
- Closure retained: 3 shots, 3 internal timelines, 3 occurrences; pins: 3 shot, 3 internal-timeline, 5 media, 0 document.
- `config.clips` remained absent; raw opaque track data remained retained.
- Exactly one offline `clip.add-media` command, `select: "parent"`, `intent: {}`, no `doc.patch`.
- Selected media preserved all five Runtime fields.
- Image add emitted no `created` or `reads` claims, as expected for this recipe.
- No Runtime submission or authority acceptance claimed.

Callable interface for the next Agent fixture:

`src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.ts:214`  
`producePreparedImageRequestFromPaths(inputPath, outputPath)`

Existing handoff implementation:

`src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:127`  
`createTimelineLocalSaveHandoff`

Exact targeted command and type/lint commands were run from the review brief. The old 2348 fixture is not claimed as acceptance; this was an offline producer qualification only.

Required commit message and empty `DONE` marker were created.