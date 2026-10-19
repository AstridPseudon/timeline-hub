# Agent baseline — 2026-10-19

Environment: `/home/user/work/venv-agent`, dependencies only (no editable/source install), Python3.13.16. Initial source main `e51595c6`. Linux only; macOS/live lanes not run.

| Command / check | Recorded outcome |
| --- | --- |
| `make check` | Blocked at locked Remotion prerequisites: exact Node20.19.4/npm10.8.2 still hits GitHub2rp v0.1.1 tarball403. Later typecheck/parity did not run through this command. |
| `python -m pytest -q tests/editing_conformance` |179passed,4existing parity skips in19.72s. |
| Original default `PYTHONPATH=$PWD .../venv-agent/bin/python -m pytest -q` | Orchestrator stopped the original run near87%; no final count, no pass claimed. Do not restart/repeat it. |
| Central replacement `agent-full-1019191532-6465` | RUNNING, source snapshot includes main plus reviewed Viewing labels (`a6502806`); orchestrator designated this as baseline result. Exact command/tree/footer in central result directory. Counts pending. |
| Independently run structure/docrefs/ruff/cycles at initial main | Passed; detailed evidence in agent-review-notes.md. |

Doctor's hermetic subprocess drops checkout PYTHONPATH and uses a temporary cwd; dependency-only shared env has no installed Astrid. Main CI uses an editable install, so this is a setup limitation, not a proved product regression. Mypy in this Python3.13/NumPy2.5.2 environment fails parsing NumPy stubs under target3.11; main CI Python3.11 lock chooses NumPy2.4.6. Missing YAML stubs also reproduce on untouched main. Do not attribute these to the port or report those gates green.

M1 results are separate from this baseline: normal-source focused233pass and actual central CLI/Python commit path3pass18.51s are recorded in agent-review-notes.md. The ONE merged full request is agent-full-1019193420-11899, queued behind the original baseline; it is not a baseline rerun or a full-green claim. New source failures will be compared against exact baseline evidence when available.
