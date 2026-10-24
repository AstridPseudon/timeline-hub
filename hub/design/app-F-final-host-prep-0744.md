## Report

Prepared the bounded read-only final-host recipe. No source, test, pin, config, suite, registration, generated, or design files changed.

Current App tuple:

- HEAD: `38b29b5e295f0ef0c6cee6af598812021d7105aa`
- Tree: `4561b53e00545003e3ae7d9e479cc070a30f0791`
- Worktree: clean

Known Runtime producer:

- Commit: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`
- Tree: `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Source/result: 409 PASS, retained result `409 passed` in 101.45s
- Producer inventory: 79 artifacts; schema digest `sha256:4118b1…`; manifest version `sha256:650857…`
- Consumer custody currently FAILS because Agent/App generated clients and locks are stale. No compatibility credit is claimed.

### Existing route recipe

After authentic `finalAgentSHA` and final App SHA are supplied:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout agent "$finalAgentSHA" "final App-host Agent source"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout runtime becfe6db88b2cc034dba3fafa6c050117cdf2b06 "final Runtime producer"
```

Use the existing vendor route:

```bash
python scripts/vendor_lock.py update runtime.lock.json --producer <exact Runtime checkout>
python scripts/vendor_lock.py check runtime.lock.json --producer <exact Runtime checkout>
```

App generated mappings must come from:

- Runtime `packages/typescript/src/generated.ts` → App `src/integrations/runtime/generated.ts`
- Runtime `packages/typescript/src/contract-metadata.ts` → App `src/integrations/runtime/generated-contract-metadata.ts`
- Public source root: `vendor/astrid-build-inputs/public`, overridable with `ASTRID_PUBLIC_CHECKOUT`

Use only the existing Remotion route with exact source carriers, approved template (`agent-remotion-0013-nodes` or `remotion-env-nodes`), Node `20.19.4`, npm `10.8.2`, and `request-child-venv --source-carrier <Agent checkout> <Runtime checkout> <Runtime SHA>`. Reuse is valid only when child source, Runtime client identity, import origins, and installed reports authenticate the same tuple.

### Supported P1–P5 routes and inputs

- P1: `ap2-P1-chain-h6`; `tests/e2e/local/three-products.p1-chain.spec.ts`
- P2: `full-e2e-three-products`; the three `three-products.p2-*.spec.ts` files
- P3: `ap2-P3-gate5-h6-0348`; `tests/e2e/local/three-products.spec.ts` plus `support/gate5-reset-precondition.test.mjs`
- P4:

  ```bash
  request-test integration:agent p4-v2-http-nodes --files "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document"
  ```

- P5:

  ```bash
  request-test integration:runtime commit-integration
  request-test integration:runtime first-capture-integration
  request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py
  ```

The current `suites.conf` contains the historical App P1/P2/P3 rows, but no current P4 `p4-v2-http-nodes` or P5 `first-capture-integration`/`marked-integration` rows. This is an owner-side registration input, not something changed here.

The existing callers provide fail-fast preflight, report-all failure aggregation, durable `$ORCH/tests/$RUN_ID/preflight/` logs, per-stage records, and per-stage Playwright output. Every final gate must retain the same run ID across the actual host, clean Agent/Runtime checkouts, keyed child, imports, source/body fingerprints, and terminal packet.

C0 caller contract is preserved: scoped v2 commit request with base IDs, commands, `created`, label, steps, merge, reads, `Idempotency-Key`; replies retain `{data, receipt}`, canonical document/digest, id map, accepted/base/previous IDs, merge mode, publisher, durable receipt, and accepted/merged/conflict/invalid status details. App’s production POST route is `src/tools/video-editor/commands/localSaveSession.ts:179-188`.

### Verification

- `git diff --check HEAD` — PASS
- `git status --short --branch` — clean
- No tests, service requests, HTTP/browser runs, builds, installs, child creation, checkout creation, or full suite were run.

Missing inputs remain explicit: genuine `finalAgentSHA`, final adopted App SHA, exact clean checkouts, authenticated child/Remotion receipts, current service registration, and Proof’s same-ID terminal packet. Historical `079`/`37eb`/old App receipts remain preserved and were not relabeled.