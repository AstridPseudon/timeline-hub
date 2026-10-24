Added [the F-D40 harness](/home/user/work/wt/agt-F-D40-observer-sol-0540/tools/run_d40_installed_observed.py). It retains its exact source before execution and observes the real return through a profile hook without replacing the production callable.

SHA-256: `3cfefd6a72bec379897b80745c91ecdcfa5358c42d7f59afd826adbc3e5e1630`

Stage A passed under installed child `3b5c` with `python -I`:

- Six synthetic checks covered forwarding, object identity, exceptions, durable logging failures, origin logging, and iterator non-consumption.
- All 2,053 product/test Python files remained unchanged.
- Syntax, retained-source equality, Ruff, and whitespace checks passed.

Exact preflight argv and results are retained in [preflight.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-observer-sol-0540/evidence/stage-a-final/preflight.json), alongside source bytes, stdout, stderr, and exit `0`.

Additional commands passed:

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache tools/run_d40_installed_observed.py
git diff --no-index --check /dev/null tools/run_d40_installed_observed.py
git diff --check
```

No original body, host subprocess, probe, or full suite ran. The old `1 passed in 3.32s` / three-assertion result remains immutable and caveated as **result-only**; complete installed custody remains open.

Next: independent Luna review, then manager-dispatched Stage B. Commit message and `DONE` were written.