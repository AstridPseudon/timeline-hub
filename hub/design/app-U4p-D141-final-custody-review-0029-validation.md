# D141 final App source custody validation

Environment: Node `v20.20.0` via `/opt/node20/bin`; all checks were read-only.

Direct reviewer checks:

- `PATH=/opt/node20/bin:$PATH node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime` — PASS; pinned Runtime checkout matches.
- `PATH=/opt/node20/bin:$PATH node scripts/build/verify-astrid-vendor-sources.mjs` — PASS; 65 pinned closure files, 160 browser vendor files, 11 public imports.
- `PATH=/opt/node20/bin:$PATH node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --plan` — PASS; all proposed pin changes are no-ops and schema digest is exact.
- Read-only Git/blob/conservation check — PASS; Agent HEAD/tree and provenance commit/tree exact, 159 direct Git-blob hashes exact, zero source/vendor mismatches, 160-file set, two changed paths only, no outside paths, worker clean, and non-pin manifest keys conserved.

Durable author evidence independently read:

- `node scripts/astrid-landing/refresh-vendor.mjs ... --destination <private>` and normal destination — PASS; 160 files and private/default payload bytes/file sets equal.
- `node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs` — PASS, 6/6.
- Vendor/runtime Vitest bundle — PASS, 2 files and 17/17.
- Scoped ESLint — PASS.
- `git diff --check` and author direct conservation checks — PASS.
- Independent prior App source qualification — 89/89 tests, both TypeScript configs, lint PASS; reused unchanged per D141 policy.
- Independent Runtime source receipt — 119/119; reused unchanged per D141 policy.

An attempted private generator rerun was denied by the sandbox with `EPERM` when Node tried to spawn Git against `/home/user/work/agent`. It was not bypassed. This is an environment limitation, not a product mismatch; the author’s durable generator receipt plus the direct current hash/verifier checks are retained as the reproducibility evidence.

Not run or claimed: full/pristine/P1-P5/browser/live socket/child/build/ZIP/body/MAIN GO suites, or unchanged functional reruns.
