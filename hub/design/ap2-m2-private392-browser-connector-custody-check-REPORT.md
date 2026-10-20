# Private392 browser-connector custody review

## Verdict

**APPROVE the exact source at `4e0454f20085f0268b747ac1c572c0f3a05b40be` for one real test.** No unsafe hunk found.

## Review findings

- The candidate patch has exactly two files and only the intended changes:
  - removes `token: harness.productToken` from the two Door-bound `RuntimeDataProvider` instances in `tests/integration/runtimePrivate392Consumer.test.ts:220-224` and `:254-258`;
  - changes only `DRIVER_SHA` in `scripts/testing/private392-http-runner.sh:49` to `54aa8bf25dee747499ccc3a3f15ebc1c61e95e6cb90c9ab72077d827ae67bd3a`.
- The existing client contract is sufficient: `WorkspaceClient` adds `Authorization` only when `token` is present (`src/integrations/runtime/generated.ts:73-85`). The supplied `doorTransport` calls `DirectHarness.doorRequest`, which injects the hosted Origin (`tests/e2e/local/support/harness.ts:791-798`), while `startRuntime` configures the Door with the product credential file (`:453-461`). This is the supported connector, not a guard bypass.
- The direct Runtime remote provider remains unchanged at `tests/integration/runtimePrivate392Consumer.test.ts:280-285` and `:330-334`; it retains its explicit actor token and `runtimeTransport` bearer header.
- Scenario logic/assertions are unchanged: the candidate diff contains no assertion, fixture, request-body, project-id, or guard edits. The direct-journey blob is identical to its parent (`7f44222a7e87675d2a436b9d8c480c653cde2d06`).
- Existing strict negative controls remain in place: browser `Authorization` is refused as `browser_credentials_forbidden` (`tests/e2e/local/direct-journey.spec.ts:789-795`), the browser page cannot send an `Authorization` request (`:819-825`), and foreign or missing Origin is refused (`:305-330`, `:760-762`). No auth, Origin, Host, or project guard was weakened.
- The Agent `1303ce6b` / Runtime `f8da4b6d` pins, App lock, 13 lock entries, 75-artifact custody, interpreter/import checks, cleanup, and vendor-lock guard are outside this two-file patch and remain unchanged.

## Checks and evidence

Reviewer checks performed:

- `git diff --unified=0 4e0454f20^ 4e0454f20` — PASS; exactly two provider-token deletions and one digest replacement.
- `git diff --check 4e0454f20^ 4e0454f20` — PASS.
- Candidate driver hash — PASS; `sha256` of `tests/integration/runtimePrivate392Consumer.test.ts` is `54aa8bf25dee747499ccc3a3f15ebc1c61e95e6cb90c9ab72077d827ae67bd3a`.
- Direct-journey blob equality against the candidate parent — PASS.
- Worktree status — PASS; this review worktree remained clean.

The source worker’s recorded checks were also reviewed: runner syntax/test, vendor-lock, ESLint, TypeScript, and the existing 30-test control lane all passed. I did not rerun them.

The live `runtimeRestore`/private392 integration and browser direct journey were not run by this reviewer because the brief explicitly forbids browser/socket/request-test/full execution. Thus this is a custody/source approval for the next real test, not a claim that the corrected live run has already passed. Recommended next step: run exactly one central private392 integration selector on this source; classify any result independently.

