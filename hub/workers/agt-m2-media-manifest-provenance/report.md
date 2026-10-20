Implemented the shared provenance fix; both strict xfails now pass. Exact undo/redo preserves original pins and disjoint additions, while dependent references and corrupt boundaries refuse atomically. Implementation is frozen; both commit-message files are written.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_recorded_graph_roots.py tests/editing_conformance/test_recipe_m1_commands.py
```

**303 passed.**

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_runtime.py
```

**4 passed.** Ruff and `git diff --check` passed.

Used existing accepted boundaries without ABI/schema changes. Also fixed an absent→absent grouped inverse bug. Real Runtime acceptance is proven with test-only forward admission; production popup operations and artifact refresh remain unqualified. No full suite ran. M2 integration remains held pending PLAN M1.

[Detailed report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-media-manifest-provenance/notes/report.md) · [Updated handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-popup-native-contract.md)