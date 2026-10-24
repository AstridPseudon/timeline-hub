## Report

Readonly recipe correction completed. No App source, tests, pins, config, kit, registrations, runtime, checkout, install, or test-service state changed.

### Exact final-host inputs

These remain explicit future inputs:

```bash
FINAL_AGENT_SHA=<40-hex final Agent commit>
FINAL_APP_SHA=<40-hex final adopted App commit>
AGENT_CHECKOUT=<clean checkout at FINAL_AGENT_SHA>
RUNTIME_CHECKOUT=<clean checkout at becfe6db88b2cc034dba3fafa6c050117cdf2b06>
RUNTIME_SHA=becfe6db88b2cc034dba3fafa6c050117cdf2b06
```

Known Runtime producer:

- Commit: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`
- Tree: `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Schema digest: `sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2`
- Artifact count: `79`
- Manifest version: `sha256:65085756a96619a74de401b90d6e1b4ff0590d5090e4d4d411c50de476f345b8`
- Artifact manifest hash: `sha256:2f3d56b6f83834b4529ecb86657e2a5948bce072342bf46f9a2ab983cae369c3`
- Producer result: `409 passed`, 0 failures/errors/skips, 101.45s

### App vendor commands

App uses `scripts/vendor-lock.mjs`, not `scripts/vendor_lock.py`.

Real App lock files:

```text
config/astrid-cli-surface/vendor.lock.json
runtime.lock.json
```

Commands:

```bash
node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json --producer "$AGENT_CHECKOUT"
node scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer "$AGENT_CHECKOUT"

node scripts/vendor-lock.mjs check runtime.lock.json --producer "$RUNTIME_CHECKOUT"
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$RUNTIME_CHECKOUT"
```

`update` is only valid after the authorized lock selector points to the supplied source commit. Current App `runtime.lock.json` still selects `34eac0041b0891e9011966b39bcbd26053fde5bc`, so it cannot currently be claimed against `becfe…`.

### Direct Runtime-to-App mapping verification

Runtime producer paths and expected hashes:

```text
packages/typescript/src/generated.ts
  sha256:7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4

packages/typescript/src/contract-metadata.ts
  sha256:1028aaeca1cd15f860994c1e830ba69f55405e648841877eff4d43f466f40c79

packages/typescript/src/timeline-commit-types.ts
  sha256:bf4728831e35bdfec96ffa0188feb439f3c89a2aecfa8682925019eba5855470

contract/schemas/timeline-config.schema.json
  sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd
```

Verify directly, without trusting the lock alone:

```bash
cmp <(git -C "$RUNTIME_CHECKOUT" show "$RUNTIME_SHA:packages/typescript/src/generated.ts") \
  src/integrations/runtime/generated.ts

cmp <(git -C "$RUNTIME_CHECKOUT" show "$RUNTIME_SHA:packages/typescript/src/contract-metadata.ts") \
  src/integrations/runtime/generated-contract-metadata.ts

sha256sum src/integrations/runtime/generated.ts \
  src/integrations/runtime/generated-contract-metadata.ts
```

Current App status: `generated.ts` matches `7be7…`; `generated-contract-metadata.ts` is stale at `001186de18c627be1930c3b77b78afb1b15a3eea4bd8401931e251643f33c972`. App code still references the old schema digest `sha256:35c2d9…`; no compatibility credit is claimed.

### Exact maker argv

Child environment:

```bash
request-child-venv NAME AGENT_SHA \
  --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
```

Runtime maker:

```bash
request-runtime NAME AGENT_SHA LOCK_SHA256 \
  AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA TEMPLATE_SUITE [NODE_BIN]
```

Approved templates are `agent-remotion-0013-nodes` and `remotion-env-nodes`. `LOCK_SHA256` is the full 64-hex lock digest without a `sha256:` prefix. Final Agent SHA, clean checkouts, and lock digest are not yet available; no final runtime is claimed.

### Suite matrix and counts

Valid existing rows:

- P1: `ap2-P1-chain-h6` — 2 cases in `three-products.p1-chain.spec.ts`
- P2: `full-e2e-three-products` — 8 cases across the three `three-products.p2-*.spec.ts` files
- P3: `ap2-P3-gate5-h6-0348` — 1 gate journey plus its reset precondition

Missing registrations, therefore unavailable:

- `p4-v2-http-nodes`
- `first-capture-integration`
- `marked-integration`

Exact future P4 request:

```bash
request-test integration:agent p4-v2-http-nodes --files \
"tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document"
```

P4 count: 3 service nodes.

P5 scope:

- `tests/test_timeline_commit_integration.py`: 14 integration tests
- `tests/test_timeline_commit_crash.py`: 24 crash tests

Existing `commit-integration` covers only the Runtime integration command; it does not establish complete P5 coverage.

```bash
request-test integration:runtime commit-integration
request-test integration:runtime first-capture-integration
request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py
```

Total proof-map count: 52 behavioral cases, plus the P3 reset precondition. Missing registrations are not evidence that the host is fundamentally unsupported.

The production caller and C0 v2 request/reply shapes remain unchanged, including scoped bases, commands, label, steps, merge, reads, `created`, `Idempotency-Key`, and `{data, receipt}`.

### Verification

- `git diff --check HEAD` — PASS
- `git status --short --branch` — clean
- No tests, HTTP/browser runs, full suites, child creation, checkout, install, or registration request performed.
- No old receipt was relabeled; historical `079`/`37eb` material was preserved.
- No commit needed; commit-message marker written.
- `DONE` marker created.