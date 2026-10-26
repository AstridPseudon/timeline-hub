# D141cc single-controller validation

Selector: `p2-transition-none-single@original`  
Normal suite: `full-d141-p2-transition-none-single-82e9e13d-submit`  
Status: `NOTRUN_CUSTODY` / no body verdict.

- Plan and accepted Sol packet read from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/dispatch-recipes.json`: PASS; dispatch index 2 selected.
- Read-only candidate custody inspection immediately before submit: PASS, `FIRST_NATIVE_INVOCATION_ONLY`; no prior request, artifact, lock, or registry row.
- Admission measurement immediately before submit: `5642002432` bytes observed, above 5.2 GB.
- Four exact detached source pins: PASS; all HEAD/tree pairs and clean detached statuses recorded in `source-manifest.json`.
- Builder SHA/blob: PASS for `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f` / `59b65214bc74c1ca118b097bc3b13c0ffe480a93`.
- Native invocation count: exactly one.
- Native invocation result: exit 1 before request registration. First error: `D66 source selection: D66 agent source does not match its submit-time pin: selected ecdc242ed9b673f641759ecf029f95e89a2c6f92/d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735, pinned ecdc242ed9b673f641759ecf029f95e89c2a6f92/d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`
- Post-return custody inspection: no request ID, no normal artifact, no lock, and no registry row. No `wait-test`, `stop-test`, or retry was authorized.
- The initial wrapper attempt had a controller path typo and stopped before native execution; the only native invocation then failed on the recorded agent-SHA typo. This is retained as an operational first error, not repaired.
- Product tests/types/lint/full suite: N/A and not run; no product/source/pin/registry/queue mutation.
- Sampler: retained direct session 44814 wrote `disk-trace.txt`, then was stopped/waited/reaped. First-tool direct-trace coverage is explicitly not claimed because session 22332 initially emitted supplemental stdout only.
