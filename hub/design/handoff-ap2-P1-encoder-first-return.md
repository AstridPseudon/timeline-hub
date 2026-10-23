# P1 encoder first return handoff

## Verdict

**PASS for the interim encoder slice; not H3 GO.** Only the App test file changed. The genuine pinned Agent split fixture now has exact complete-delta assertions: the full `right` insertion payload, `clip-a` before-values and three intended updates, original order, `created`, physical root, mirrored arrays, preserved unknown/opaque fields, and input immutability. The existing complete trim test is unchanged.

## Exact identities

- Base: `d5dded578b21c41f0d0e7ba6bd046ae21723f023`.
- Modified test SHA-256: `198a22068c6c99b2ece932273a4728068a559e97da94586037b893f9130a946b`.
- Pinned split fixture: Agent commit `cda4d18ca1e0369ee2e1398f5d594ffda75647dc`, SHA-256 `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204`.

## Evidence

- Combined targeted Vitest command: **PASS**, 2 files / 14 tests.
- `node node_modules/typescript/bin/tsc --noEmit`: **PASS**.
- Targeted ESLint command with `--max-warnings 0`: **PASS**.
- `git diff --check`: **PASS**.

## Remaining limits

The encoder has no production caller: repository imports are only its implementation plus `documentPatchIntent.test.ts` and `p1EncoderCorpus.test.ts`. It remains unsent; mounted A2 is App-owned. The split→trim-after fixture/mounted chain, production mount, outside-sandbox service, full/browser/live-socket suites, and full v2 ABI/reply evidence remain unexecuted and unclaimed. Local tests do not earn H3 GO or replace the v2 contract boundary evidence. Provenance checks, including all seven current and all eight historical hashes, were preserved.
