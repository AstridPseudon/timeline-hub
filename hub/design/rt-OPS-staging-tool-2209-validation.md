# OPS staging candidate validation

Source-only candidate; no live installation, publication, real worker cleanup,
network acquisition, full suite, browser, provider body, or git operation was
run.

Commands and results:

```text
python3 -m py_compile ops-drop-staging/drop_staging.py ops-drop-staging/drop-staging ops-drop-staging/test_drop_staging.py
PASS

python3 ops-drop-staging/test_drop_staging.py
PASS — 8 tests, 0 failures

/home/user/work/venv-agent/bin/ruff check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py
PASS — All checks passed

git diff --check
PASS
```

The unittest invokes the executable `ops-drop-staging/drop-staging` through
private temporary worker fixtures. It covers archive-first success, forced
low-disk fallback, durable fallback logging, idempotent repeat refusal,
archive collision, running/not-ended workers, missing and bad evidence
manifests, manager lease, outside/traversal/evidence-overlap paths, symlink
target/descendant, and KEEP protection. Fixture cleanup is confined to the
test temporary directory.
