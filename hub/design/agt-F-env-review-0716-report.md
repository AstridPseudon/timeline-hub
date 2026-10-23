# F-agent-full environment repair review

ENVREPAIR PASS. CLASSIFICATION PASS. FULLRESULT FAIL/collection-blocked.

Exact one-row diff in ORCH/tests/suites.conf:
    -agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3
    +agent       full              env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -n 3
Captured blob IDs ef20cd75184faed72b9b6c1a995c80916b660fed -> a6d37acb6882ab1285088c0be39f495b7e39f36f; current blob is the post-image and SHA-256 is bf596aaddb68152b8ad25ed1b179bc5b7c23269464d6a0928e8955d65c5625b7. DB dry-run confirms no suite row was added.

Agent 4edc4b321cae5cfc58252d7ed89e3f0408238646 tree f17b84c48bae3461dd11cedb8719bd17495a8210; Runtime a5d4258312c979024865ee704da2d632ca5b2730 tree f74b016ea837f8148db4a602c972073a226ed177.

bash -n, exact command/no-filter assertion, and import preflight: PASS. Imports resolve to the review Agent tree and /home/user/work/runtime/runtime_protocol/__init__.py. PYTHONPATH=. negative control reproduces ModuleNotFoundError runtime_protocol.

Authorized agent-full-1023071006-24096: exit 4 before body, 0 nodes, one collection error. Separate author 0715's later repaired collection is reused, not repeated: 16804/18327 collected, 1523 deselected, exit 2, zero bodies, separate astrid.core.extensions error in test_dev_journey_quick.py. D14/H9 remain visible with no PASS relabeling. Existing 0658 Ruff 2149/2149 and mypy 1912/1912 evidence is reused.

V2 request/reply metadata contract was read and remains untouched. No source/service/test/generated/schema/dependency/pin/Git/upstream changes and no duplicate full request. Resolve the separate extensions collection issue before one replacement full run.
