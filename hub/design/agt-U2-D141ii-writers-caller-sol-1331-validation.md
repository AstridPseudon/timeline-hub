# Validation

Exact final two-selector command (selectors loaded from reviewed JSON as a Python argv list):

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141ii-writers-caller-sol-1331:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -n3 --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ii-writers-caller-sol-1331/evidence/targeted.xml --basetemp=/tmp/w-16bdf8c48c/basetemp -o cache_dir=/tmp/w-16bdf8c48c/cache 'tests/packs/timeline/test_verbs_working_copy.py::test_commit_conflict_names_the_writer_and_offers_discard_first[astrid.editor.timeline.5fb2249e000000000000000000000000-the editor published 5fb2249e after your checkout (rev-0)]' 'tests/packs/timeline/test_verbs_working_copy.py::test_commit_conflict_names_the_writer_and_offers_discard_first[authoring-parent-revision-38cecaa5ffffffffffffffffffffffff-someone published 38cecaa5 after your checkout (rev-0)]'
```

Result: **2 passed in 3.39s**, no failures/errors/skips; `targeted.xml` contains exactly IDs 12 and 13. An earlier caller run passed 2 in 3.30s; added exact command/base/current/no-write assertions passed 2 in 3.52s; final run follows Ruff import ordering and binds the trusted provider context hash to the actual generated POST body/path/publisher. No full or broad suite was run/requested.

Static checks (all PASS):

```text
/home/user/work/venv-agent/bin/ruff check tests/packs/timeline/test_verbs_working_copy.py
```

Exit 0. All checks passed!

```text
/home/user/work/venv-agent/bin/python -c 'import py_compile,sys;py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)' tests/packs/timeline/test_verbs_working_copy.py /tmp/w-16bdf8c48c/test_verbs_working_copy.pyc
```

Exit 0. 

```text
git diff --check
```

Exit 0. 

Ruff cache and compilation output were private under actual TMPDIR; no worktree bytecode or shared environment/cache write.

## Exact mypy and baseline

baseline, target default, cwd `/home/user/work/wt/agt-U2-D141ii-writers15-return-1319`; `MYPY_CACHE_DIR` pointed to `/tmp/w-16bdf8c48c/mypy-correct-baseline-default`.

```text
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py
/home/user/work/venv-agent/lib/python3.13/site-packages/numpy/__init__.pyi:737: error:
Type statement is only supported in Python 3.12 and greater  [syntax]
    type _Falsy = L[False, 0] | bool_[L[False]]
                                               ^
Found 1 error in 1 file (errors prevented further checking)
```

Exit 2.

baseline, target 3.12, cwd `/home/user/work/wt/agt-U2-D141ii-writers15-return-1319`; `MYPY_CACHE_DIR` pointed to `/tmp/w-16bdf8c48c/mypy-correct-baseline-3.12`.

```text
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports --python-version 3.12 astrid/packs/timeline/cli_native.py
Success: no issues found in 1 source file
```

Exit 0.

candidate, target default, cwd `/home/user/work/wt/agt-U2-D141ii-writers-caller-sol-1331`; `MYPY_CACHE_DIR` pointed to `/tmp/w-16bdf8c48c/mypy-correct-candidate-default`.

```text
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py
/home/user/work/venv-agent/lib/python3.13/site-packages/numpy/__init__.pyi:737: error:
Type statement is only supported in Python 3.12 and greater  [syntax]
    type _Falsy = L[False, 0] | bool_[L[False]]
                                               ^
Found 1 error in 1 file (errors prevented further checking)
```

Exit 2.

candidate, target 3.12, cwd `/home/user/work/wt/agt-U2-D141ii-writers-caller-sol-1331`; `MYPY_CACHE_DIR` pointed to `/tmp/w-16bdf8c48c/mypy-correct-candidate-3.12`.

```text
/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports --python-version 3.12 astrid/packs/timeline/cli_native.py
Success: no issues found in 1 source file
```

Exit 0.

The inherited product blob and pyproject.toml are byte-identical between the baseline worktree and candidate. Default mypy is **FAIL_ENVIRONMENT**, not source PASS: Python 3.13.16 runs mypy 1.17.0 with repository Python 3.11 target; installed NumPy uses Python 3.12 `type` syntax at __init__.pyi:737. The explicit 3.12 target is diagnostic evidence only; no shared/config change was made. An initial isolated single-file baseline lacked the repository import graph and was discarded; the reported baseline runs above use the complete inherited worktree read-only.

Disk trace: 163 samples at five-second intervals plus terminal samples; admission 4960673792 available bytes, minimum 4615389184 available bytes; 4 GB stop never crossed. Retained sampler stopped through its terminal session (exit 130).
