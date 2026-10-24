## Report

Implemented harness-only PATH qualification in [tools/run-render-cohort-0013.sh](/home/user/work/wt/agt-F-render-node-five-0031/tools/run-render-cohort-0013.sh).

- Added pinned Node bin to parent/child `PATH`.
- Preflight now resolves and reports `node`/`npx` paths and versions.
- Added strict five-node selection; original 21-node evidence remains preserved separately.
- No product, test-body, pin, dependency, or profile changes.

Checks:

- `bash -n tools/run-render-cohort-0013.sh` — passed.
- `git diff --check` — passed.
- Central targeted run `...1024003218-10359`:
  - 5 selected; 4 passed.
  - 1 failed by existing 45-second timeout: `test_threejs_support_rejects_unsupported_timelines_with_clip_reasons`.
  - No body retry performed.
- Prior preserved run remains 16 passed / 5 failed in 289.20s.
- Pre/post custody, source origins, profile fingerprints, Runtime `8ea0766f` / tree `6047ac3`, and Node `v20.19.4` / npx `10.8.2` verified.

Remaining timeout is unclassified; no renderer fix was attempted.