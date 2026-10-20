Published [edit-recipe.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/edit-recipe.md), the schema artifact and executable hard-case spikes. Adopted Runtime’s frozen ABI 1; no product implementations changed.

Verification:

- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_recipe` — **14 passed in 157.21s**.
- `PYTHONPATH=$PWD ASTRID_RECIPE_R4_ROOT=/home/user/work/wt/agt-m0-spike /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_recipe/test_recipe_spikes.py` — **9 failed**, all blocked by missing `CheckAdmissionContext`.
- `/home/user/work/venv-agent/bin/python -m ruff check --isolated --select E4,E7,E9,F,I,BLE tests/m0_recipe` — passed.
- `PYTHONPATH=$PWD make check PY=/home/user/work/venv-agent/bin/python` — preflight blocked by absent `remotion/node_modules`.

The design documents each observed gap and required source change. Next: fix overlay admission, rerun its spikes, then obtain manager review. Live Runtime/App, pixel/audio parity and macOS remain unverified.

[Full report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m0-recipe/REPORT.md) and the required `commit-msg` are written.