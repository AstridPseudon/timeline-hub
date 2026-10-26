# Validation

Read-only checks completed:

- The complete PLAN was read; P1 is the real-document and App queue-chain proof lane.
- Programmatic JSON load of `dispatch-recipes.json`, `dispatches[5]`: passed; selector `p1`, scope `original`, exact argv/cwd/environment/path fields.
- `sha256sum /home/user/work/app/scripts/testing/d66-plain-stack.mjs` and `git -C /home/user/work/app hash-object /home/user/work/app/scripts/testing/d66-plain-stack.mjs`: passed; `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f` and blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`.
- `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test`: passed; `9408dc44636db0e69ee64c59c373f5cd09cf7c82196a83167182227706d443cb`; its source line confirms `KEEP` is written before the request is queued.
- Programmatic recipe checks: both preflight/normal recipes have exactly 12 D66 pin fields; `TEST_KEEP` is not encoded in command text; command and LF-terminated row hashes match the original dispatch record.
- Raw result checks: preflight `31121` and normal `32161` request, snap, status, exit, `KEEP`, `ext`, trace-validation, manifest, XML, summary, and logs were read. Both status/exit pairs are `pass/0`; both snap trees match `6a6e49...d710`; both raw markers contain `D141hh p1`.
- Native trace recomputation: preflight 3 samples, minimum 5,061,656,576 bytes, maximum gap 2.110925033s; normal 42 samples, minimum 4,840,955,904 bytes, maximum gap 5.006692319s. Neither reached the 4GB stop.
- Pinned P1 source inspection: source hashes match the result manifest; complete assertions and tails were read without execution.
- `git diff --check`: passed; this worktree remains clean.

No product/full/browser/service/private-control/typecheck/lint test was run by this reviewer. The only test evidence cited is the original native service terminal and its retained artifacts.

Reviewer sampler: corrected foreground session `35987`, 5-second interval, 3 samples, explicit SIGINT, wait, and reap with exit 130. The first sampler shell invocation had a quoting parse error; no evidence was written by that failed command.
