## Report

Result: **FAIL diagnostic-mode fitness**; **PASS static normal-behaviour conservation**.

Finding: diagnostic mode calls `build(stage) → verify(stage) → seal(stage)`, but `STORE_VERIFY` runs without `--staging` and rejects writable paths. The staging root is created `0700`, so verification fails before retention can succeed. Probe confirmed: `unsafe or writable retained path`.

Evidence:

- Installed preimage: `e62f89eaf226897a36bd4c7f715d43a7a1d4206ff371432296c01de6bdd52dc3`, mode `0755`.
- Embedded `STORE_BUILD` and `STORE_VERIFY` hashes exactly match installed source.
- Default-off mode, opt-in grammar, duplicate/unknown/malformed argument refusal: PASS.
- Normal `Store.ensure` path remains present; no live runtime test performed.
- Receipt construction records actual verifier argv and excludes raw payload/credentials statically.
- `bench_store.py` and dependency-verifier hashes unchanged.
- No build, install, registration, reissue, provider, or test body run. Farm inputs remain intentionally unavailable.

Commands/results:

- `bash -n evidence/maker.sh` — PASS
- Embedded Python compilation — PASS
- Parser refusal probes — PASS
- Embedded block hash comparison — PASS
- Manifest JSON validation — PASS
- `git diff --check`; Composition worktree clean — PASS

Required next step: fix the seal/verify ordering or provide an explicitly reviewed staging-aware verifier path without weakening ownership checks, then repeat independent source review before any Farm build.

Commit message written and `DONE` marker created.