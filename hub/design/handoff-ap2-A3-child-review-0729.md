# A3 child-placement independent review — FAIL

Reviewed App `cc918bd9f8298392142f0accfb6a4e15c3e2fe33` (`852b8e00460482b668cc0c00d76ec9ae1ccfe16d`) and cumulative WIP `577d4b810`.

The service implementation is safe when explicitly called with `ownerRef`: it validates one canonical occurrence, submits the existing Agent `occurrence.fork` through A2 `LocalSaveSession`/outbox, preserves the sibling physical root, reloads the accepted head, and then performs the existing parent placement. Targeted owner-boundary controls pass.

The production integration requirement is not met. The mounted callers at `useShotGenerationMutations.ts:360` and `addImageToShotHelpers.ts:41` call `placeGeneration` without `ownerRef`, and no other production caller supplies it. The real UI therefore cannot perform same-selected-occurrence placement; the passing unit test is a direct service invocation only. Keep A3 unqualified until the existing selected-occurrence identity is passed through the mounted caller and covered by a caller-level test.

Evidence: 5 Vitest files/79 tests, `tsc`, scoped ESLint, diff checks, App/Agent normal Runtime-34e lock checks all PASS. Composition archive hash/private graph identity `819acf6b…` PASS, but the canonical package-resolution test is blocked by shared `node_modules` Composition `0.0.8`; no shared install was changed. No live Runtime admission, browser, body, build or full suite.
