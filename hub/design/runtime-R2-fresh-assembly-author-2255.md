Implemented the production repair in `timeline_commit_store.py`: each lookup builds one dependency graph, runs every node’s fresh authentication checks, then verifies replay proofs in dependency order. Every subsequent lookup rebuilds the graph, including within the same request. Cycles and rows changed while queued refuse.

Matched controls used the supported film fixture and a real Agent preview calling `RequestCommitPort.history_entry`:

| Recorded entries | Checks old → new | Old wall/CPU | New wall/CPU |
|---:|---:|---:|---:|
| 2 | 2 → 2 | 0.023/0.011s | 0.010/0.010s |
| 4 | 8 → 4 | 0.038/0.038s | 0.074/0.074s |
| 8 | 128 → 8 | 0.677/0.583s | 0.070/0.066s |

Deterministic replays remained 2/4/8. N=8 closure reads fell 256 → 16. These measurements cover one history lookup; continuation edges and event-prefix work can still grow with history.

Validation on final source:

- Required files and new regressions: **193 passed**.
- Authentication/ABI/history neighbors: **192 passed**.
- Finite comparison: **3 passed**. The unchanged multiplicity assertion failed on baseline at N=4.
- Central daemon restart/exact retry: **1 passed**.
- Ruff **zero new findings**; Pyright **zero new findings**; compile and `git diff --check` passed.

Controls cover same-request and cross-request mutation, ancestors/parents, events/metadata, physical files, rewind/fork/ABA, deferred-row corruption, cycles, threads, reopened retry, and all ten lock-placement cases. Exact commands, environments and durable results are in [commands.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-fresh-assembly-sol-2240/evidence/commands.json).

One independent Luna source review found no confirmed blocking regression. Its caveat is the read-to-replay race for external DB/CAS writers bypassing Runtime’s mutex; no atomic DB/filesystem snapshot is claimed.

Base: `732c48c6f5a9441a65c61b24595d454a1cd3e180`. Production file SHA-256: `4fbac66eb878a4aa09f4dd3050d81e536b2793628adff00a86a76e1d7e78bfe5`. Agent: `7c485e5b612a31a9b4f6e9a67163612a4a3313d4`.

Commit message and `DONE` written. Nothing blocked. **Original P4 timing remains pending**; next step is integration followed by the receiving Agent’s original run. No full suite, original body, profile or stacks were run.