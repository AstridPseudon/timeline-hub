# AP2 P1 D21 preflight return

Status: NOTREADY; no actual-ready claim.

Corrected only the existing ap2-P1-chain-h6 row in scratchpad/orch/tests/suites.conf. It now targets App ce82f9dc1797e39172b4b0d78b202066935bbbd0 / tree 2e0ef95cc03f4d620180d9473973587412d97b0c, preserves P1 body SHA-256 f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133 and Gate-5 blob 37caf28577d42fbe98afd2320dffa3c72e6e74b1, and binds the exact fresh receipts venv-agent-child-ap2-p1-5b1-1310 and agent-remotion-ap2-p1-5b1-1310.

The row reports all independent setup failures, labels dependent stages NOTRUN, runs normal hosted global-setup before the harness availability check, performs the existing startDirectHarness() default native parent seed with credential-path/accepted-seed checks and stop() in finally, requires exactly the original two selectors, then runs the unchanged P1 bodies only after all preflight stages pass.

Evidence: row bash -n PASS; current dry run and a missing-pin negative probe both return expected 2 with multiple blockers; source/tree/body invariants PASS; worktree clean. No receipts currently exist, so the real runner, build, browser, live service, and P1 bodies remain unrun.
