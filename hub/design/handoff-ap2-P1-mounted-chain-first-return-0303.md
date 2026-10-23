# P1 mounted-chain first return after source1372 / review0259

Result: **test source repaired; static qualification passes; live H3 proof is
unexecuted by instruction**.

Changed only `tests/e2e/local/three-products.p1-chain.spec.ts`. The accepted
chain now has distinct boundaries for (1) local dependent authoring behind a
held split and (2) trim acceptance after a real disjoint Agent edit. It checks
stable authored created-ID/value/order guards before and after acceptance,
canonical closure/digest/authoritative step dependencies, Agent field
preservation, post-acceptance ACK loss, exact restart retry equality, and one
history record. The refused chain checks structured conflict/current-head data,
retained-save message/state, and canonical original + Agent move preservation.
Old snapshot writes remain forbidden by the network observer.

The original `tests/fixtures/p1-feasibility/cases.json` is a descriptor corpus
with `h3_chain.status = authored-not-go`; its exercised trim intent is pinned to
`src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim.json`. The test
uses the existing real-media direct genesis seam because those descriptors are
not runnable mounted documents. Invalid/preview/unexercised reply variants
remain explicitly outside this selector.

Checks:

- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p1-chain.spec.ts` — PASS, 2 tests listed.
- `node node_modules/typescript/bin/tsc --noEmit` — PASS.
- `node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS.
- `git diff --check` — PASS.

No browser, socket, body, full, or heavy acceptance run was performed. Later
selector and dependencies: the same P1 file after the official Runtime 780
producer READY, App normal 780 plus current-trim join, and v2 Runtime/Agent
client integration are present.
