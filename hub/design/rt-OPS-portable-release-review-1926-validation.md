# OPS portable final independent source review

Verdict: **PASS** for the requested independent source/unit review. The source
is not genuine E2E GREEN: the Agent-only whole-maker run remains **NOTRUN** and
installer1826 stays held until that run and its independent result review pass.

## Exact final source

Reviewed commit `60753548ebc8e69f3c84fbb28fa2e09b1ca78316`, tree
`dd4347a933103bbfc17c3e3237d52ea13ac1f677`, parent
`2fffe593175338ffb8144705bb70c9542fa4459f`. The final diff contains only
`ops-child-custody/tests/e2e_inventory.py` and
`ops-child-custody/tests/test_e2e_inventory.py`. Runner SHA-256 is
`c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e`;
`support.py` is `e85b42ac7ffff730166443ed7d081a1a68062b828af3aa5d8e0dd9352afb6581`.

Independent hash/mode checks pass for parent maker0857, candidate makerc3226b,
protected Store helper123bb, dependency helper116b, bootstrap artifact443977,
the tiny manifest, and all manifested source files. The two maker verifier
blocks are byte-identical with hash `f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209`.
The complete manifest retains the four required roles and exact required source
file sets, dependency wheel pins, maker paths/hashes/modes and commit fields.

The final source keeps `suites.conf` creation before both unchanged
`Store.initialize` calls, retains bootstrap-artifact staging in
`prepare_venue`, and leaves the immutable reserve `5905580032` and stop line
`4000000000` unchanged. AST comparison confirms `prepare_venue` and
`run_venue` are unchanged from the parent. No maker, verifier, Store API,
source guard, admission, Git mutation, or production trust path changed.

## Finding disposition

All seven finite findings are mapped and fixed: 1903’s Ruff failure and early
malformed-role exception; 1909’s malformed wheel-role shape, maker-path type,
missing required source roles, ambient `python3`, and TMPDIR writability.
Malformed roles, paths, hashes, modes, source files and manifests accumulate
independent failures while valid entries remain authenticated. This is explicit
validation, not a broad catch or a skipped source guard. The actual-component
helper/maker checks pass read-only, and the original 42 controls remain exact.

## Commands and results

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ops-child-custody/tests /home/user/work/venv-agent/bin/python -m unittest -v ops-child-custody/tests/test_e2e_inventory.py ops-child-custody/tests/test_custody.py ops-child-custody/tests/test_inventory.py
exit 0; Ran 64 tests in 6.949s; OK

/root/.local/bin/ruff --version
exit 0; ruff 0.16.8
/root/.local/bin/ruff check --no-cache ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py
exit 0; All checks passed

/home/user/work/venv-agent/bin/ruff --version
exit 0; ruff 0.12.0
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
exit 0; All checks passed

bash -n ops-child-custody/make-child-venv
exit 0
PYTHONPYCACHEPREFIX=/tmp/w-df218d2590/portable-final-review-check/pycache /home/user/work/venv-agent/bin/python -m py_compile ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py ops-child-custody/tests/test_custody.py ops-child-custody/tests/test_inventory.py ops-child-custody/tests/support.py
exit 0
AST parse of all five test Python files
PASS

/root/.local/bin/pyright ops-child-custody/tests/test_e2e_inventory.py
exit 0; 0 errors, 0 warnings, 0 informations
/root/.local/bin/pyright ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py
exit 1; exactly the same five pre-existing diagnostics recorded by author1908

git diff --check 2fffe593175338ffb8144705bb70c9542fa4459f -- ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py
exit 0
git diff --check f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe -- ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py
exit 0
git diff --check f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe
exit 2; only the disclosed frozen maker EOF diagnostics at candidate:1224 and parent:1201
```

## Direct check-only result

The actual final CLI was run with the real protected helper, bootstrap artifact,
Agent venv runner/build interpreter and physical `/usr/bin/python3.13`, but
missing private carrier/wheel inputs. It exited **2** and emitted a complete
structured census. The 11 missing labels were the private wheelhouse path,
the Agent and Runtime carrier paths, their two Git-history entries, the five
local wheels, and the unchanged start reserve.
`ok=false`; `mutating_setup_started=false`, `maker_started=false`,
`store_initialized=false`, and `git_mutated=false`. Source, maker, helper,
interpreter, command, path, and verifier checks were still traversed.

No genuine receiving prepare, Store initialization, Git carrier creation,
wheel build/acquisition, package installation, child request, maker body,
network/socket/browser/profile, production Store, or D130 action was run.
Final `df -Pk` available space is `4476448` KiB (about4.58GB), below the
unchanged source floor and `5905580032`-byte reserve; heavy work remains
unspent and available space remains above the `4000000000` stop line.

Historical frozen EOF bytes are intentionally disclosed; they are not part of
the authored final diff. No full suite was requested.
