# Protected review report — FAIL

Reviewed exact candidate:

- Source commit: `bbba1990bce3b38511a34743c49a8cd666fadc47`
- Tree: `981344f5fdf0be5154efb361d7c7646872f6f1c7`
- Worktree: `/home/user/work/wt/app-P2-asset-native-review-0149`
- Base: `74051303cb398b80fa881488ce8851f08343c970`
- Exact two-file delta:
  - `tests/e2e/local/support/p2-elements-assets-receipt.test.mjs` — blob `f68e126f54656566eb7b10494027f09b64896b87`
  - `tests/e2e/local/three-products.p2-elements-assets.spec.ts` — blob `dd31864086c92ba6e3b4519eb019a4ae5d220fdc`

## Finite findings

1. `three-products.p2-elements-assets.spec.ts:186` uses `expect.objectContaining(...)` in the new native inverse request oracle. The brief explicitly prohibits `objectContaining`; this is an unconditional FAIL.

2. Native reply/history metadata is not independently strict enough:

   - normalized `reads`, `expect`, `authorship`, `bindings`, `resolved`, `selections`, and `created` are checked only by type/nonemptiness;
   - authoritative step `patch` and `dependencies` are only required to be nonempty arrays;
   - recorded writes/reads/bindings and dependency fields are only length/type checked;
   - the added controls mutate request fields but do not test malformed authoritative reply/history metadata.

   Therefore wrong producer-derived reads, metadata, patches, or recorded dependencies can pass.

## Predicate map

- Native inverse request: new branch `assertRequestV2:181-217`; exact command, base IDs, `fields`, empty request reads, label, step keys, UUID, ordinals, and empty submitted patch.
- Existing `doc.patch` request path: retained at `219-248`, including `atomic`, omitted request reads, nonempty patches, and omitted step reads.
- Accepted reply: inverse routes to `assertNativeAcceptedReply:299-368`; old commands retain the prior path.
- History: inverse routes to `assertNativeHistoryEntry:420-454`; old history predicates remain.
- Undo history: `assertUndoHistoryEntry:456-495` now requires native inverse, authoritative receipt/head/history identities, native merge mode, recorder fields, and `undo_of`.
- Existing asset/element/placement canonical closure, registry/config/manifest, no-legacy, reload, and Undo behavior predicates remain in the original body.
- Production source remains unchanged and independently confirms the inverse ABI at `src/integrations/runtime/dataProvider.ts:770-800` and the outbox envelope at `src/tools/video-editor/commands/commitSession.ts:218-236`.

## Verification

Passed:

```text
Node20 node:test controls: 23 passed, 0 failed
Vitest semantic/geometry controls: 18 passed, 0 failed
Root/App/Node TypeScript --noEmit --incremental false: passed
Scoped ESLint --max-warnings 0: passed
git diff --check: passed
```

Node20 command:

```text
node --import tsx --test --test-concurrency=1 --test-reporter=spec \
  tests/e2e/local/support/p2-elements-assets-receipt.test.mjs \
  tests/e2e/local/support/p2-media-import-oracle.test.ts \
  tests/e2e/local/support/p2-parent-oracle.test.mjs \
  tests/e2e/local/support/p2-transition-oracle.test.mjs
```

Vitest used the existing App graph with an isolated temporary config/cache; no installs or shared dependency mutations were made.

The central targeted-service invocation returned `No test files found` because that generic suite excludes these Playwright e2e paths. The original live 26-import/browser journey was not run, consistent with the no-localbrowser/no-fulltour constraint and the finite FAIL.

Protected unchanged hashes included:

```text
three-products.p2-tour.spec.ts                 2a275b182f213dd7e0d33c4b4ffbf11fcf1f98ad
support/p2-parent-oracle.test.mjs               0b12316aef58bf2ece3f43c1b7f4b7ff944432c9
support/p2-media-import-oracle.test.ts          da75f00ac541b8bd0c8dca6a32a0249f6296361f
support/p2-semantic-oracle.test.mjs             f6829667a5a22d2b589c824c1293d1c6e8072768
three-products.p2-popup.spec.ts                 d7da4c234fb921c448bc18e9ac174b1a11dbc4a6
support/p2-popup-oracle.test.mjs                d77ecc3c116453e3b0c1106580f7c5dd905114ea
```

No body, host, plan, merge request, or submission was created.

Existing ledger context: the prior asset run reached registry/history/reload checks but failed at the first native Undo predicate because the generic oracle incorrectly required `merge: 'atomic'`; this review confirms the candidate corrects the native `fields` path structurally, but does not qualify it because of the prohibited matcher and remaining weak authoritative metadata predicates.