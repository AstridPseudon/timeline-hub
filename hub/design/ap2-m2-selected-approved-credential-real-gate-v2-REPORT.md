# AP2 M2 selected approved-credential real gate v2

## Result

**NOT QUALIFIED / BLOCKED before P1 admission.** The source remained the custody-approved App commit `50797493e81fd6fc1a6a61fa6ba01e65e154830d` (tree `a9961c62fe886f26ca0719053da30fe6bfa3dad5`). No App product or shared dependency files were changed.

The existing named wrapper was used unchanged:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh`

It retained the reviewed tuple: Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`, locked App graph archive SHA256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`, and Composition tarball SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Preflight evidence

All bounded preflight checks passed:

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — passed; the credential-path/0600/cleanup regression completed successfully.
- Selected App controls and neighbours — **71 passed** across 6 Vitest files.
- ESLint on the touched selected harness/spec files — passed.
- Playwright collection — selected exactly one test: `local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo`.
- `sh -n` on the existing central wrapper — passed.
- `SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh .../run-central-selected-p1.sh "$PWD"` — `selected DEV private workspace preflight: ready`.

Effective source identity was checked before the gate. The helper remains:

```ts
export function selectedParamCliEnv(base: NodeJS.ProcessEnv, credentialFile: string): NodeJS.ProcessEnv {
  return { ...base, ASTRID_RUNTIME_CREDENTIAL: credentialFile };
}
```

The browser/Door product credential path was not changed. The reviewed credential regression source bytes were:

```text
tests/e2e/local/support/harness.ts                         0b5ac38fc5c11794d2e9ed75d03adf4e085262825a56db36aa73b08e4d630a14
tests/e2e/local/support/selected-param-credential.test.ts  5e376bf6f2092648758b8616f3e4baa5cd7d39477a93d6595b32c3cf9bc61bef
tests/e2e/local/three-products.selected-param-dev.spec.ts  2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
```

## One authorized central run

Exact command submitted once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-approved-credential-real-gate-v2 ap2-m2-selected-real-p1-history-fixture-fix --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-selected-approved-credential-real-gate-v2-ap2-m2-selected-real-p1-history-fixture-fix-1020233704-10734`, exit 1 after 77s.

The central wrapper successfully completed private graph setup, exact one-test collection, and the hosted build (`5577 modules transformed`, built in `55.91s`). The browser journey then failed during the real Agent `project-pack init` handshake, before source admission and before any P1 history existed:

```text
HTTP Error 401: Unauthorized
astrid_runtime_client.generated.ApiError: unauthorized: invalid bearer credential
astrid.sdk.workspace_client.WorkspaceClientError: invalid bearer credential
```

Therefore the run proves neither normal P1 admission nor the downstream P1/P2/removal/refusal/dirty-draft/lost-ack/reload/restart/exact-retry/undo/zero-legacy journey. No selected assertion failed; the test never reached those assertions. No retry was submitted.

Bounded result log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-approved-credential-real-gate-v2-ap2-m2-selected-real-p1-history-fixture-fix-1020233704-10734/log.txt`

Retained sanitized wrapper trace:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`

## Decisions, limits, next step

- Preserved the existing mode-0600 credential-file source and unchanged browser transport; no provider, schema, package, pin, shim, or API changes were made.
- Did not use the stale archived token source, hosted8e substitution, or a fabricated P1/history record.
- Did not prepare the physical selected snapshot fallback cut because PASS prerequisites were not clear.
- No full suite, local browser/socket run, or second central attempt was run.
- Qualification is blocked by the wrapper’s runtime credential handoff: workspace readiness passed, but the selected Agent child’s real file-backed credential was rejected by the frozen Runtime at `/v1/handshake`. The next owner action is to repair that wrapper/runtime credential binding, then independently authorize a future gate; this worker did not retry it.

