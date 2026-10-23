## Verdict: FAIL

The ClassVar/fixture-helper delta and canonical packet pass independently:

- Patch applies with `--fuzz=0`; replay and candidate are byte-identical.
- Final hashes match: patch `eadd855…`, manifest `d129fe3…`, fixture `3309a530…`.
- Core differs only by `ClassVar` import/annotation; caller is byte-identical.
- All 21 fixture bodies/assertions remain equivalent; completed run: **21 passed**.
- Ruff 0.16.8: baseline/result **3/3 inherited findings**, fixture **0**. Scoped `E,F --ignore E501`: pass.
- Compile, `bash -n`, `git diff --check`: pass.
- Runtime worktree clean; no live/full/browser/install operations performed.

Required installed-hash custody check fails for one file:

- `make-child-venv`: actual `33373 / c887a1…`; manifest records `32441 / 89d826…`.
- Other five installed hashes match.

I did not modify the shared install or manifest. Recommended next step: reconcile or freshly evidence `make-child-venv`, then rerun the six-file custody gate. `DONE` and the conventional commit message were written.