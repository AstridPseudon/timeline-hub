# D118c occurrence2 own-node facts

Verdict: lower cause observed; no source, product, assertion, or input change applied.

The allowed test file remains byte-identical to `HEAD`, with SHA-256 `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f`. The full-file AST and target test-function AST match `HEAD`; both have 29 assertions. The authored invalid input remains `on: 1e308`, with the retained expected status `409` and reason `unsupported_timing`.

Both exact retained nodes were run independently with the authenticated `astrid` provider and the locally available released Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0` (tree `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`). Each private `generated_runtime` ran the established generator and manifest commands, including both `--check` invocations, with exit 0. The generated runtime key hashes match the selected Runtime source. A concurrent merge advanced the shared Runtime integration checkout during the work; the first exact run and the rerun use private generated-runtime hashes proving `42aad`, and the non-qualified intermediate `[True]` run is not used as evidence.

Observed lower cause for both nodes:

- outer pytest exit `1`;
- inner generated subprocess exit `1`;
- `RuntimeErrorBase` from `runtime_protocol.errors`;
- `_prove_birth` line 173;
- actual status `422`, reason `unsupported_timing`;
- safe detail keys only: `base`, `code`, `conflicts`, `current`, `hint`, `path`, `reason`, `status`, `suggested_command`.

The source/contract disposition is therefore an unapplied Agent/Runtime owner handoff: `occurrence.create` produces `unsupported_timing`; the current Agent classifier maps that unchanged-base failure to HTTP 422/`invalid`, and Runtime preserves the status. The retained test expects 409. No speculative correction was made. Later history, inverse, redo, retry, and no-write assertions are unverified because the retained status assertion is the first failure.

Evidence: `node-false.log`, `node-false.xml`, `node-false-trace.json`, `node-true-r42.log`, `node-true-r42.xml`, `node-true-trace.json`, and `facts.json`. The unqualified intermediate `node-true.log`/`node-true.xml` came from the concurrently advanced Runtime and is not part of the qualified result.
