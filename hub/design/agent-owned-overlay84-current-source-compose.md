# Agent owned overlay 84fc current-source compose

## Peer ACK scope

This is an Agent source-only handoff for the private owner-pinned overlay
successor. It composes the reviewed f83 assertions onto the current 84fc
source. It does not activate an App caller, claim a normal/public cohort,
change Runtime, or qualify hosted/system built-ins.

## Exact source delta

- Current canonical schema:
  `astrid/core/timeline/schema/edit-command.schema.json`
- New canonical schema SHA-256:
  `5f42a41d65f5feb705456995330e0f749f42e89eb25163b2675d20705917e261`
- Removing only `ClipAddArgs.properties.schema_source` reconstructs the exact
  84fc source SHA-256:
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
- The sole schema addition is optional `ClipAddArgs.schema_source`, an
  existing `DocumentPin`.

The add path accepts that pin only with an exact owner-qualified `elementRef`
(`packId`, `id`, `kind`, `revision`), requires an effect whose id equals
`row.clipType` on an active visual output track, resolves the retained admitted
snapshot through the existing source-input path, and validates only known
params. Unknown row fields and unknown params remain opaque/literal.

The existing `clip.set-params` carrier and `clip.delete` removal path remain
unchanged. Add records exact `params.schema`, `params.snapshot`, and fixed
`params.element` dependencies. Selected authority recognizes the born add,
invalidates it on removal, and preserves original authority through
set/clear/delete/inverse/redo and disjoint rebase. Wrong owner, revision, or
pin refuses before writes. No caller inline hash/disk authority, new resolver,
DTO, store, endpoint, or source fabrication was added.

## Evidence

Passed with the worker checkout and shared Runtime import root:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-overlay84-source \
  tests/sdk/test_timeline_builtin_overlay_authority.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_current_union_schema.py
63 passed in 171.22s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-overlay84-neighbors \
  tests/editing_conformance/test_recipe_m2_clip_add.py \
  tests/sdk/test_timeline_clip_add_provider.py \
  tests/sdk/test_timeline_selected_param_authority.py \
  tests/sdk/test_timeline_selected_schema.py \
  tests/sdk/test_timeline_selected_schema_runtime.py
122 passed, 33 deselected in 21.62s
```

No full, browser, live-socket, Runtime, App, hosted/system, activation, or
public-cohort suite was run or claimed.
