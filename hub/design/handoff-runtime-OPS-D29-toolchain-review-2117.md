# PASS — OPS-D29 toolchain carrier review

Reproduced the committed fixture using the actual private requester, unchanged dispatcher, and patched maker.

Result:

```text
PASS cases=14 explicit=2 legacy=3 wrong-version/npm/path/missing/symlink/unsafe/extra/ambiguous=9 store=0 build=0
PASS actual requester -> unchanged dispatcher RUNTIME word-shape -> actual maker preflight
```

Checks passed:

- `patch --batch --fuzz=0`; deterministic `cmp` for both targets.
- Manifest target hashes and byte counts verified.
- `bash -n`, Python compile, JSON parse, `git diff --check`.
- Incomplete requester shapes 4/5/6 refuse before queue creation.
- Focused Ruff undefined-name lint passed.

Artifact hashes/bytes:

- Patch: `01c26c4b...763d4dd`, 5653 bytes.
- Manifest: `e7f0fe94...e3821e3`, 2960 bytes.
- Fixture: `9abe24db...1b56324`, 8675 bytes.
- Patched `make-runtime`: `873ddcfa...dd70149`, 28041 bytes.
- Patched `request-runtime`: `471fd470...b33b5f`, 2735 bytes.
- Preserved baselines: maker `99cca067...e9e4e28`; requester `f13a1d07...591f7b1`.
- Dispatcher preserved: `f18bc20b...8912c15`.
- Authorized child references remain disjoint; reviewed child hashes are requester `3b771253...c8aa33`, maker `c887a1bef...c404ff2`.

Default Ruff reports fixture style issues (EXE001/I001/PLW1510); no functional failure and no cleanup was made.

The approved App Node path is absent in this sandbox, so no real Node receipt, Store result, or build qualification is claimed. Known-version Node/npm files are bounded mocks only.

Correct fresh App command was recorded from the manifest and deliberately not executed. No queues, daemons, installs, builds, network, full suite, or product files were touched. Worktree remains clean.