## Report

Implemented the P2 D96 scope correction.

- Shared `seed3` fixture remains default 12 seconds.
- Added separate explicit 14-second `placementTest`.
- Only automatic child placement uses `placementTest`; element and registerAsset remain on default 12.
- Preserved placement title/body/assertions/waits byte-identically.
- Updated controls for 18 total callers: 17 default, 1 explicit 14.

Validation:

- Placement/receipt controls: 3/3 passed.
- D66 and asset controls: 146/146 passed.
- Python AST/compile: passed, 21 assertions.
- App/Node TypeScript under `/home/user/work/.app-tsc.lock`: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- No browser, service, full suite, merge, or independent review run.

Branch: `tl/app-P2-D96-placement-scope-return-0411`  
HEAD: `422905edcc54ee5dcd0bfc1c67a5c5b829aa6004`

Final source hashes:

```text
bcefb8d185d974302c713ffd378e435922eb245391d75a0875533462833e16bd  harness.ts
0ae315bab74429ac6530b619430f20521002e3e755c840788b0e8fb607718ad0  three-products.p2-elements-assets.spec.ts
1e9b93e3ab9889729ab72a7b7c54728fa37d8a5ead6b8023a60e5111bb6c2c00  p2-placement-seed-window.test.mjs
```

Commit message written and `DONE` marker created.