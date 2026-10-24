## Result

Source-supported setup expectation proposal; no production files changed.

Root cause: the mounted file drop reaches generic `handleFileDrop` → `dropAsset` and creates an `uploading-*` skeleton. It never reaches `occurrenceAddMediaPort`. The missing wiring is in:

- `useTimelineState.ts:895`
- `useExternalDrop.ts:130, 682`
- `external-drop-utils.ts:422`
- `useAssetManagement.ts:312`

The allowed occurrence/session files already contain the guarded port and negative controls; fabricating ownership there would be unsafe and out of scope.

## Retained evidence

- Readiness: PASS.
- Runtime media import: returned successfully.
- Media selection: returned successfully.
- Drop evaluation: returned successfully.
- No intended commit POST.
- DOM retained the uploading skeleton.
- Original failure: `waitForResponse` timeout at `commitFromGesture` lines 149/565.
- No browser/original rerun performed.

## Verification

- Focused Vitest: 3 files, 97 tests passed.
- TypeScript: `tsc -p tsconfig.app.json --noEmit` passed.
- `git diff --check` passed.
- ESLint: N/A; no source/test files were touched.
- Protected six SHA-256 values verified unchanged:
  - `93c2bf4c…559a64`
  - `2b9723db…301593`
  - `50960dd2…9ebf17`
  - `f2d63c70…54d10`
  - `07fe3d84…ed2f3c`
  - `413d314d…fa4133`

Commit message and `DONE` marker created.