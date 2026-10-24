**PASS — offline P2 oracle repair. No live qualification credit.**

Changed only the three authorized files. Complete rows now derive from immutable pregesture state, production allocation/snapping, and source-defined image defaults, including `opacity: 1` and manual geometry. Exact media, labels, claims, command/step keys, omitted reads, `merge: fields`, and empty submitted patches remain enforced.

Source basis: `timeline-asset-plans.ts`, `timeline-data.ts`, `coordinate-utils.ts`, `timelineLocalSaveHandoff.ts`, `shotTimelineDataProvider.ts`, and `localSaveSession.ts`. No product or schema changes.

Genuine serialized parent and occurrence requests pass. Controls reject wrong/missing opacity, unsupported fields, malformed claims, reads, merge, patch, select, args, intent, and metadata. Controls use Vitest to resolve real production imports; caches stay private.

All final commands exited **0**:

```bash
N=/opt/node20/bin/node
C=/tmp/w-297f53ea94/p2-vitest.config.mjs

$N node_modules/vitest/vitest.mjs run --config "$C" --configLoader runner --no-cache tests/e2e/local/support/p2-semantic-oracle.test.mjs
# 7 passed

$N node_modules/vitest/vitest.mjs run --config "$C" --configLoader runner --no-cache src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts
# 46 passed

$N node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
$N node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
$N node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json

$N node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/support/p2-semantic-oracle.ts tests/e2e/local/support/p2-semantic-oracle.test.mjs --max-warnings 0

$N node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.p2-elements-assets.spec.ts
# 3 collected

$N node_modules/vitest/vitest.mjs run --config /tmp/w-297f53ea94/p2-old-new.config.mjs --configLoader runner --no-cache --reporter verbose --silent=false tests/e2e/local/support/p2-semantic-oracle.test.mjs -t 'genuine'
# 4 selected producer probes passed: OLD RED / NEW GREEN

git diff --check
```

The same genuine body was supplied to both helpers. Old/new SHA-256 values matched for each probe:

| Producer | Identical old/new body hash |
|---|---|
| Parent, contain | `d3534f5a88456786e35f1a0e8e80670b030ddb6010743f3b787e47a13159854e` |
| Parent, manual | `d9a18d647f222576ed0bf14c40b61792f45c2462ca2204755d70b96e5cc40549` |
| Parent, snapped | `57892d7c7244ca64816d761ae1d3a73d6bd570323678b46d468fef32e40283f1` |
| Occurrence | `554e9de758ced3294d55ff3a04466433503c5e77ea601c72a2005407655b098b` |

File SHA-256, base `7d3ef22794949e13d420ed151840af648d052db2` → current:

```text
spec
e1fe7a0877c4a64a9648c17260cd1af355acb9a5c8b168f63eec09ec07b6e74f
5f82ec9064abf15e1beada27e3c7905556cbcf66a63bc0a843f685729cb9ae71

helper
076fe9d79a9a019c71f3e19ba6d048fed9d866ada884c718c7cd604b6f21a82e
460bd9110ffd31621c70eaba424ee4faf5cd4498e913fe9afa5aacee972105e4

controls
3e230b582b8bd78d492ad109dfe4f926f26465e3cc8769000997cd91c39e7da7
287aeb8671d1a626b55bba84d0a9a5219b4105a009ef4ec844e69cf3d2eb04f5
```

Original element/doc.patch/inverse region and both authoritative result/history/reload/undo tails are byte-identical to `6635416195`, verified by hashes and direct equality.

No blockers. No browser, backend, sockets, HTTP, service, full suite, build, install, or Git writes. Scratch remained under 7 MB. P2 commit message and `DONE` written.

Next: independent review, then manager-controlled composition.