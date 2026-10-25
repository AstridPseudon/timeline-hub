# D118d commands and results

Working directory: `/home/user/work/wt/app-D118d-projection-setup-sol-1606`.

```sh
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py
```
PASS, exit 0: `All checks passed!`

```sh
/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/sdk/test_timeline_capture_projection.py
```
PASS, exit 0: `Success: no issues found in 1 source file`.

```sh
PYTHONPYCACHEPREFIX="$TMPDIR/pycache" /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py
git diff --check
```
PASS; no compilation or whitespace diagnostics. Final `git diff --check` also exit 0.

Source verification used an inline `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python` command with Python ast/hashlib and read-only Git subprocesses. PASS, exit 0: original assertion multiset retained (43); base assertion multiset identical (44); test-function AST dictionaries identical (11); every original saved_closure statement retained as an ordered subsequence; canonical reader field tuples identical; only assigned file changed; upstream target absent; exact Runtime pin/tree and empty porcelain verified. Recorded hashes rechecked after the gate.

```sh
git rev-parse HEAD HEAD^{tree}
git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD HEAD^{tree}
git -C /home/user/work/wt/rt-pin-5e9ad1c6 status --porcelain --untracked-files=all
git ls-tree 92443771676ef2bbb547d0a103d708fa8bec4c63 -- tests/sdk/test_timeline_capture_projection.py
```
PASS: Agent HEAD e02180cedafa581bc8105d77341456b8b1c50b5b, tree b83fcf6cbb2b9bd8620a8b203ba8d0419fa8c354; Runtime HEAD 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344, tree de2954a0ceadb4455903d9abdfec3b773318a50f, clean. Upstream ls-tree empty (target absent).

Exact authorized own9 command (NOTRUN):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-setup-sol-1606/evidence/own9.xml tests/sdk/test_timeline_capture_projection.py::test_real_saved_projection_config_registry_and_full_pins_golden tests/sdk/test_timeline_capture_projection.py::test_real_saved_entire_expansion_golden tests/sdk/test_timeline_capture_projection.py::test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[parent]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[child]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[new_shot]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[duplicate]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[remove]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]'
```
Fresh disk gate measured with `shutil.disk_usage(os.environ['TMPDIR']).free`: 4,987,809,792 bytes, 12,190,208 below required 5,000,000,000. No pytest subprocess started. No XML/log exists. No repeated failed nodes or alternate Runtime used. Ongoing 4 GB stop was not reached because dispatch was refused by the required disk admission gate.
