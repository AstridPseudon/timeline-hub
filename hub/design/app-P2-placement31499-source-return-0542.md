## Result

No App source patch was made. Current run 31499 proves a different issue from 20517:

- After reload, the committed revision label is present.
- Canonical rereads return the accepted closure, including the new child clip.
- The mounted child row uses an occurrence-scoped DOM identity, while the assertion supplies the raw authored clip ID.
- Projection source: [shotCompositionProjection.ts:336-348](/home/user/work/wt/app-P2-placement31499-source-return-0542/src/tools/video-editor/data/shotCompositionProjection.ts:336).
- Revision provenance remains correctly supplied/rendered by [ShotTimelinePreview.tsx:258-274](/home/user/work/wt/app-P2-placement31499-source-return-0542/src/tools/travel-between-images/components/ShotTimelinePreview.tsx:258) and [RemotionPreview.tsx:501-510](/home/user/work/wt/app-P2-placement31499-source-return-0542/src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:501).

The central report names `assertReload`; trace inspection shows its label predicate passes, with the nested mounted-row assertion failing at [three-products.p2-elements-assets.spec.ts:1211-1213](/home/user/work/wt/app-P2-placement31499-source-return-0542/tests/e2e/local/three-products.p2-elements-assets.spec.ts:1211). The missing input/owner is the post-reload canonical projected row identity, owned by the caller/oracle boundary—not Runtime or revision provenance. Changing that oracle was explicitly out of scope.

## Tests and validation

- Central run 31499: readiness PASS; original placement journey FAIL.
- Passing comparators: parent 20481 and native asset 27438.
- XML parsing: PASS.
- Trace archive `unzip -t`: PASS.
- Protected e2e hashes matched manifest before/after.
- `git diff --check`: PASS.
- `git diff --quiet`: PASS.
- Vitest, TypeScript, and ESLint were not rerun because the worktree is unchanged.

Current tuple: App `e96be32f`, Agent `5faeec5b`, Runtime `0c62dfa`, Composition `635f4de`.

Required `commit-msg` and empty `DONE` markers were created.