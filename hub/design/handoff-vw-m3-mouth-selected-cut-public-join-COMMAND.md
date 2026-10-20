# Commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python - <<'PY'
import ast
from pathlib import Path
ast.parse(Path('tests/packs/rendering/test_presenter_selected_cut_aggregate.py').read_text())
print('python AST: ok')
PY
node --check tests/packs/rendering/presenter_selected_cut_query.mjs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/rendering/test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle \
  tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_cut_selection_does_not_invent_a_reference
# 2 passed; local pure lane. Public package query lane requires the central service.
```

The direct public aggregate suite was not runnable locally because this
worktree has no qualified Node 20/composition dependency environment. No
shared dependency or cache was changed.
