Updated only [test_commit_runtime_m1.py](/home/user/work/wt/agt-m1-cli-journey-review/tests/editing_conformance/test_commit_runtime_m1.py:159). Expected readback now uses main’s lossless authoring codec for the entire bundle, preserving occurrence/placement, shot, and source-mapping checks. Independent public GET assertions verify the complete accepted parent payload, digest, identity, and dependency manifest.

Central run `agt-m1-cli-journey-review-commit-integration-1019195003-6839` executed:

```bash
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_commit_provider_runtime.py
```

**Result: 2 passed, 1 failed in 23.08s.**

- Passed: touched-basis conflict schedule and structural real-store test.
- Disjoint schedule passed readback, restart/retry, rebase, undo, and exact `show`; failed at native inputs visualization.
- Blocker: [_resolve_view](/home/user/work/wt/agt-m1-cli-journey-review/astrid/packs/timeline/cli_visualize.py:191) selects `contact` without considering `--mode inputs`; [SDK validation](/home/user/work/wt/agt-m1-cli-journey-review/astrid/sdk/remote.py:889) requires `filmstrip`. Stopped at the product boundary, retaining the original expectation.
- Post-visualization history and historical readback assertions remain unreached. Full suite was not run.

Tested source tuple:

```text
Agent base: 8c4bd8506a9b3809875a894b4898381b8d4798aa
Agent tree: cb1c4aa6d6c96f8d834b1c4327f1b45fe7f9cf4a
Runtime:    182a7dd8446456162a452a25c8493256c5da29fe
App:        0dfb3896545e555c221c5be7a6e1680965b6d004
Composition:7aa384a9f3c815f78ce88ff9b47de5adee7bf34a
```

`python -m ruff check --no-cache --isolated --select E4,E7,E9,F tests/editing_conformance/test_commit_runtime_m1.py` and `git diff --check` passed. Harness commit message written.

Recommended next step: dispatch the bounded CLI input-mode default correction, then rerun this central lane. **M1 remains unproven.**