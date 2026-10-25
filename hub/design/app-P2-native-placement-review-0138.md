# Review report

## Native Undo reply

**Verdict: PASS**

- Source: `tl/app-P2-native-Undo-reply-0127`
- Commit/tree: `6107a8cddb21ada1c454be538eb72b2dad38111b` / `6c101596dd6ebcc247266eecefca70d40e3cdf0b`
- Exact checkout: `/home/user/work/wt/app-pin-6107a8cd`
- Reviewed blobs:
  - `three-products.p2-tour.spec.ts`: `62d799a92fca8b98399b6ca5bbd3a06127cd9d86`
  - `p2-parent-oracle.test.mjs`: `c24f9b3dde68e8328cf0ce5571b450bca17099f3`

Verified source-derived labels and steps, exact authoritative patch/dependency metadata, strict wrong/missing/extra metadata failures, native/modern branches, Undo/Redo predicates, request/reply history, and omission-only fallback behavior.

Commands passed:

- Parent oracle: 16 tests
- Transition oracle: 3 tests
- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`
- Scoped ESLint
- `git diff --check`
- Protected-file hashes and exact two-file delta

Normal merge completed:

`4b98436552bf30f5fb28bbb958b1817430b12e34`

The merged blobs exactly match the reviewed source blobs.

## Managed placement

**Verdict: FAIL**

- Source: `tl/app-A3-placement-coordinator-apply-0127`
- Commit/tree: `a90d4251cac526dd2723e037e5c91d4b547dc56a` / `8007f39e5de281f4b47a5b93cf7650b394081e9b`
- Exact checkout: `/home/user/work/wt/app-pin-a90d4251`
- Reviewed blobs:
  - `drop-position.ts`: `48ce58e641b00ca02c26aae4d9533a7d97a633ef`
  - `external-drop-utils.ts`: `a4af7b39ea051ca697b5938191868b390af2b08f`
  - `drop-position.test.ts`: `c8e8dd8c73995faab2db29388ff816bac9a1bc24`
  - `mountedFileDrop.test.tsx`: `a2f8bffc50ea0f2780d314ff0dc6b9274c04444b`

The actual mounted coordinator and asset planner paths were verified. Pointer geometry retains V2 at `(368,54)` and `32px/s`; generic collision remains V3 at `4.5s`; managed image save resolves through `occurrence.add-media` to V2 at `9s`.

The finite blocking finding is hover-preview inconsistency: the real hover indicator uses generic resolved `trackId/time` (V3 at 4.5s), while the committed managed-image path uses `pointerTrackId` and planner settlement (V2 at 9s). This is a concrete preview/commit mismatch, so placement merge was not requested.

Commands passed:

- 99 focused Vitest tests, including the final 25
- All three App typechecks
- Scoped ESLint
- `git diff --check`
- Protected-six exact hashes
- Old-source comparison against the real mounted path

No reviewer source fixes were authored.

## Submission ledger

Placement failed, so no placement merge or P2 body submission was made. There is no body ID, host, or plan to report. The existing native merge remains the only external state change.

Required `DONE` marker and conventional commit message were created.