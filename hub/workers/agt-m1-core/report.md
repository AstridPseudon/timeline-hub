Implemented native move capture/execution, guarded replay/inverse/redo, track-create proof, canonical schema, and two parity fixtures. Published the API seam early in `m1-agent-coordination.md`. Commit message written; no git mutations performed.

Tests:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1*.py --basetemp=/tmp/agt-m1-core-final-focused
```

**45 passed** on final code.

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1*.py tests/timeline/test_authoring_bundle.py tests/timeline/test_authoring_recipes.py tests/sdk/test_timeline_structure.py tests/sdk/test_timeline_restructure.py --basetemp=/tmp/agt-m1-core-final-neighbors
```

**109 passed, 1 integration test deselected** by the repository’s default lane.

Product Ruff, isolated test Ruff, schema byte comparison, and added-file whitespace checks passed.

Decision: parent `payload.clips` changes preserve legacy `config.clips`, avoiding unrecorded writes. Image provenance uses entity dependencies; provider remains responsible for authenticated ancestry and publication.

**Size:** 911 Python product lines + 656 frozen schema lines = **1,567 lines**.

No blockers. Full, browser, socket, and integrated-provider suites were not run. Next: integrate provider/frontends and verify App capture against both fixtures.