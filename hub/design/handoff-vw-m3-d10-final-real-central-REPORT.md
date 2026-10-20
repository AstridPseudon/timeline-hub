# D10 final central Home normal-refresh qualification

## Result

PASS. One named central suite ran the exact owner packet in a disposable
private root. The packet's unmodified generator used real `git` against the
recorded Astrid source commit `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`,
with no `NODE_OPTIONS`, preload, fake git response, source-pin change, manual
hash, or generator semantic rewrite.

Fresh output was byte-identical to the packet's generated vendor tree. The
unexcluded normal generation had 156 files including provenance; the packet
had 147 including provenance, with exactly the nine documented exclusions and
146 recorded vendor files. The verifier passed with 11 Home public imports.

## Exact central command and evidence

- `request-test vw-m3-d10-final-central-without-preload integration-viewing-pack-wrapper-unit --files "tests/e2e/timeline/d10-final-central-without-preload.test.mjs" --no-cache`, then `wait-test`: PASS, result `vw-m3-d10-final-central-without-preload-integration-viewing-pack-wrapper-unit-1020183621-31017`.
- Expanded command: `node --import tsx --test tests/e2e/timeline/viewing-parity/bootstrap.test.ts tests/e2e/timeline/d10-final-central-without-preload.test.mjs`; 1 test passed.
- Central verifier: `Verified 11 @astrid-public imports from src/pages/Home/astrid-public-host.tsx.` and 146 vendor files.
- Existing consumer qualification was reused from the unchanged prior packet evidence: 3 files / 20 tests passed. It was not rerun because those consumer tests and their inputs were unchanged.

The prior worker's preload was inspected: it replaced `execFileSync` with a
`spawnSync` wrapper and copied status/stdout/stderr onto failures. That was
transparent enough to preserve output in its lane, but it still intercepted
the generator's git calls and therefore was not counted as custody proof.

No product integration edit remains in this worktree. No full suite,
typecheck, browser, install, live socket, or shared dependency write was run.
The owner packet remains unapplied and ready for owner merge.
