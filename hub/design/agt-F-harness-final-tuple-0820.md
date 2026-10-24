## Report

Implemented F-harness tuple rebinding in:

- `tools/run-discovery-original-0603.py`
- `tools/run-generic-reopen-original-0605.py`

Both now use:

- Agent `0c2c28da4f9733a1becc134f95219ae3079fc50e`
- Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06`
- Shared Store candidate `venv-agent-child-final-0c2c-becfe`
- Canonical client identity SHA256 `d79568df4fe4bed2a217b519d73824e8fd1ca17f61dfe0ce8492f1903764eb44`

Preserved original bodies, assertion counts, watchdogs, custody predicates, and source hashes. No wrappers or product files changed.

Validation:

- `python3 -m py_compile`: PASS
- `ruff check --no-cache`: PASS
- `mypy --cache-dir ... --follow-imports=skip`: PASS
- `bash -n` wrappers: PASS
- `git diff --check`: PASS
- AST predicate inventory/source-carrier hashes: PASS
- Bare `ruff --no-cache` is unsupported by installed Ruff 0.16.9; equivalent supported command passed.

Original runners were not executed because the genuine candidate is queued but not yet registered/qualified, as required. No full/browser/gate suites run.

Commit message written and `DONE` marker created.