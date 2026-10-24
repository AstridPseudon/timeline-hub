SOURCE FAIL — independent review of `07b3f277a`.

The focused tests passed:

- 5 new installed-root tests.
- 7 existing fence/admission security tests.
- Vendor lock, artifact manifest, and `git diff --check` passed.
- Actual origins: Agent from this worktree; `runtime_protocol`/`astrid_runtime` from Runtime `8ea0766f`.

Security failures found:

- `invoke_capability()` trusts caller-supplied `source_roots` and recomputed digests. A forged admission redirected execution to an arbitrary foreign root and reached launch.
- A genuine admitted pack containing a symlinked module outside the pack also reached launch.
- Passing the admitted root through `PYTHONPATH` permits a top-level external `astrid` package to override the installed package.
- The child launch uses `sys.executable -m ...` without the installed `-I` isolation shape, so installed-runtime guard coverage is not preserved/proven.

Scoped quality checks remain unqualified: Ruff reports 101 existing-file diagnostics; Mypy is blocked by a dependency `.pyi` using Python 3.12 syntax.

The original installed positive was not rerun; it remains pending/unqualified after the author’s pre-provider `runtime_protocol` import failure. No product files were modified; worktree is clean.