# P4 current-five test import

## Result

Imported exactly five test files on base `ecea7d8563c93059283ef9475ecb41a37e628a38` (`tl/agt-G3-corrected-current-0259`):

- `tests/sdk/test_p4_commit_v2.py` — donor commit `2d21a98919767016b5ff32a37c2ee207ec1c31fe`, blob `85218e8e99a1c7602d2b7ee399f3847fac759186`
- `tests/sdk/test_p4_ten_note_provider.py` — donor commit `e7385882ef50a59e6f62f32058fe211eb6e0b69f`, blob `1ed257c4604552793d2eaabfc117babe93c5b445`
- `tests/sdk/test_p4_note_rerun.py` — donor commit `755d6e7a4a179e74ce5ed497edab88e8b7a292af`, blob `80c15e2944b5660a18077aa38f84cf3b3ced09bb`
- `tests/sdk/test_p4_cli_sheet_v2.py` — donor commit `fe781e4d2cf267994d655dc57320448dddd5d708`, reviewed packet `f4f40fe7d7d018b72b55ec719876f64527f835e7`, blob `fd248182a0e1c120fa6440994da545c4e13219ad`
- `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — proof donor `ddff86c18b8f8eef2092715d7804f8b50f2ef39f`, blob `05f7aa2bd862fc608ee17515d373c5f5b47c27eb`

All five current blob IDs exactly match the donors. No assertions, skips, xfails, production, generated, lock, schema, or other tracked files changed. Worktree status contains only the five requested untracked test files.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py` — **15 passed in 9.61s**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration --collect-only -p no:cacheprovider tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — **1 test collected in 1.07s**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — **All checks passed**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /tmp/astrid-u2-typecheck/bin/python -m mypy tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — **Success: no issues found in 5 source files**
- Final delta audit: tracked diff from base **none**; whitespace checks **clean**; protected-path audit **clean**; all five donor blob checks **MATCH**.

## Decisions and boundaries

- Used the reviewed four-file packet tree from `f4f40fe7d7d018b72b55ec719876f64527f835e7` and the separate Runtime proof donor from `ddff86c18b8f8eef2092715d7804f8b50f2ef39f`.
- No old Proof product ancestry was merged; the Runtime HTTP test was only collected, not executed.
- No full, browser, Runtime P5/native14, HTTP-body, farm, install, or shared-dependency suite was run.
- No blockers. Recommended next step: independent delta review, then home import/merge after the G3 source is accepted.

