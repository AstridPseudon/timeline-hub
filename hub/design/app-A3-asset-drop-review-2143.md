## FAIL — A3 asset-drop ownership review

Target: `5a14972add51959e9d8027062373ba2e16d66605`  
Tree: `b2f92324540cc21cb7d913bd4685f4597d820117`

The source fix correctly aligns rows by track ID. Faithful same-kind reproduction showed old behavior targets `v2`, while current `computeDropPosition` targets rendered `v1`.

Blocking finding: the author regression uses one visual and one audio track. Old code’s compatibility fallback still returns the correct visual `targetTrackId`; it only differs in `requestedTrackId`. Since the production asset path forwards `dropPosition.trackId`, this test does not prove the actual wrong-target handoff. Add a same-kind reordered-track regression asserting the target ID.

Additional concern: `drop-position.ts:138` fabricates empty rows for missing track IDs, potentially defeating required fail-closed missing-row behavior; this needs explicit coverage/decision.

Checks:

- Vitest: 5 files, 126 tests passed.
- TypeScript app check: passed.
- ESLint changed files: passed.
- `git diff --check`: passed.
- Protected six spec SHA-256 hashes: exact matches.
- Only the two assigned files changed.
- No browser/full/service run, per task limits.

DONE marker and review commit message were created.