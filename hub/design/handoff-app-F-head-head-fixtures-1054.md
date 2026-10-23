# App F head-fixtures handoff

## Result

PASS. The 34 stale fixture failures are fixed at the transport boundary. The
production paired-head read remains unchanged and now receives the same
metadata-only public timeline projection that Runtime serves: project/timeline
identity, `head_revision_id`, `head_publication_id`, and catalog metadata. The
fake fixture uses the established `publication-current` identity with its
current dynamic revision; strict null/race overlays in existing tests remain
unchanged.

The four allowed paths changed:

- `src/test/fakeWorkspaceRuntime.ts`
- `src/integrations/runtime/resolveProjectSelector.test.ts`
- `src/integrations/runtime/timelineCommit.test.ts`
- `src/tools/video-editor/pages/VideoEditorPage.test.tsx`

The mutable timeline write guard and retired document route guard were not
removed. No production caller, assertion, v2 request shape, or save path was
changed.

## Evidence

Base: `7e0af6c9cda5a81a89505b006fcd653d4a5fc770`.

Original exact focused command: 34 failures / 117 passes across 4 files.
After the fixture updates: **4 files, 151/151 tests passed**.

Direct fixture/provider neighbors: **3 files, 119/119 tests passed**.

Required App TypeScript check passed:

```text
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
```

Scoped ESLint and `git diff --check` passed for the changed paths. No full,
browser, journey, localhost, install, or shared-dependency run was performed.

## Decision and next step

The public GET is intentionally supported per Runtime0637/App507. Its response
is metadata-only; mutable document bytes remain retired. The late-A test
transport returns its independently observed `r3`/`p3` pair so the existing
head race proof remains strict.

Recommended next step: independent review, then harness commit/merge of this
worker. The farm should re-run the App full suite on the merged current head;
this worker does not claim full-suite coverage.
