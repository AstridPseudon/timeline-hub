## Report

- Inspected retained `26387` artifacts: manifest, JUnit, DOM snapshot, trace network, parent/shot payloads, and App load/group source.
- Original failure: `three-products.p2-popup.spec.ts:331`, unchanged 5s wait for `f2-occurrence-copy:` group.
- Parent API returned two canonical occurrences and the shot API returned the internal revision ID. The subsequent internal timeline read produced no HTTP response before teardown (`-1` trace status; not a genuine 404/422).
- App source correctly falls back to the parent timeline scope when the shot lacks `timeline_id` (`dataProvider.ts:694-718`), and same App/runtime comparator evidence completed this read successfully elsewhere.
- DOM remained in canonical loading state with no canonical group label; legacy `f2-app.png`/`f2-video.webm` clips remained visible. No App source defect was proven.

Precise Runtime input: inspect the internal timeline revision read for the captured project/timeline/revision tuple from artifact `.../tests/app-pin-ce1cd9c4-p2-d83-p2-popup-add-2058-1024210432-26387/d66`, under Runtime `dc55b8bc...`.

Tests/checks:

- Focused Vitest: 5 files, 55/55 passed.
- Locked Node 20 App TypeScript check: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Worktree unchanged; six protected spec hashes preserved.

No source change was made because the failure is unproved on the App side. Commit message and `DONE` marker were created.