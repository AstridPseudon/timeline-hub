Implemented scoped collection queries, exact clip/track row restoration, container-shape guards, and shared alias overlap. Restored rows retain historical order and raw JSON; untouched rows retain newer fields. Legacy M1 records remain unchanged.

Validation: **209 passed in 9.76s**:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py
```

Changed-file Ruff passed:

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_collections.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/commit.py tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py
git diff --check
```

- Line effect: product **+353/−35**; tests **+403**.
- Historical boundaries supply missing legacy inverse order proof; missing proof refuses.
- `timeline.restore` tests are unchanged and pass.
- No full suite, sockets, merge, or git mutation performed.
- Commit messages written as `commit-msg` and `commit-msg.txt`; test cache removed.

No implementation blockers. Merge remains held until recorded M1 completion. Next slice: staged dependent reversal, including reversing consumers before checking creator removal.