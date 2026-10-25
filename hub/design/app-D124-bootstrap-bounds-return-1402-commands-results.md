# Commands and results

1. Exact normal targeted control: the mandated Node 20.19.4 command with `--test-name-pattern='a fixture that throws|P2 Runtime observer bootstrap'` over the fake server and P2 bootstrap files.
   Result: PASS, 2 passed, 40 skipped.

2. Reviewed-helper live control with exact D66 path/SHA and the same supported environment.
   Result: BLOCKED before capture validation; Runtime exited before endpoint readiness. Repeated with `ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER*` names with the same result.

3. Reviewed capture validation using the exact prior protected capture and reviewed SHA.
   Result: PASS.

4. Temporary RED mutation control for retained count, output bytes, UNKNOWN/count contradiction, negative timestamp, sample share 2 and `PRIVATE_MARKER`.
   Result: PASS; each mutation rejected and the positive control accepted. Temporary test removed.

5. `eslint tests/e2e/fake-runtime/server.contract.test.mjs tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`
   Result: PASS.

6. `tsc -p tsconfig.app.json --noEmit && tsc -p tsconfig.node.json --noEmit`
   Result: PASS.

7. `git diff --check`
   Result: PASS.

8. Protected `*.spec.ts` conservation check.
   Result: PASS; no protected spec file changed.
