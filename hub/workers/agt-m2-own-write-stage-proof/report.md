Implemented generic stage validation and input-head replay claims without new record fields. One registered fixture recipe proves own-write reads, two creates, exact undo/redo, disjoint C preservation, ABA rejection and surviving-dependent refusal. Existing M1 goldens remain unchanged.

Final targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_internal_stages.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recorded_graph_roots.py tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider_scalar.py tests/sdk/test_timeline_commit_graph_roots.py tests/sdk/test_timeline_sync.py
```

**473 passed in 21.95s.**

```sh
/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_collections.py tests/editing_conformance/test_recipe_internal_stages.py
git diff --check
```

Both passed. Full suites, network tests and real Runtime acceptance were not run.

[Report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-own-write-stage-proof/notes/report.md>) and both commit-message files are written. No technical blocker for the covered cases. Review the recorder and collection-proof changes together; **M2 integration remains held until PLAN clears M1**.