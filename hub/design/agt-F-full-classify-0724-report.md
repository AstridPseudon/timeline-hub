# F-agent-full classification handoff — RUNNING

This is a durable progress handoff, not a completed classification.

| Field | Evidence |
|---|---|
| service | `agent-full-1023072419-4249` |
| requested | `2026-10-23T07:24:19Z` |
| last poll | `2026-10-23T08:11:43Z` |
| status | `running` |
| snapshot tree | `fcc33e0eb964dd48d422673e8f692f195c88748c` |
| Runtime commit | `a5d4258312c979024865ee704da2d632ca5b2730` |
| App commit | `890b9561666c3619f69335dd747b15e042b3a9a3` |
| Composition commit | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` |
| Runtime import source | Not exposed by live service files before terminal completion; configured `/home/user/work/runtime` via `PYTHONPATH` and `ASTRID_RUNTIME_CHECKOUT`, actual `runtime_protocol.__file__` unverified |
| command | `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -n 3` |
| progress | approximately 97% from the live pytest stream |

The live stream includes failures, errors, skips, xfails and `u` markers. Final node IDs, traceback/source evidence, totals and exit status are unavailable until completion, so every classification remains pending. Continue the same run; do not submit a duplicate.

No source, test, dependency, pin, filter, skip, xfail, V4 repair, executor or Git changes were made.
