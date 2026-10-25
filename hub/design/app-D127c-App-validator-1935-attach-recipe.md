# D127c attach recipe

Source-only follow-up recipe; do not execute as part of this task.

1. Admit genuine free disk at or above 5 GB for the light run; stop at the 4 GB floor. If below the floor, report source/static NOTRUN.
2. Use the supported Node 20.19.4 binary from the D127 recipe:

   `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node`

3. Use the canonical D66 source-preflight and one-time `p2-element --submit` recipe from the reviewed D127 recipe, with the exact helper blob from Runtime commit `5747c48931839356b049a8fb6ddaf8f30b5b6d1a` and SHA-256 `a92122c24afc581f71687d25ffc6a4bd8bb7c2e7381e5b47a6be861d23594a1c`.
4. Run only the offline validator positive/mutation selector first:

   `node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c reviewed-profiler validator|D127 reviewed-new validator)' --test-reporter=spec tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`

5. A later protected review may run the original observer bootstrap/body only with a mounted Runtime checkout, localhost services, the exact helper identity, and the plan's one coupled review. No browser, body, D66, SWAP, WAL, recovery, or full-tour result is claimed here.
