## D33 whole-path report

Completed a read-only inventory; no product, wrapper, fixture, Store, or source changes.

First failure in service `...16002`:

- Exit `1`, empty log.
- `/home/user/work/venv-runtime/bin/python` was absent at the wrapper prerequisite guard.
- No inputs, fixture Git, Store, maker, verifier, or registration ran.
- No safety/permission refusal occurred.

Additional portability defect found:

- The archive omits `ops-child-custody/make-child-venv`; `support.py` resolves it relative to the archived path.
- The archive root also lacks `.git`, so the runner’s parent `git show` cannot work.
- Minimal fix: run source1747 from a real temporary Git checkout/worktree at the exact commit, with the maker sibling present.
- Bind runtime Python to `/home/user/work/venv-agent/bin/python`; it is Python 3.13.16 and has `build`, setuptools, and wheel. System Python lacks `build`.

Evidence:

- [wholepath.json](/home/user/work/wt/agt-OPS-inventory-E2E-wholepath-1816/evidence/wholepath.json)
- [prerequisites.json](/home/user/work/wt/agt-OPS-inventory-E2E-wholepath-1816/evidence/prerequisites.json)
- [source-manifest.json](/home/user/work/wt/agt-OPS-inventory-E2E-wholepath-1816/evidence/source-manifest.json)
- [validation.md](/home/user/work/wt/agt-OPS-inventory-E2E-wholepath-1816/evidence/validation.md)

Checks passed: `bash -n`, parser cases, Python imports, AST, JSON, hashes, artifact inspection, verifier equality, and `git diff --check`. No full suite or E2E retry was run. E2E remains unqualified pending the two wrapper binding repairs and one fresh service run.