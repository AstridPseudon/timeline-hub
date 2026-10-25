# D127c later supported bootstrap recipe

This recipe is recorded, not executed. It grants no activation credit.

1. Use Runtime commit `368f53f4454d5908c86de53d174f0bedcf23781c`, tree `8d5683702f36034f27ee7f49737665d66dbc2b75`; verify `tests/helpers/p2_commit_phase_capture.py` SHA-256 `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
2. Use the harness-published App commit descended from protected base `6c0329334797b42565918114f2e760a606b026b6`; its final commit SHA must be written explicitly before execution. The current repaired source file SHA-256 is `59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`.
3. After the harness publishes that final App SHA, run the supported Node 20.19.4 command from the App checkout with Runtime pinned as above:

   `APP_FINAL_SHA=<harness-published-final-App-commit-SHA> RUNTIME_FINAL_SHA=368f53f4454d5908c86de53d174f0bedcf23781c /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 --test-name-pattern='^P2 Runtime observer bootstrap is opt-in, source-pinned, bounded, and flushed on exit paths$' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`

4. Before granting any body/activation credit, check private TMPDIR sink mode `0600`, directory mode `0700`, helper basename/hash/source identity, no helper filename leakage, and the existing lifecycle phases. Keep D130 SWAP/WAL/recovery/full-tour held.

The explicit `APP_FINAL_SHA` value is intentionally pending the harness commit; no live command was run against an implicit or moving App head.
