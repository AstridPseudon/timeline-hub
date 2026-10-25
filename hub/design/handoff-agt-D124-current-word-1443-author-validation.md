# D124/D107 source-only validation

- Normal head: `a4e016b6a9f91fbe372672bdcf382c630bf59186`.
- Donor source: `2e3331ee2f035e302f5ca52488832cd0e22bb3aa`.
- Donor/current test AST: identical after normalizing only the fixture import module name.
- Assertion count: 131 in donor and current.
- `pytest.raises` contexts: 5 in donor and current.
- The legacy M1 file, native fixture, Runtime fixture/archive, generated/client/schema/lock/store/host/emitter/installer files were not modified.
- No pytest, provider, Runtime service, socket, browser, P4, full, 95, original-ten, or core-425 run was performed.

Commands and results:

```text
PYTHONPYCACHEPREFIX="$TMPDIR/agt-D124-current-word-root-1428/pycache"   python3 -m py_compile   tests/editing_conformance/test_m1_current_equivalent.py   tests/editing_conformance/current_word_baseline_fixture.py
PASS

/home/user/work/venv-agent/bin/ruff check --no-cache   tests/editing_conformance/test_m1_current_equivalent.py   tests/editing_conformance/current_word_baseline_fixture.py
All checks passed!

python3 AST conservation script (donor 2e3331ee2f, 131 asserts, 5 raises)
PASS

git diff --check
PASS

git diff --no-index --check /dev/null <each allowed untracked file>
PASS (no whitespace diagnostics)

/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
Ruff findings: current=2143 baseline=2143
PASS

/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1902 baseline=1902
PASS
```

The first baseline attempts with system Python were not used: system Python lacked the installed `ruff`/`mypy` modules. No dependency installation was attempted.
