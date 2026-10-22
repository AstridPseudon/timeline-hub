# U2 private typecheck environment

## Result

Environment repair is solved privately. The unchanged `make mypy` gate now runs
to source diagnostics in a valid Python 3.11 environment; it is not whole-gate
green because the unchanged source has 41 findings over its committed baseline.
No repository files, tests, config, pins, shared venvs, runtimes, or node_modules
were modified.

Private environment:

- Interpreter: `/usr/bin/python3.11` (3.11.17)
- Environment: `/tmp/astrid-u2-typecheck`
- Private uv cache: `/tmp/astrid-u2-uv-cache`
- Private mypy cache: `/tmp/astrid-u2-mypy-cache`
- Installed versions: `mypy==1.17.0`, `numpy==2.4.6`, `PyYAML==6.0.3`,
  `types-PyYAML==6.0.12.20260906`, `mypy-extensions==1.1.0`,
  `pathspec==1.1.1`, `typing-extensions==4.16.0`

The NumPy choice follows `requirements/runtime.lock` / `requirements/proof.lock`:
2.4.6 for Python `<3.12`; 2.5.2 remains the declared branch for Python `>=3.12`.
`types-PyYAML` is absent from the repository declarations, so it was added only
to this private typecheck environment and was not pinned in source.

## Exact gate

Run from `/home/user/work/wt/agt-U2-quality-env`:

```sh
MYPY_CACHE_DIR=/tmp/astrid-u2-mypy-cache \
  make mypy PY=/tmp/astrid-u2-typecheck/bin/python
```

Result: exit `2` from the Make target. The checker completed and reported:
`Mypy findings: current=2020 baseline=1979`; then
`ERROR: Mypy regressed by 41; fix the new findings.`
There were no missing-stub, incompatible-NumPy syntax, or interpreter setup
errors. This is the expected source-baseline failure and remains visible.

The environment was built without changing the repo:

```sh
UV_CACHE_DIR=/tmp/astrid-u2-uv-cache uv venv \
  --python /usr/bin/python3.11 /tmp/astrid-u2-typecheck
UV_CACHE_DIR=/tmp/astrid-u2-uv-cache uv pip install \
  --python /tmp/astrid-u2-typecheck/bin/python --index-url https://pypi.org/simple \
  mypy==1.17.0 numpy==2.4.6 types-PyYAML==6.0.12.20260906 PyYAML==6.0.3
```

## G2 validation

Validated committed G2 `63f7b4c21` in a temporary `git archive` snapshot of the
G2 tree, without mutating the G2 worktree. The exact declared-config command
was recreated and run as follows:

```sh
G2_SNAPSHOT=/tmp/astrid-g2-source-63f7b4c21
mkdir "$G2_SNAPSHOT"
git -C /home/user/work/wt/agt-G2-open-commit archive --format=tar \
  63f7b4c21 | tar -x -C "$G2_SNAPSHOT"
cd /tmp/astrid-g2-source-63f7b4c21
MYPY_CACHE_DIR=/tmp/astrid-u2-g2-mypy-cache-final \
  /tmp/astrid-u2-typecheck/bin/python -m mypy \
  astrid/sdk/timeline/commit_session.py \
  astrid/sdk/timeline/__init__.py \
  astrid/sdk/timeline/api.py \
  astrid/sdk/timeline/sync.py
```

Result: exit `0`, `Success: no issues found in 4 source files` (only the normal
`annotation-unchecked` notes for untyped function bodies). The temporary source
snapshot was removed after validation.

For separation from the declared gate, the prior report's additional
`--check-untyped-defs` variant was also run over those four files. It found one
source diagnostic in `sync.py:159` (`TimelineSession` has no attribute
`_explicit_outbox`); that flag is not in `pyproject.toml`'s declared checker
rules, so it was not suppressed or used to claim gate success.

## Checks and decisions

- Shared `/home/user/work/venv-agent`, `venv-agent-child`, and
  `venv-agent-child-s2` were inspected read-only; all are Python 3.13.16 with
  NumPy 2.5.2 and no `types-PyYAML`.
- System Python 3.11.17 was the existing compatible interpreter; no Python
  target or repository dependency declaration was changed.
- The supported uv/PyPI path succeeded using the configured proxy/CA path.
- No full, browser, renderer, or live-socket suites were run or requested.
- Final worktree status is clean.
