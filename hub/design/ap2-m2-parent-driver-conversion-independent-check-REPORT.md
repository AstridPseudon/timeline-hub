# AP2 M2 parent driver conversion independent check

## Verdict

**APPROVE** the narrow assertion/driver conversion in commit
`6221b114004e3f807e32fcf7849762514f72382a` (`test(app): correct manual drop
import identity expectation`). This approves the lineage and expectation
conversion only; it is not new browser qualification.

## Old-to-new assertion map

The exact mounted row from approved `d4c60b271d43df1512477cdbe2cf78dddf3a72e6`
was compared with candidate `6221b1140`. The only row difference is:

```diff
 expect(importedBody.data.entry).toMatchObject({
   object_id: harness.seed.video.objectId,
-  digest: harness.seed.video.digest,
   size: harness.seed.video.size,
   media_type: harness.seed.video.mediaType,
 });
```

Thus the stale import-entry `entry.digest` expectation is removed, while the
actual `entry.object_id`, size, and media type remain asserted. No digest was
invented or moved into the import-entry contract. The separate fixture
integrity checks that prove the stored bytes' SHA-256 identity remain intact.

The existing five-field selection authority is retained and made explicit in
`src/integrations/runtime/mediaImport.test.ts:141-149`:

```text
asset, generation_id, variant_id, object_id, catalog_digest
```

The mounted row still binds `selected.object_id` to
`importedBody.data.entry.object_id` (`three-products.spec.ts:1469`), verifies
the verified request with all five selection fields (`:1476-1480`), and passes
the exact selected object to native `clip.add-media`.

## Retained lineage/guards

- `tests/e2e/local/support/app.ts:189-232` is byte-for-byte the approved
  `File`/`DataTransfer` helper from `e07d31f2608ed5c8c63e04f01946217974758700`.
- The candidate row is byte-for-byte the approved `d4c60b2` row except for the
  one removed `entry.digest` field.
- Genuine decodable `video/webm`/File evidence remains, including object
  bytes, size, MIME, WebM header, SHA-256, and browser metadata checks.
- The normal import remains HTTP 201; the positive normal selection and
  verified read remain HTTP 200; the deliberately altered verified selection
  remains asserted as 404/409; frozen selection behavior remains covered by
  the targeted adapter test.
- Lost ACK, dependent newer edit, reload, Runtime restart, exact retry
  identity/body/response, recovery order, undo, opaque data, single placement,
  order/position, and zero legacy traffic assertions are unchanged.
- The independently approved custody/source guard file is untouched. Its
  existing `current013-integration.test.mjs` suite retains the 16 passing
  guards for exact inputs, paths/identity, symlinked venvs, dirty-source
  refusal, forwarding, postflight mutation, child status, metadata, and
  fingerprint checks.

## Verification evidence

Independent read-only checks:

- `diff -u` of the extracted mounted row from `d4c60b2` to `6221b1140` — one
  deletion only: stale `entry.digest`.
- `diff -u` of the extracted approved drop helper from `d4c60b2` to
  `6221b1140` — no differences.
- `git diff --quiet hub/tl/integration 6221b1140 -- scripts/testing/current013-integration.mjs scripts/testing/current013-integration.test.mjs` — passed; custody guard sources unchanged.
- `git diff-tree --no-commit-id --name-status -r 6221b1140` — exactly the
  expected three App test/support files.

Candidate-reported direct verification:

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/app.ts tests/e2e/local/three-products.spec.ts src/integrations/runtime/mediaImport.test.ts` — passed.
- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts` — exactly one test collected.
- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx` — 3 files, 84/84 passed.
- `git diff --check` — passed.
- Candidate source-lineage comparison — passed.

No browser, build, socket, full suite, or `request-test` was run for this
review, as required. The later recovery/undo behavior remains subject to the
authorized HOME browser gate.

## Decision

Approve exact commit `6221b114004e3f807e32fcf7849762514f72382a` for adoption.
