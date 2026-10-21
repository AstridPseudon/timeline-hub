# Agent movement/current-source union

## Result

Ported the reviewed `parent-afterClip84` source implementation from
`edbcd0d5d9be42f6ae4ba596257e45e67177b623` onto reviewed free-multi base
`a19192ea789a209260da46bfbdd5b616fc7cc4ac`.

Implemented only parent after-clip birth behavior: raw source-row clone,
immediate same-track ordering/ripple, exact anchor/media/rate/read guards,
reserved identity handling, and staged replacement compatibility. The current
move-set changes in `_recording.py` and `commands.py` were preserved.

## Exact source/tree/schema

- Base commit: `a19192ea789a209260da46bfbdd5b616fc7cc4ac`
- Reviewed source compose: `edbcd0d5d9be42f6ae4ba596257e45e67177b623`
- Resulting uncommitted tree: `84120e176540fbc2281dcff4b7186ec8ae413274`
- Schema: `astrid/core/timeline/schema/edit-command.schema.json`
- Schema SHA-256: `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`
- Schema diff from base: none; free-multi schema bytes are unchanged.
- Reviewed `native_parent_media_commands.py` bytes: exact match to the source compose.

## Proof

- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_free_move_set.py`
  - 171 passed in 31.00s
- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timing_compiler.py`
  - 121 passed in 173.07s
- `git diff --check`: passed.

The proof covers existing after-clip positive/refusal behavior, exact clone
and immediate same-track ripple, inverse/replay guards, rational-list FPS,
equal-state forward repair and strict free-multi guards, plus one disjoint
free move-set interaction. No new matrix was added.

## Boundaries

- Source-only Agent change.
- Caller list for the new `after=` path: none; no App activation and no
  Runtime acceptance claim.
- No full suite, browser, localhost, live-socket, App, or Runtime acceptance
  test was run.
- No blockers.

## Next step

Orchestrator can review/merge this source-only patch and qualify Runtime/App
consumers separately.
