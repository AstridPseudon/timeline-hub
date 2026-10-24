# Final host review: FAIL

The existing route is not actionable as written. No source files were changed.

## Findings and exact corrections

- **Vendor lock:** App has `scripts/vendor-lock.mjs`, not `scripts/vendor_lock.py`. The valid App commands are:

  ```text
  node scripts/vendor-lock.mjs check <lock> [--producer <checkout>]
  node scripts/vendor-lock.mjs update <lock> --producer <checkout>
  ```

  The proposed `runtime.lock.json` route is therefore an Agent-side command, not the App normal route. App runtime generated files must be adopted from the Runtime producer and verified directly.

- **Runtime adoption:** `generated.ts` currently matches final Runtime producer bytes:

  ```text
  sha256 7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4
  ```

  `generated-contract-metadata.ts` is stale:

  ```text
  App:     001186de18c627be1930c3b77b78afb1b15a3eea4bd8401931e251643f33c972
  Runtime: 1028aaeca1cd15f860994c1e830ba69f55405e648841877eff4d43f466f40c79
  ```

  App code still guards the old schema digest `sha256:35c2d9…`, while final Runtime is `sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2`. This cannot receive compatibility credit.

- **Child venv argv:** The proposed invocation omits the required name and Agent SHA. The actual form is:

  ```text
  request-child-venv NAME AGENT_SHA --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
  ```

- **Remotion runtime argv:** The exact source-carrier maker/request route is:

  ```text
  request-runtime NAME AGENT_SHA LOCK_SHA256 AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA TEMPLATE_SUITE [NODE_BIN]
  ```

  Approved templates are `agent-remotion-0013-nodes` or `remotion-env-nodes`. The final Agent SHA, clean checkout, and lockfile SHA are missing, so no final runtime can be claimed.

- **Suite registration:** `p4-v2-http-nodes`, `first-capture-integration`, and `marked-integration` are absent from the actual registry. `commit-integration` exists, but covers only the Runtime integration command and does not establish the complete P5 scope. Missing registrations mean unsupported/unavailable routes, not proof that the host is fundamentally unsupported.

  `request-test` requires:

  ```text
  request-test integration:REPO SUITE [--files "a b c"]
  ```

  The three P4 nodes and `--files` form in the proof map are correct, but the suite must first exist in the registry. No registration was added per task constraints.

## Proof-map scope check

The proof maps are internally correct:

- **P1:** `tests/e2e/local/three-products.p1-chain.spec.ts`, two cases covering accepted/merged recovery and refusal rollback.
- **P2:** eight cases across exactly:
  - `three-products.p2-elements-assets.spec.ts`
  - `three-products.p2-popup.spec.ts`
  - `three-products.p2-tour.spec.ts`
- **P3:** `tests/e2e/local/three-products.spec.ts` plus its reset precondition.
- **P4:** exactly three service nodes:
  - `test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
  - `test_http_ten_note_commit_per_step_inverse_and_redo`
  - `test_http_note_conflict_reruns_public_function_from_verified_peer_document`
- **P5:** `tests/test_timeline_commit_integration.py` with 14 integration tests plus `tests/test_timeline_commit_crash.py` with 24 crash tests.

The production caller still uses the exact C0 v2 request/reply shapes, including scoped base IDs, commands, label, steps, merge, reads, created, `Idempotency-Key`, and `{data, receipt}` response fields. Existing interface facts are valid even though final Agent custody is missing.

## Custody status

Final Runtime producer facts:

- Producer: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`
- Tree: `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Schema digest: `sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2`
- Artifact count: 79
- Manifest version: `sha256:65085756a96619a74de401b90d6e1b4ff0590d5090e4d4d411c50de476f345b8`
- Artifact manifest: `sha256:2f3d56b6f83834b4529ecb86657e2a5948bce072342bf46f9a2ab983cae369c3`
- 409-result: PASS, 0 failures/errors/skips, 101.45 seconds

Producer source/result passed, but consumer custody/adoption failed because Agent/App pins are stale. Abbreviated hashes are insufficient custody evidence.

The cited caller `d54582a08c6ad0453742523a3ec374dd321ce477` and target `66354161950d1e747965c095ea97b881d2592708` remain historical reference material. Current App is `38b29b5e295f0ef0c6cee6af598812021d7105aa`, tree `4561b53e00545003e3ae7d9e479cc070a30f0791`. Final Agent SHA and final adopted App SHA remain explicit missing inputs. Final Agent absence does not invalidate the existing caller/interface facts.

## Verification

- `git diff --check HEAD` — passed.
- Worktree remained clean; no tests, browser journeys, HTTP runs, child creation, checkout, install, registration, or source mutation were performed, as required.