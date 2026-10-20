Implemented candidate freezing and capture-only inline submission so Runtime can validate before CAS publication. The SDK already forwarded the full candidate; the Runtime test adapter was omitting it.

- Final focused command: `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_capture_closure_source.py tests/sdk/test_visualize_authority_objects.py` — **28 passed, 2 strict xfails**.
- Both M1 import fences passed in the broader run. Its sole native-path regression was corrected and verified above.
- Ruff/diff checks passed. Mypy was blocked by installed NumPy stub syntax.
- All 12 forgery cases remain unchanged strict xfails. The 21 Runtime cases were collected only; paired execution awaits the projector metadata decision and reviewed sources. Visible UNCERTIFIED labels remain Viewing-owned. **M3 stays held.**

Exact commands, assertion inventory, blockers, and next steps are in [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-capture-candidate-forward/notes/report.md). Coordination docs, ledger rows, and both commit-message files are ready. No full suite or commit was run.