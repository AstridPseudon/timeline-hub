# Agent shared environment ready

The shared Agent dependency environment is ready for worker use.

- Python: `/home/user/work/venv-agent/bin/python`
- Python version: 3.13.16 (Linux)
- Source usage: run Agent commands with `PYTHONPATH=<Agent worktree>`; the
  environment contains dependencies only and does not install a worktree.
- Runtime dependencies: installed from the repository's hashed
  `requirements/runtime.lock`.
- Build dependencies: installed from the repository's hashed
  `requirements/build.lock`.
- Declared development tools: installed from `pyproject.toml`'s `dev` extra
  (without installing Astrid itself into the shared environment).
- Pinned source dependencies:
  - `runpod-lifecycle` at
    `db79345536985c701b7aff2eb5eec36667aae204`
  - `banodoco-timeline-schema` from `ArtAgents` at
    `242f9c4306bf3b501222cb041a9eb246ef47bc85`
- Import smoke: passed for the runtime modules exercised by the project,
  `pytest`, `pytest-cov`, `pytest-timeout`, `mypy`, `ruff`, `build`,
  `banodoco_timeline_schema`, and `astrid`.
- Missing dependencies: none observed in the import smoke.

Installation and import logs are outside the worktree under
`/home/user/work/wt/agt-m0-env-logs/`.
