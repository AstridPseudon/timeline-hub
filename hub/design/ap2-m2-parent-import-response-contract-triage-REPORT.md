# AP2-M2 parent import response contract triage

## Classification

The latest genuine-drop failure is a test expectation error, not missing Runtime
selection evidence and not a Runtime data-loss/security finding. The real
`POST /media-imports` response has the normal import contract:

```json
{
  "entry": {
    "object_id": "sha256:<opaque digest>",
    "media_type": "video/webm",
    "size": 160935,
    "filename": "manual-drop.webm"
  }
}
```

It intentionally does not include `entry.digest`. The object identity is
already carried by `entry.object_id` (and `asset_id`). The later normal
`GET /media-selection` response supplies the immutable five-field selection,
including `catalog_digest`; `GET /media-selection/verified` returns that exact
selection and verified media metadata. The deliberately altered object
selection received the expected refusal, while the original selection received
HTTP 200.

Runtime source confirms this contract at
`/home/user/work/runtime/runtime_protocol/service.py:4980-5083` and
`/home/user/work/runtime/runtime_protocol/timeline_commit_port.py:734-842`;
the generated TypeScript contract at
`/home/user/work/runtime/packages/typescript/src/generated.ts:20-21` also has
no import-entry `digest`. Existing Runtime tests cover the exact five-field
selection and mismatch refusal in
`/home/user/work/runtime/tests/test_timeline_verified_media.py:108-179`.

## App change

The current latest integration base has no mounted manual-drop e2e row (the
failing donor row is not an ancestor of this base), so I did not resurrect that
large donor test. I made the row-local App contract test explicit in
`src/integrations/runtime/mediaImport.test.ts:141-172`:

- added one exact positive assertion for the five-field `prepared.mediaSelection`;
- retained the assertion that the registry `entry` has no `catalog_digest`;
- retained the existing wrong-object mismatch refusal at lines 191-198;
- made no consumer, wire, provider, store, schema, pin, or Runtime changes.

The existing App consumer continues to carry the selection outside the asset
registry (`src/tools/video-editor/hooks/useAssetManagement.ts:244-250`) and
uses the existing verified-media read before native media mutation
(`src/tools/video-editor/hooks/useTimelineCommandsService.ts:474-540`). No
browser authority or fabricated digest was added.

## Retained evidence

Raw trace and bounded browser evidence remain at:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/recorded-evidence/playwright-trace.zip`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/recorded-evidence/bounded-browser-evidence.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/recorded-evidence/error-context.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/recorded-evidence/runner-tail.log`

The bounded record shows POST 201, normal selection GET 200, wrong verified
selection 404, positive verified selection 200, and empty console/error
collections. This report omits request credentials and does not copy trace
headers or secrets.

## Verification

- The initial direct `npx vitest run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism ...` startup failed before collection because this repo's config references `__dirname` under the ESM runner. A private one-line preload supplied only that config compatibility value; it was removed after the run.
- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-import-response-contract-triage/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx` — **passed**, 3 files / 84 tests.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 src/integrations/runtime/mediaImport.test.ts` — **passed**.
- `node_modules/.bin/tsc --noEmit --pretty false --project tsconfig.app.json` — **fails on pre-existing unrelated cross-repo type errors** in Astrid status and timeline-composition exports; no error points to the changed test.
- `git diff --check` — **passed**.

No request-test, local browser/socket, or full suite was run per task scope.

## Peer-owned follow-up

No Runtime fix is required. If the donor e2e row is reintroduced on a future
integration base, remove only its expectation of `importedBody.data.entry.digest`
and keep its exact selection and verified-read assertions unchanged.
