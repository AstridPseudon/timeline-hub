Completed the exact three-file donor port onto Agent `3f7e63b0cfb0c7165b0b61d6f149d038c16dd630`. Current files matched the donor parent, so no adaptation or new semantics were needed. Nothing deleted; tests unchanged.

All three product blobs equal **both** reviewed donors `1a983fa7c2` and `d33fe5f9f0`:

| File under `astrid/sdk/timeline/` | Exact Git blob |
|---|---|
| `_command_state.py` | `f7a1c8ae2b3143535065def60c6be25b243b8059` |
| `inverse.py` | `c04836b08e50677e1a5e69ea3500e59c1fba7d2d` |
| `native_occurrence_media_commands.py` | `b3a925090b1aa26561891719b1626ab9f6672e48` |

Validation passed:

- In-memory `compile(bytes, filename, "exec")` for all three files.
- `/home/user/work/venv-agent/bin/ruff check --no-cache` with those three paths.
- `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --no-pretty --no-error-summary --show-column-numbers --cache-dir "$TMPDIR/mypy-shadow-current"` with those paths. Base comparison used identical options and three `--shadow-file` mappings: **base 0, current 0, normalized new 0**.
- `git diff --check`.
- Exact bounded test command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$PWD:$TMPDIR/runtime-460c-source" \
ASTRID_RUNTIME_CHECKOUT="$TMPDIR/runtime-460c-source" \
/home/user/work/venv-agent/bin/python -m pytest -q \
-oaddopts= -pno:cacheprovider --timeout=45 --tb=short \
tests/timeline/test_occurrence_media_binding_identity.py \
tests/editing_conformance/test_recipe_occurrence_media.py \
--basetemp="$TMPDIR/pytest-source-controls" \
--junitxml="$TMPDIR/source-controls.xml"
```

Result: **87 passed in 11.54s**.

Runtime source was archived from `460c2d397e9beb052a5d03d70123ba8776f22d01`, whose tree `c026c3e486c03513a90176550f26befd74bde4ea` equals reviewed `35764ce10c`. Import checks confirmed Agent came from this worktree and Runtime from that archive. The production publication caller reaches the changed capture path; its existing source test passed.

`commit-msg` and `DONE` are written. Commit subject: `fix(timeline): port F-ABA authenticated item mapping`. **Commit SHA awaits the harness.**

No execution blockers. Keep branch-only until Viewing’s six diagnostic expectation migrations join and independent review passes. No diagnostic/original ABA reruns, installed/home, HTTP, browser, or full-suite qualification claimed.