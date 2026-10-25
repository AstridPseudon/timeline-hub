## Result

Fixed the App-owned omission in embedded `ShotTimelinePreview`: it now passes canonical, local, conflict, and adoption-state revision provenance to `RemotionPreview`.

Changed:

- [ShotTimelinePreview.tsx](/home/user/work/wt/app-P2-placement20517-reload-source-0523/src/tools/travel-between-images/components/ShotTimelinePreview.tsx:258)
- [ShotTimelinePreview.test.ts](/home/user/work/wt/app-P2-placement20517-reload-source-0523/src/tools/travel-between-images/components/ShotTimelinePreview.test.ts:233)

Tests passed:

```text
Vitest: 41 tests passed
tsc tsconfig.app.json: passed
tsc tsconfig.node.json: passed
Scoped ESLint: passed
git diff --check: passed
```

No e2e/full/browser suite was run. Protected e2e/support files remain unchanged.

Decision: `RemotionPreview` already renders supplied provenance correctly; the first proven owner was the embedded caller failing to supply it. Runtime changes were not justified.

Commit message and `DONE` marker created.