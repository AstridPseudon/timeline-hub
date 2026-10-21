# Agent literal-three current union

Status: **SOURCE ONLY**. This candidate combines the completed ordered-remove,
track-mute, and clip-opacity units on the current Agent floor. It does not
change Runtime/App, generated clients, pins, activation, generation, or live
callers.

## Exact source references

- Starting ordered-remove floor: Agent commit
  `30f3d20bf2788e62c1e157f1767d2156dca15131` (`c49` schema).
- Reviewed track-mute source unit: `3804a26a016e4dafa6ed0d1db7ee9d37a9fc0441`.
- Reviewed opacity source unit: `391dd72bbc52e350df8888888bc68aa9a98b184c`.
- Resulting schema: `astrid/core/timeline/schema/edit-command.schema.json`,
  SHA-256
  `da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068`.
  It has 59 definitions and 33 operation clauses.

The union adds only raw boolean `track.muted` set/clear and raw clip
`opacity` in the inclusive numeric range `0..1`. Existing ordered project-data
remove mode, opaque values, null/absence/order behavior, original guards, and
strict inverse behavior remain in place. No old whole schema was copied.

## Floor reconstruction

The compact guard in
`tests/sdk/test_timeline_materialization_schema_union.py` strips only the other
two additions from a fresh copy for each source and asserts these exact hashes:

| Source reconstructed | SHA-256 |
| --- | --- |
| ordered-remove (`c49`) | `c49a6058cfb49fec3dd12e8d93868de6433f121b07a56a943257e34b239f9b7c` |
| track-mute | `0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890` |
| opacity | `9b4f16f87fffc00da010e2dbea469ca6bfc021695c5b453c821d1d4553336708` |
| all three removed (`84fc`) | `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5` |

The existing checks continue to cover the preserved `65bb`, `27f`, `392`,
`613`, and `6ba` floors; historical compatibility comparisons strip only the
two intentional scalar widenings where the checker cannot model enum extension.

## Touched paths and hashes

```text
da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068  astrid/core/timeline/schema/edit-command.schema.json
5bd7760401f3b17d2bc8542b14e63a0ab19db60a2f072281dbc324d651104a88  astrid/sdk/timeline/_scalar_commands.py
9abfa98994ff8287f7f0d37f797fc6859d8a6688e7648a5cf0cbca06d0272a13  astrid/sdk/timeline/_clip_scalar_commands.py
7998213e56be0ff12de449859c5feebd6fccb0104ca7676d8711f1836219e9f9  tests/editing_conformance/test_recipe_track_scalar_fields.py
8a13a068f4a886646551a8af6950567482530aed21a9a9db43a776337c5c5283  tests/editing_conformance/test_recipe_clip_scalar_fields.py
965f8e2f2e2ad228cb5129b295e360352a12bd0f1baff740cf0fe76c08477ffa  tests/sdk/test_timeline_materialization_schema_union.py
b58ee969415fd15b368917c7ee76b6c8a2f6277a924e3b53354aa1f71f6d28da  tests/sdk/test_timeline_current_union_schema.py
```

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_track_scalar_fields.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_m2_project_data.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py`
  — **211 passed** in 178.88s.
- The four compact floor nodes — **4 passed** in 0.70s.
- Ruff on all touched Python files — passed.
- `python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json` — passed.
- `git diff --check` — passed.

No full, Runtime, App, browser, HTTP/live-socket, generation, pin, activation,
or live-caller suite was run.
