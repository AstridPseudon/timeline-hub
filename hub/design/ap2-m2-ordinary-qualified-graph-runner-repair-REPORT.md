# AP2 M2 ordinary qualified graph runner repair

## Result

PASS. Ported the approved bbffe ordinary closure oracle into the current App
test source. The ordinary test now reads the pre-A parent revision plus the
manifest-pinned shot and internal-timeline revisions through normal Runtime
reads, asserts the complete closure shape, and compares the final ordinary
undo against that independent closure with only the disjoint Agent S1 label
overlaid.

No product behavior, dependency, package pin, schema, Vite configuration, or
assertion weakening changed. The current `config/vite/vite.config.ts` is
byte-identical to e401af721 (`sha256 dea422fb35c4113343168ec69c8e9366b999ae870173e11268b4101f743a4391`).

## Effective graph proof

In a disposable private copy, copied from the current source tree, I cloned
the locked Agent 8130 source, built a private package graph from the protected
graph, copied Composition rather than linking it, and ran from the copied App
root. App createRequire and App/Agent Vite resolution all selected Composition
0.0.13, evaluation digest
`e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`, exactly
77 package files, with both `getSanitizedPlaybackRate` and `clipOpacity`.
The copied-source hosted Vite build passed. Temporary proof paths were removed
after the run; shared installs and caches were not modified.

## Tests

- `git diff --check` — PASS.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/ordinaryRealBatch.test.ts src/tools/video-editor/dev/localExtensions.catalog.test.ts src/test/threeProductsAuthoring.test.ts` — PASS, 5 tests.
- Central authoritative gate, requested exactly once after graph proof:
  `request-test ap2-m2-ordinary-qualified-graph-runner-repair e2e-m2-ordinary-committed-driver-gate` — PASS, 1/1 ordinary test; hosted build and Chromium smoke passed; 29.8s test duration, 100s total.
  Evidence: `.../scratchpad/orch/tests/ap2-m2-ordinary-qualified-graph-runner-repair-e2e-m2-ordinary-committed-driver-gate-1020232857-26437/`.

The central run retained the sanitized log, summary, source snapshot, and
status records. It produced no failure trace/request-response artifact because
the ordinary test passed; the committed driver cleaned its private browser and
graph paths as designed.

## Decisions and disposition

- Reused the existing ordinary committed-driver runner, not the failed
  public13-integration runner.
- Ran Vite graph inspection from the copied App root; inspecting from the
  worker root demonstrably resolves the shared 0.0.8 package and is not valid
  gate evidence.
- Preserved the later current-branch bootstrap and ordinary-trim changes while
  porting only the approved closure-oracle correction.

No blockers. No full suite or additional local browser/socket run was made.
