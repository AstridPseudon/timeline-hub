# D116/G3 independent protected source review

Static source checks: PASS. Final source qualification: FAIL at the supported semantic capture seam. Behavior: FAIL during fixture setup.

Candidate `65d1dead09331f2615d5649c9a2ede8191799724` is reviewed against its author parent `a30e74e901a28b39c28facba3deb00d76f186e23` and protected baseline `795608e1b9d8077487b26eea50b65c1e79c3f522`. The author commit changes only `tests/editing_conformance/native_checkout_current_fixture.py`; no source fix was made and no author self-review credit is claimed.

Required source checks:

```text
PYTHONPYCACHEPREFIX=/tmp/app-D116-native-gate3-protected-1755-private/pycache /home/user/work/venv-agent/bin/python [AST/compile for fixture and equivalent test] -> PASS
RUFF_CACHE_DIR=/tmp/app-D116-native-gate3-protected-1755-private/ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py -> PASS
/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/app-D116-native-gate3-protected-1755-private/mypy-cache tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py -> PASS
git diff --check a30e74e901a28b39c28facba3deb00d76f186e23..HEAD && git diff --check 795608e1b9d8077487b26eea50b65c1e79c3f522..HEAD -> PASS
```

The refused document-membership edit was replaced by the existing registered `occurrence.delete` semantic command, a local `commands.execute` preview, and the existing registered `clip.add` semantic command. The production Runtime path registers `create_runtime_commit_service`; the provider validates the v1 ABI and dispatches through `RuntimeService.commit_timeline`. The Gate3 behavioral test remains unchanged and retains renderer-off, reload, guarded undo, and unavailable-visualize predicates.

The immutable Runtime commit/tree are present and clean at `/home/user/work/wt/rt-pin-5e9ad1c6` / `de2954a0ceadb4455903d9abdfec3b773318a50f`. The literal path in the brief, `/home/user/work/wt/rt-pin5e9ad1c6`, does not exist; no alias or shared-worktree mutation was created.

The one authorized Gate3 node was run once after admission. It failed before the Gate3 assertions: `native_checkout_current_fixture.py:91` calls `capture_occurrence_delete(authored, "occurrence:occ")`; the helper calls `commands.execute`, and after the occurrence is cleared, recorder compilation recompiles the remaining anchored card. `compile_authored` then raises `TimingCompileError: bound source occurrence/clip is missing or ambiguous` at `astrid/sdk/timeline/native_word_anchor.py:71`, wrapped as `CommandError` at `astrid/sdk/timeline/commands.py:381`. This is an unsupported route for the authored topology, so the final source qualification is FAIL. No retry or alternate route is permitted, and no behavior credit is claimed.
