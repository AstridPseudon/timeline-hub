# G5 native-port first return — source fidelity correction

Draft only; P1/G5 remains NO-GO.

Source author `3996822a009d8d7393630ef4920ca6c59410e00f`; normal CLI source
interface consulted at `cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6`. Product
blobs were not duplicated or imported.

The two scoped corrections are:

1. The fake history/reopen adapter now retains the accepted provider receipt,
   exact canonical previous pair, request-derived label/steps/merge metadata,
   command records, inverse `undo_of`, and bootstrap row. It uses actual
   generated response/request identities rather than empty items or guessed
   pins.
2. `test_normal_commit_conflict_keeps_head_and_has_no_force_overwrite` now
   drives the normal CLI `show`/`edit`/`apply` route and retains conflict,
   head/history/no-write, and force-refusal predicates.

The exact four scoped blobs and hashes, commands, source identities, and
pending seven behavior reds are recorded in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-native-ports-return-1538/report.md`

Evidence: 87 collected; three representative tests passed in 9.32s;
compileall, scoped Ruff, scoped mypy, and diff-check passed. The current
branch still lacks the product `--commit` parser, so accepted redo remains
pending that join; detached duration remains pending its separate product
owner. No full suite or seven-red rerun was run.
