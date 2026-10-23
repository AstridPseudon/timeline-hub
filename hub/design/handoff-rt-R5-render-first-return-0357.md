## R5 first-return report — FAIL / BLOCKED

- Runtime SHA/tree: `ac115014b01fc2e970c53d588b53432f7306a615` / `da7d10da5014fddb6e0a985da4ff6a4481aef640`
- Agent SHA/tree: `b53842d307578492aac3a63330babdd0f62f729e` / `57d80ab60e1092b6676b3b48134b4e5445f69112`
- Owned tests preserved unchanged:
  - `tests/test_timeline_render_publication.py`
  - `tests/test_timeline_render_publication_authority.py`

The real-daemon probe reached the staged G4 path but failed at:

`publish_stitched_render` → `publish_authoring_proposal` → `client.tasks.admit`

`RemoteTasks` in the staged Agent checkout has `create`/`admit_task`, but no `admit`. Exact error:

```text
AttributeError: 'RemoteTasks' object has no attribute 'admit'
```

I did not add a substitute adapter, fake publisher, or weaken/drop assertions. No pytest suite was rerun because the known old-route failures remain and the required real entrypoint is unavailable.

Checks:

- `py_compile`: PASS
- `git diff --check`: PASS
- Ruff: existing baseline failures, 2 diagnostics
- Pyright: existing baseline failures, 12 diagnostics
- Worktree: clean
- Frozen artifacts: unchanged

Scenario migration is therefore uncompleted; all original render and authority scenarios remain preserved for the Agent API repair. `BLOCKED` and the requested commit message were written.