# App U3b+D39 whole-path review

## Source/tool inventory: PASS

- Current source: `a16645c69c` (`fix(app): adopt D39 recordings...`), merge parents `cd29ff2642` and sanctioned U3b state `82cb5c0005`.
- Runtime producer verified as `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3`; manifest contains 79 artifacts.
- App lock contains 14 consumer artifacts, including `commit_conflict_409` and `retired_route_410`; obsolete `publish_conflict_409` is retained only as historical behavior coverage.
- Normal mapping, generator, artifact, and vendor checks passed.
- Vendor provenance verified at Agent `ba55ac1e9e70156f03f7e31cc1b1ef040bb75b84`, tree `c13d3686`.
- Protected bodies and six dormant D31/D37 areas remain unchanged.
- Generated client/types, transport, capability admission, response validation, canonical adoption, receipts, and conflict/invalid mapping are intact.

## Focused validation: PASS

Exact command:

```text
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/recordedResponses.test.ts \
  src/integrations/runtime/vendorLock.test.ts \
  src/integrations/runtime/client.test.ts \
  src/test/fakeWorkspaceRuntime.recorded.test.ts
```

Result: 4 files passed, 70/70 tests passed.

Also passed:

```text
generators/generate.py --check
scripts/artifact_manifest.py --check
scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime
scripts/build/verify-astrid-vendor-sources.mjs
scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json
git diff --check
```

No typecheck or lint was needed because this was read-only and no source changes were made. No full, browser, HTTP, build, or service suite was run.

## Caller compatibility: FAIL — known incomplete

The sole genuine production incompatibility is:

`src/tools/video-editor/commands/localSaveSession.ts:160`

```ts
const fullV2 = String(SCHEMA_DIGEST) === 'sha256:35c2...';
```

The current generated D39 digest is `sha256:4118...`, so `fullV2` is false.

Consequences:

- `doc.patch` and persisted `documentIntent` saves are blocked before transport.
- Semantic saves transmit without `steps`, `merge`, and `reads` because metadata assignment is gated at line 185.
- Main mounted saves, popup saves, and placement saves all funnel through this function:
  - `useTimelineSave.ts:319`
  - `shotTimelineDataProvider.ts:1035`
  - `placementService.ts:250`

The exact HEAD acceptance evidence records 43 failures across four caller suites. This is caller incompatibility, not a Runtime schema/client failure.

The old `35c2…` digest is valid only for the old 34e tuple. Frozen R4 candidate App is an even older ABI (`fc6c…`) and is not the current D39 comparator.

## Minimal repair guidance for SoleSol1022

Repair the central `localSaveSession` gate only:

- Remove the literal old digest assumption.
- Always attach current generated-contract metadata for D39.
- Preserve verified project/timeline/base IDs, ordered commands, created IDs, persisted step IDs, reads, merge semantics, label, rationale, group ID, `dry_run`, source, and outbox `Idempotency-Key`.
- Preserve the existing `{data, receipt}` response adoption and accepted/merged/rebased/conflict/invalid handling.

No code or test edits were made in this review. Worktree is clean; commit message and `DONE` marker were created.