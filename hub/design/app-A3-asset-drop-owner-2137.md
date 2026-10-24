## Report

Implemented the minimal A3/P2 fix in:

- [drop-position.ts](/home/user/work/wt/app-A3-asset-drop-owner-2137/src/tools/video-editor/lib/drop-position.ts:133)
- [drop-position.test.ts](/home/user/work/wt/app-A3-asset-drop-owner-2137/src/tools/video-editor/lib/drop-position.test.ts:63)

The planner now aligns mutable rows to rendered track order by ID, preserving physical drop ownership before the strict A2 handoff. Existing ownership guards and handoff refusal behavior remain unchanged.

Tests:

- Vitest: 5 files, 115 tests passed.
- TypeScript `tsc --noEmit -p tsconfig.app.json`: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Protected six spec hashes unchanged.
- Mounted post-fix browser journey: not run, per task restriction. Independent review is still required before merge.

Protected hashes:

```text
three-products.spec.ts                 93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b
three-products.mounted-readiness.spec.ts 2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593
three-products.p1-chain.spec.ts        50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17
three-products.p2-popup.spec.ts        4292d0b5928e1390c48d0e33876621a2e9b6c7e0616607a72f1b3fa3873d1de9
three-products.p2-tour.spec.ts         07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c
three-products.p2-elements-assets.spec.ts c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797
```

Commit message and `DONE` marker were created.