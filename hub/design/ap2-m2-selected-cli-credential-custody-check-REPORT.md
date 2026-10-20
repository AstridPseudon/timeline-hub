# APPROVE — selected CLI credential custody

## Exact source reviewed

- Writer commit: `50797493e81fd6fc1a6a61fa6ba01e65e154830d` on `tl/ap2-m2-selected-cli-credential-file-fixture-source`, based on `hub/tl/integration` (`a6fa6ff8c`).
- Diff scope: `tests/e2e/local/support/harness.ts` (10-line diff) plus the new offline `tests/e2e/local/support/selected-param-credential.test.ts`.
- No source changes were made in this review worktree.

## Independent custody findings

1. Frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` treats `ASTRID_RUNTIME_CREDENTIAL` as a credential-file path when it names an existing file. Its reader rejects non-regular/symlinked paths and extracts the `token` field from JSON. The existing harness `provisionCredential()` obtains the token through the normal Runtime `/v1/credentials` route and writes the existing accepted `{token, actor_id}` carrier at mode `0600` under the harness `mkdtemp` root.
2. The fix passes that absolute ephemeral file path through a cloned child environment. The parent environment is not mutated, and the bearer token is no longer assigned to `ASTRID_RUNTIME_CREDENTIAL`. The selected Agent project-pack and Agent CLI children therefore receive the normal path contract.
3. Browser/Door transport remains separate and unchanged: `WORKSPACE_RUNTIME_TOKEN_FILE` still points to `product-credential.json`, while the selected file is only used for Agent-side resolution. The Vite server inherits the selected path only so its canonical resolver child can use the same Agent contract; the non-`VITE_` variable is not browser-exposed, and the product token remains server-side.
4. Cleanup is structurally complete: `DirectHarness.start()` catches setup failures and calls `stop()`, the App fixture finalizer calls `stop()` after child/test failures, and `stop()` waits for the Vite/Runtime process groups before recursively removing the whole ephemeral root. The focused regression covers mode, path-versus-token semantics, product transport preservation, teardown, and idempotent teardown.

## Existing selected wrapper

The wrapper retains the exact frozen tuple and private custody boundaries:

- Agent commit/tree: `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Graph archive SHA: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Composition package: version `0.0.13`, member SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The wrapper clones those checkouts into a per-run root, writes the private source manifest, creates/inspects the expected realm, keeps data/caches/overlay below that root, and traps all exits to remove it (retaining only failure diagnostics). `sh -n` and all tuple/hash checks passed. The wrapper’s prior private-workspace preflight passed twice; I did not rerun workspace/socket/browser execution under this read-only check.

The source diff does not alter product credential/project/source guards, workspace readiness, the genuine P1/P2 admission path, P1/P2 removal/refusal/retry/reload/undo assertions, or the existing 75/77 controls. It does not manufacture a pack ID or history, add a shim, log a secret, or substitute a builtin.

## Evidence

Writer-reported targeted results (not rerun here because this task forbids browser/socket execution):

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — 2 passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx` — 6 files, 71 passed.
- Targeted ESLint and `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- Playwright `--list` for `three-products.selected-param-dev.spec.ts` — exactly 1 test listed.

Independent checks:

- `git diff --check hub/tl/integration tl/ap2-m2-selected-cli-credential-file-fixture-source` — passed.
- `sh -n` on `run-central-selected-p1.sh` — passed.
- Frozen commit/tree, graph archive, Composition member hash, and package-version assertions — passed.

No real selected gate, browser/socket run, `request-test`, or full suite was run. The earlier 8979 gate remains a pre-P1 failure and is not silently reclassified.

## Decision and next step

**APPROVE** the exact writer source for credential/custody correctness and wrapper preservation. The central named selected gate should be rerun once by the orchestrator; its P1/P2 admission and full journey remain the required live qualification evidence.
