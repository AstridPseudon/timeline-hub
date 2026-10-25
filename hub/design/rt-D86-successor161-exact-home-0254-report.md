# F-D86 report

Completed successor161 exact-home harness work. No Runtime source/test changes; worktree is clean.

- Bound manifest to exact checkouts, preserving all four SHAs:
  - Agent `cef8a5be...` → `/home/user/work/wt/agt-pin-cef8a5be`
  - Runtime `6634a17f...`
  - App `c1014775...` → `/home/user/work/wt/app-pin-c1014775`
  - Composition `635f4de0...`
- Updated private path-sensitive manifest, aggregate, and import origins only. Source hashes, selectors, schema, and profile values remain unchanged. The P4 aggregate hash changed only because absolute paths are hashed.
- Preserved 161 selectors, original 550 rollup rows, and 23 no-JUnit dispositions.
- Positive/poison controls passed: positive exit 17 with one body call; poison exit 1 with zero calls.
- Corrected sampler 0242 ran first as required; central result was terminal failure without duplicate submission.

Central successor161 run:

```text
request-test integration:agent fd86-successor161
request id: agent-fd86-successor161-1025025816-9211
```

Route used `-m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`; no unintended `-m integration`.

Results:

- Preflight: exit 0
- Body: exit 1
- 161 testcases: 6 passed, 43 failed, 112 errors
- All 161 per-ID outcomes are durable in `per-id-outcomes.tsv`
- XML, logs, argv, manifest/runmanifest, receipts, import hashes, profile, and registry evidence are under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D86-successor161-exact-home-0254/evidence/fd86-successor161-exact-home/output`

Validation commands passed:

- `bash -n` on launch scripts
- `py_compile` on launcher installer
- AST/source preflight: all 161 selected functions hash-matched
- XML count assertion: exactly 161 testcases
- Registry restore: byte-identical to pre-run hash `a42da904...`
- Evidence size: 11 MB
- `git diff --check`

No local pytest or full suite was run. No additional verdict was added. D91 was not submitted by this worker.

Commit message recorded and `DONE` created.