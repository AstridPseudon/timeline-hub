D127c corrected-source validation; no product/source/pin/App changes.

Functional evidence (one normal central request, no resubmission):

- Request command: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D127c-mounted-selection-sol-1935 targeted --files tests/test_p2_commit_phase_capture.py`
- Wait command: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-D127c-mounted-selection-sol-1935-targeted-1025194027-30318`
- Actual service command: `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py` — **61 passed in 3.62s**, exit 0, tree `8d5683702f36034f27ee7f49737665d66dbc2b75`.
- Permanent service log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-D127c-mounted-selection-sol-1935-targeted-1025194027-30318/log.txt`.
- Initial free bytes were 4,922,544,128 (<5 GB). New genuine structural selection/provenance nodes were authored first; red unit-body execution was NOTRUN below the local light floor. One corrected-file request was queued instead. No duplicate local run occurred when free space subsequently recovered. Prior candidate 20838/31-pass evidence was not used as corrected-source proof.

Static checks on the corrected exact two files:

- `/root/.local/bin/ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS, all checks passed.
- `/root/.local/bin/pyright tests/helpers/p2_commit_phase_capture.py` — PASS, 0 errors/warnings/information.
- `/root/.local/bin/pyright tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — 2 existing test diagnostics (pytest import, optional stop at line 78), 0 NEW; exit 1 is reported, not hidden.
- `MYPY_CACHE_DIR="$TMPDIR/mypy-cache" /root/.local/bin/mypy --follow-imports=skip tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — 2 existing test import diagnostics (pytest, test_timeline_commit_port), 0 NEW; exit 1. The helper's optional stats lookup is corrected by narrowing a separate callee_stats variable; no ignore/disable was added.
- `PYTHONPYCACHEPREFIX="$TMPDIR/pycache" python3.11 -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS.
- `git diff --check` and `git diff --check e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` — PASS.

Separate parent baseline:

The same exact two mypy/Pyright inputs were read with git show from e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9 into `$TMPDIR/parent-e319`, retaining tests/__init__.py. Read-only symlinks to the unchanged Runtime module tree and adjacent commit-port fixture reproduce the original import layout; no dependencies were installed/copied/modified. Baseline mypy with --follow-imports=skip reports exactly the same 2 import errors; baseline full touched-file Pyright reports exactly the same 2 test errors. An initial incomplete baseline overlay produced extra missing imports; restoring its package/import layout resolved those baseline-only artifacts. Raw baseline logs remain in private scratch; no checker was suppressed.

Preservation/source identity:

- Exactly tests/helpers/p2_commit_phase_capture.py and tests/test_p2_commit_phase_capture.py differ from 5747/e319. All outside tracked blobs were hashed and are unchanged; no untracked task source files.
- The full AST map is predicate-map.json: original c363950 has 160 behavioral predicates, 156 exact plus 4 pre-existing valid lifecycle migrations (lifecycle allowlist, failed->raised with buffer completeness, pending->pending_at_shutdown). All e319 test bodies, nested functions and all 183 whole-file assertions (181 inside tests plus 2 credential-helper assertions) are AST-identical. No skip/delete/xfail/weakening was introduced.
- Helper projection/schema functions, raw-output guard, stop/restoration and summary methods are AST-identical to 5747, except the projection's typed optional lookup. No cprofile field/version change.
- The final tree was independently calculated with Git blob/tree hashing without writing Git internals and equals the central test snapshot exactly. Final helper SHA-256: 095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d. Exact final commit SHA is deliberately pending harness exit, with an ordinary ref/source resolution recipe in source-manifest.json and attach-recipe.md.

Not run: full suites, browser/socket bodies locally, actual mounted element/provider/profile original body, native/full tours, acquisition, SWAP/WAL/recovery. No App test adaptation or final coupled independent review is claimed here. Those are the next gates; normal/home/body stays held.
