# Agent selected-transition presence repair

Date: 2026-10-21 UTC

## Result

Implemented the three requested repairs on the selected transition authority
path:

- canonical `elementRef` and legacy `element_ref` are read independently by
  explicit presence; absent is not a truthy fallback, and present null,
  empty, malformed, or disagreeing values refuse visibly;
- both present spellings must agree before a selected transition can reuse
  P1 authority;
- `clip.set-params` keeps its existing non-transition lookup behavior;
- provider regressions cover legacy P1 -> unauthorized same-stable-ID P2,
  canonical null plus valid legacy P1, exact unchanged documents on both
  refusals, and matching legacy P1 success.

No schema, generated client, pin, release, activation, generation, Runtime,
App, or Composition change was made. New live callers: **NONE**; existing
generic sheet/SDK callers remain unchanged.

## Exact source and schema identity

The harness will commit this worktree using the required commit message.
Before harness commit:

| Identity | Value |
| --- | --- |
| Base source commit | `47b716d001b45d38805e03b1a254c3353b5968e9` |
| Base source tree | `bbb5ffa28eaadcc521ebc85e115f56e7edf3b1ca` |
| Uncommitted patch SHA-256 (`git diff --binary HEAD`) | `b08ba10e5a124fceecc006964b17c79282cd1cc4a0f9e9fa00896c72929d8cd6` |
| Schema SHA-256 | `9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a` |
| Schema inventory | 55 `$defs`, 29 `EditCommand` clauses |
| Transition-stripped ordinary floor SHA-256 | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |

Changed-file SHA-256 values:

```text
7fb70b05e2bb2c6c289adc4e46b2239c4614a7f6c397e88acbea863839e76bcc  astrid/sdk/timeline/_selected_param_authority.py
d573611e5892d56730829ecc79991241fb96436ae4f5c7fd23ad03f0448e1803  astrid/sdk/timeline/commit.py
f045c36a89d2e60fe5e0829b1ab4f07a257484845bc8652984dd16add76c5c08  tests/sdk/test_timeline_selected_param_authority.py
```

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
85 passed in 27.52s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py
34 passed in 167.86s

/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_selected_param_authority.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_selected_param_authority.py
All checks passed

git diff --check
passed

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json >/dev/null
passed
```

No full/full*, native, HTTP, browser, localhost, socket, generation, pin, or
live-activation suite was run.

## Decisions and follow-up

The strict presence rule is scoped to the new transition carrier through an
explicit resolver flag, preserving the existing `clip.set-params` path as
required. No blocker remains. The harness commit SHA and post-commit tree
identity should be recorded by the orchestrator after commit.
