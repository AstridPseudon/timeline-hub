## A4 integrated proof — PASS

- Verified `HEAD`: `8bd7d59e19`; tree: `ef12f75b7d3e6c3ffd36ecd84f053ab46af0c37c`
- Worktree clean; no source or test changes.
- Donor blobs matched exactly:
  - Preview: `fb27e554a9` (`media.ts`, `media.test.ts`)
  - Session: `039fc35ed7` (helper and generic-patch test)
  - Fixture: `40bcffb9f228141bba773c570f6a8451c2d60b0c`
  - D31: 397 lines / 40 assertions

Tests:

```text
Vitest targeted suite: 9 files, 136 passed
Root/App/Node tsc --noEmit --incremental false: PASS
Scoped ESLint (4 files, --max-warnings 0): PASS
git diff --check: PASS
```

The first Vitest attempt was blocked before collection because the prescribed `tmpdir` path was a regular file. Rerun used private `/tmp/w-3d1c2167db/...` cache/TMPDIR with Node 20, runner config, and no cache; it passed.

Production caller remains:

`useTimelineCommandsService → useTimelineSave.applyEdit → localSaveSession/outbox → RuntimeDataProvider.commitTimeline → AstridRuntimeClient/generated transport`

Retained assertions cover the v2 request fields and accepted/conflict reply structure. Runtime transport, replies, and media selections are test doubles; live Runtime authority, browser, HTTP, backend, and full-suite behavior remain unverified.

Wrote the required A4-prefixed commit message and empty `DONE` marker.