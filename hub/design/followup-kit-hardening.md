# Follow-up: kit hardening (root causes from 26 Oct)

Lessons #109–#112 in LOOPS.md plus the Opus 18:45Z second opinion. No new features.
1. **Private TMPDIR by default for every test** (today it is opt-in: TEST_PRIVATE_TMP=1 in request-test/test-run).
2. **Pre-build controls run the exact registered command line**, not a helper loader (#111, #112).
3. **Per-run output folders**: each run gets a fresh run-ID directory and refuses to start if it exists (#109).
4. **Harness repairs own the whole check**: rerun end to end and list every failure (#110).
5. **The source tuple carries an asserted `base` per repo**, so delivery-build checks the base, not just whatever origin/main resolves to.
6. **Verifier temp survives a kill**: no 1.07 GB leftover after SIGKILL (finally/rmtree doesn't run on KILL).
7. **Disk floors from measured peaks per repo** (the App verify peaked at ~1.8 GB against a 1.3 GB estimate).
8. **Remove the broken delivery_gate_build wrapper** from the kit copies (it drops --source-tuple and hides SystemExit).
9. **Queued tests expire** after 6 h without a fresh KEEP.
10. **README status generated from recorded gates.** The ZIP README's gate table is static template text and shipped stale (PENDING) on 26 Oct.
