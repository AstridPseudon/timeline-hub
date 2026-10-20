Implemented the fixture-only fix.

- Replaced nested `pytest_plugins` with direct `host_project`/`native_host` fixture imports in [conftest.py](/home/user/work/wt/agt-tests-sprite-global-fixture/tests/packs/rendering/conftest.py).
- Global collection: `15,213/15,906` collected, `693` deselected, exit 0.
- Renderer-peer xdist suite: `32 passed` in 107.14s.
- Ruff and diff checks passed.
- No Sprite or host tests/assertions changed; no full suite run.

Handoff artifacts:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-tests-sprite-global-fixture/report.md)
- `commit-msg.txt` written
- `DONE` marker created