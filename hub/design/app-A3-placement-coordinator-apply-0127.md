# A3/P2 Application Report

Applied the minimal Sol0112 placement proposal on base `3a2d6067b441b8eee683f2899ee0006615aa6fb0`.

Changed only:

- `drop-position.ts`: preserves rendered pointer track as `pointerTrackId`.
- `external-drop-utils.ts`: uses that track only for single managed image imports; existing asset planner settles final time.
- Focused geometry control.
- Existing mounted A3 drop suite now uses the real coordinator and asserts actual coordinates/resolution.

Fresh application evidence:

- Geometry: pointer `(368,54)` identifies `V2`; generic collision resolution selects `V3` at `4.5s`.
- Mounted managed image path: actual pointer `V2`, planner request settles to `V2 @ 9s`, with `occurrence.add-media`.
- Parent drop remains `V1 @ 5s`.
- Existing stale, ambiguous, missing-reference, sibling, explicit-new-row, generic, media, and planner controls remain covered.

Sol’s retained report recorded the original `5 failed / 93 passed` and proposal reference `98 passed`. Its ephemeral patch/witness files were unavailable, so this is a fresh source-described application; no patch equality or artifact hashes are claimed.

Verification:

- Focused seven-file Vitest suite: `7 files, 99 tests passed`.
- Final post-adjustment targeted Vitest: `2 files, 25 tests passed`.
- Root, app, and node TypeScript checks under `/home/user/work/.app-tsc.lock`: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected six E2E file SHA256 hashes unchanged, including elements-assets:
  `67976926ae233805e3ed8d7e220eaa1bf92d30fb807fd14595f5d0daaee43a2a`.

Current source blob IDs:

```text
drop-position.ts        48ce58e641b00ca02c26aae4d9533a7d97a633ef
external-drop-utils.ts  a4af7b39ea051ca697b5938191868b390af2b08f
drop-position.test.ts   c8e8dd8c73995faab2db29388ff816bac9a1bc24
mountedFileDrop.test.tsx a2f8bffc50ea0f2780d314ff0dc6b9274c04444b
```

No browser/service/full-suite run was performed. Hover-preview consistency remains unverified; these controls do not establish absence of a browser-only defect. Independent core review remains for the orchestrator.

Commit message is prepared at the requested path, and `DONE` was created.