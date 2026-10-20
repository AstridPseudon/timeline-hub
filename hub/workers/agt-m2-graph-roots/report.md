Implemented bounded shot/occurrence roots, `Recording.create_entity`, typed local reservations, new-create compilation without fabricated source pins, and shot-root schema references. Public operations and collection/order/inverse helpers remain unchanged.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider.py tests/timeline/test_authoring_bundle.py tests/timeline/test_authoring_recipes.py
```

**214 passed, 1 deselected, 2 strict xfails.** The xfails preserve positive expectations for compiled-reload inverse and root redo, pending staged inverse work.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py astrid/core/timeline/authoring_bundle.py tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py
git diff --check
```

Both passed. No full, socket, service or Runtime integration runs.

Integration still requires Runtime atomic project-wide ID admission, official schema/pin refresh, staged inverse support and shot-binding capture. No real Runtime acceptance or full migration is claimed.

Both absolute commit-message files are written. Oversized files: authoring bundle **1654**, commit **525**, schema **656** lines. Details are in [the worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-graph-roots/notes/report.md). No commit or merge request made.