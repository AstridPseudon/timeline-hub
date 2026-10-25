# Commands and results

All commands ran in `/home/user/work/wt/app-D118d-projection-identity-sol-1650`. No repository file was changed.

```sh
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py
```
Exit 0: `All checks passed!`

```sh
/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/sdk/test_timeline_capture_projection.py
```
Exit 0: `Success: no issues found in 1 source file`.

```sh
PYTHONPYCACHEPREFIX="$TMPDIR/pycache311" /usr/bin/python3.11 -m py_compile tests/sdk/test_timeline_capture_projection.py
/usr/bin/python3.11 --version
```
Exit 0; Python 3.11.17. An initial compile using the shared Agent venv's Python 3.13.16 also passed; it was followed by the required explicit 3.11 compile above. All bytecode caches stayed in private `$TMPDIR`.

```sh
git diff --check
```
Exit 0, no output.

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.11 "$TMPDIR/projection-preservation.py"
```
Exit 0. Read-only AST/hash/Git checks; writes only the requested small evidence JSON files in this worker's evidence directory. Output: 43 original assertions, 11 original test-function ASTs, 54 original fixture statements preserved; source unchanged; upstream target absent; D100 not an ancestor; Runtime clean. Detailed hashes/line mappings are in `predicate-map.json` and `source-custody.json`.

The script checked:

```sh
git merge-base --is-ancestor d3b5cfef76b4b3abef5db5f8288abc214a61354f HEAD
```
Exit 1: D100 is not an ancestor. `git show d3b5cfef76b4b3abef5db5f8288abc214a61354f -- astrid/sdk/timeline/_command_state.py` confirms the physical-membership implementation missing in HEAD.

```sh
git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_capture_projection.py
```
Exit 128: original fixture remains absent from the inherited upstream reference.

```sh
git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD 'HEAD^{tree}'
git -C /home/user/work/wt/rt-pin-5e9ad1c6 status --porcelain
git status --porcelain
```
Exit 0: Runtime commit/tree match `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` / `de2954a0ceadb4455903d9abdfec3b773318a50f`; both worktrees clean.

Own9: NOTRUN. Initial free space 4,913,999,872 bytes; later preservation-check free space 5,073,801,216 bytes. No causal test-source correction was possible, so an unchanged repeat was not authorized even after capacity recovered. No XML/log was created. Prior actual1646's exact9 results were read only: exit 1, nine setup errors, zero failures/skips, 16.26 seconds. No other test suites requested or run.
