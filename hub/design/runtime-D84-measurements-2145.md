# R2r D84a request-scoped replay result

Product parent: 7aa603d13762b499af2279e4c1340b31b6eda5a2, tree daa9efc4a158e9bc4f6fe2186dd28ffd00800405. The preserved stopped2142 branch equals this parent; git diff was empty and its finalizer recorded a clean worktree. No WIP source existed to retain. No stopped2141 source imported.

This change only memoizes successful deterministic recorder/retained-capture replay validation. The key is authenticated project ordinal plus a digest of ledger/edge bytes and fresh source/base closures, continuations, inverse history, event prefix and project realm. Current DB/event/hash-chain/physical-owner/input/materialization predicates still execute on every use. Thus raw _verify_accepted wrapper counts remain 1/11/21; full _verify_accepted_replay counts become 1/2/3. Do not label the former count as reduced. A changed source with valid replacement payload+digest, but fixed ledger/edge/head/events, is a concrete counterexample to entry-only memoization; the focused test confirms the fresh source context forces failed replay instead of a stale hit.

No lock placement, head CAS, schemas, provider, budget, persistent prefix, cross-request cache or D42 trust change. The coordinator creates a fresh explicit scope for each execute; public history API creates a fresh scope even when nested. Direct top-level store evaluations create and clean their own scope; internal nested store reads share the exact evaluation. Thread-local scope state is restored and cleared in finally on every return/exception/BaseException. No failed replay is added.

## Genuine paired control

Central targeted control runs the normal Astrid RuntimeCommitService provider, RuntimeDaemon/HTTP door and generated WorkspaceClient. Public empty bootstrap, then normal track.create commands captured from each actual document with capture_track_create and commands.execute. Full v2 body carries exact base pair, label, per-command steps, merge=fields, explicit reads, source/rationale and dry_run=false. Accepted data equals receipt.result. Provider/compiler signature is astrid-v1 / authoring-bundle-1. Command/step ordinals are [0], [0,1], [0,1,2]. Accepted project ordinals 4,5,6 are genuine measured values (bootstrap excluded from N).

Parent mode loads the exact git-show parent store/coordinator and the exact parent list-history method; candidate mode uses the final reviewed product blobs. Every round gets a fresh daemon/realm. Order parent/candidate/candidate/parent. Per-request counters reset in finally. Two identical-key retries each run fresh verification and preserve the full original receipt. Daemons are then stopped/reopened on the same realm, and two fresh HTTP history reads each independently verify all three accepted entries once, including both retained sequential entries. These are daemon/service restarts in the same Python test process, not fresh interpreter timing claims.

Final origin assertions: Agent 840a58a70aa95fde504deac03b9e6c99a5f286ad, tree 552152726b9a144a4dc87b567aad606060860ef6, unchanged before/after every round. Candidate product SHA-256 matches changed-blobs.json and security-review.txt. Runtime synthetic snapshot f6bc318c0bfb1f907ddb9d7a062e8cd5f4ca9cf1, tree a32c3ec5fd312d4277c413c2080588bc340daee3; it includes temporary measurement launchers, removed from final worktree. No product source changed after measurement/review.

| Prior accepted N / commands | Parent full recorder replay | Candidate full recorder replay | Parent historical traversal | Candidate historical traversal |
| --- | ---: | ---: | ---: | ---: |
| 0 / 1 | 1 | 1 | 0 | 0 |
| 1 / 2 | 11 | 2 | 1 | 1 |
| 2 / 3 | 21 | 3 | 16 | 2 |

At N2, parent ancestor multiplicity is 15 and5, plus one new acceptance. Candidate is one for each ordinal4/5/6. Capture-document checks 144 ->32 and schema PreparedCommit checks17 ->3. Each retry verifies ordinal6 afresh once, with one historical traversal and12 capture-document checks; neither request borrows the previous request's result. Reopened history reads each verify ordinals4/5/6 once, with2 historical traversals, independently on both requests.

Second paired control wall seconds at N2: parent .618188/.672390; candidate .267843/.215665. Median .645289 ->.241754 (62.54% reduction). Thread CPU median .631588 ->.230940 (63.44% reduction). First paired control independently had wall .8212/.7068 ->.2658/.2547. Counts are instrumented without cProfile. First parent cold imports differ from later warm imports, so the first-request timing is not a paired cold-process claim. N and command count covary; no independent scaling law, flat-N performance, lock attribution, original P4 budget or App UI budget is claimed.

First central control: targeted-1024215006-7047, PASS1 in9.83s. Final restart control: targeted-1024215503-32580, PASS1 in12.63s. Exact launchers and private control are retained in evidence; canonical commands are in their central summary/log files and evidence scripts. Both temporary worktree launchers were removed.

## Validation and handoff boundaries

New focused tests cover scoped reuse with detached replies, direct calls, nested scopes/public API, concurrent thread isolation, failure retry and KeyboardInterrupt cleanup, cycles, source/event/metadata/ABI/record/ledger/owner mutations. Coherent source mutation passes fresh closure validation but fails recorder binding replay. All negatives stay strict. Final focused13 PASS; existing same-value/ABA undo controls3 PASS. Independent security review PASS, with243 independent auth/history/ABI/execution tests and final13 focused tests passing. Scoped Ruff47/47 and Pyright453/453 diagnostics are unchanged from parent (zero new); new test Ruff is clean. Compile/diffcheck passed. Exact commands, logs, exits and XML are durable in evidence.

The central broader16-file targeted union PASSED: 1038 passed in371.91s, exit0, with exact command/log/exit/XML in final-union.*. Central wrapper targeted-1024215213-683 PASS1 in372.53s. Its product blobs match final source; final13 request tests (including two subsequently added cases and Ruff import sorting) also passed in3.29s on final source. A first launcher attempt failed before pytest because central TMPDIR was unset; corrected launcher uses its pytest tmp_path. An early local union was interrupted before its socket cases and correctly moved to central service. Initial local implementation failures are retained in initial.log/XML; the undefined extracted document variable was fixed before the paired controls and successful runs. No failed run is counted as passing.

Next: normal orchestrator/reviewer release queue, then existing Agent/App submitters own original P4 ten-note45s and isolated element first, followed by their prescribed popup/parent and all8 P2. No duplicate original/browser/full run was launched here. Step2 outside-lock work is unimplemented and is not justified by this bounded control alone.
