## Report

Implemented the D21 observer-isolation harness under [`tools/timeline-d21-observer-harness`](</home/user/work/wt/agt-F-observer-harness-2355/tools/timeline-d21-observer-harness/launch.sh>).

- Removed inheritable `PYTEST_PLUGINS`/`PYTEST_ADDOPTS`.
- Added explicit parent/xdist `-p origin_plugin_2215`.
- Preserved the frozen full-body source exactly except for that plugin argument.
- Added immutable source/profile preflight and controller/`gw0`/`gw1`/`gw2` custody capture.
- No product, guard, registry, test, baseline, or pin changes.

Validation:

- Syntax/compile checks and `git diff --check`: PASS.
- Final cohort: `25 passed in 15.61s`.
- 150 observer reports: 50 setup, 50 call, 50 teardown; 25 call nodes, all passing.
- 29 nested subprocesses exercised: 17 expected nonzero and 12 expected zero; all assertions passed.
- Observer isolation: no nested observer records; exactly controller + `gw0`/`gw1`/`gw2` before/after records.
- Source/profile before/after custody: PASS.
- Evidence: 12 MB, below the 35 MB limit.
- Full suite was not run, per D21 instruction.

Pinned identities: Agent `f88cc5242d4b6c87b97a83878b86ec3168daa3db`; Runtime `8ea0766f5e9fb23cea26c7398770a8aaac06b258`; Python `venv-agent`; Node `v20.19.4`.

Candidate hashes:

```text
cohort-body.sh       f7625816e87714aeba2a334bcc36d7c3ea2e71f2538bc6774cacba02beba5e50
full-body.sh         4ee7a7ce7a341a59e516f737dcc7ddf3c1930b004fa2efb8b765f7e1a5a13a0b
launch.sh            260a0fc095edf3d3944fe485bae16f71366c5458b07f5b408f09d61a0bfc3845
origin_plugin_2215.py b1a52cad74f7b084c4267b32925aa591da7293b177ea88d4bbf6d1000e099080
preflight.py         7f50e7fba584b8fdcd84c30cd1318d97caf9b910c7c0cb86de003776d4edd25a
```

Future full-suite row is staged in `future-full-row.txt`; it was not added to the shared suite registry and was not executed. Commit message and `DONE` marker were created.