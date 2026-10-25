Implemented D94a in the two allowed files. The cache now pins one SQLite connection, checks DB/WAL fingerprints inside read transactions and `BEGIN IMMEDIATE`, and retains one checked post-commit sample. Original authentication/boundary tests and prior evidence remain intact.

Validation:

- Central six-file acceptance: **246 passed, 74 deselected**.
- Local five-file run with `--timeout=45`: **242 passed, 74 deselected**.
- Final finite control: **2 passed**.
- Exact old-WIP race regression: **fails as expected**; candidate passes.
- Ruff **11→10**, Pyright **74→54**, with **zero added diagnostic identities**. `git diff --check` passes.

Forward accepts at N=3–22 stay at **286 SQL statements, 11 store decodes, one new-entry verification**, and 15 store digests after the first append. Warm reads stay at **27 SQL statements, zero decodes/digests**. Existing inverse ancestry costs still grow; this is **not full P4 qualification** or exclusive CPU accounting.

The protection premise remains **unverified**. Actual integration code paths `/home/user/work/runtime` and `/home/user/work/runtime/runtime_protocol` are UID/GID **0:0**, mode **0755**; the module is **0644**. Production data-root ownership/mode is unknown: no override, existing default root, or running CLI declaration was found. No broader trust trade was assumed.

Exact identities:

- Parent: `43407a1820116b73b4db014b938872534eeeeb5f`
- Candidate tree: `6a0db1ec092cf1631761fd4bbc8a0ae33eebeec8`
- Store blob: `dc7035cd7e3669a304d87e745b5743ee8cf41236`
- Test blob: `7c764726443d813145dd7caf05ffb2f74e4b40da`

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D94a-history-state-sol-0348/evidence/commands.txt), XML, curves, origins, and diagnostic comparisons are retained under the worker’s evidence directory. Artifacts total **9.13 MiB**. Commit message and `DONE` are written; commit SHA awaits the harness.

Next: independent security review covering the D94a race, external writes/WAL/rewind/restart/legacy mix and retained forgery witness, plus orchestrator disposition of the deployment protection premise. No release approval is claimed.