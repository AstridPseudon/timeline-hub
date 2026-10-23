# D29 shared environment artifact handoff

The App proof worktree adds a single shared projector at `tests/e2e/local/d21-environment.ts`, its offline controls, and a harness-only extension to `tests/e2e/local/three-products.mounted-readiness.spec.ts`. The original P1/P2/Gate-5 bodies and D28 connected/fresh-owner assertions are unchanged.

## Carrier and prefixes

Both App and Farm publish the same safe artifact file:

```text
PLAYWRIGHT_OUTPUT_DIR=$ORCH/tests/<ACTUAL_ID>/playwright-output
$PLAYWRIGHT_OUTPUT_DIR/d21-environment.json
```

App’s external D29 subject prefix is `app-P3-D29-AB-2037`; the leaf/case prefix is `three-products.mounted-readiness`. Farm’s later run must retain that leaf/file prefix under its verified actual request ID and must not use a disposable snapshot or a capped console excerpt.

## Interface

`createD21Environment()` creates a valid bounded version-1 `kind: d21-environment` record with all unavailable observations explicit. `observeD21Harness()` accepts only safe endpoint/profile/source-commit inputs; `observeD21Page()` strips URL query/fragment/userinfo and records only editor origin/path plus sanitized WS host/path; `recordD21Stage()`, `recordD21Readiness()`, and `recordD21Error()` update finite observations; `serializeD21Environment()` rejects JSON over 32 KiB; `persistD21Environment()` writes via `testInfo.outputPath()` and attaches the file.

The record separates `OBSERVED`, `DECLARED`, `UNKNOWN`, and `NOTCAPTURED`. It includes backend start/completion/error/exit, endpoint and door fields, daemon/launcher/CLI import buckets, interpreter/module public-path/source-commit slots, editor compiled-runtime/WS slots, provider slots, tool versions/public paths, build mode/dist presence, readiness, and allowlisted environment-key presence/public numeric values. Unknown daemon imports/lifecycle, provider attachment, compiled runtime base, and door allowed-origin metadata carry exact missing-seam text; no CLI/launcher fact is promoted to actual-daemon truth.

## App 2107 custody

The addition is test-only. App Codex OPS must retain the exact product-source attestation for `2107e1870e51c650d59315f4cc1ab6af338f198c` separately from the actual test target after adding these files. It must not claim whole-tree equality, weaken source guards, or alter the protected original Gate-5/P1/P2 bodies. The new file blobs are the only D29 source delta; the current pre-commit base is `13c2e27254f888e7c434dfc8170652068fbfacbb`.

## Verification boundary

Offline controls and static checks pass. No browser/live service/original journey was run, so the artifact’s connected and fresh-owner facts are intentionally unverified until the approved App service performs the real fixture/backend/editor operation before any gesture. Farm must consume the same schema and preserve failed artifacts.
