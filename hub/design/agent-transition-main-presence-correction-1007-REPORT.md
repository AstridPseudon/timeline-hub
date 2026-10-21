# Agent transition Main-shape presence correction

Date: 2026-10-21 UTC

## Result

Implemented the bounded dormant Agent correction on clean ca9 provenance:

- `clip.set` now permits an omitted `elementRef` only for an existing raw
  transition with both `elementRef` and `element_ref` keys absent and an exact
  `(type, revision presence/value)` match.
- Present canonical or legacy reference keys, changed type, changed revision,
  and changed revision presence refuse visibly.
- Canonical/legacy identity decisions use explicit key presence and a local
  `MISSING` sentinel; no truthy fallback selects authority.
- Existing raw transition fields remain opaque and are merged; params absence
  and null are retained, object params update only supplied keys, and null does
  not erase existing known selected params.
- Existing adjacency, shortest-fit, owner, source/media, selected P1, inverse,
  and ref guards remain in place.
- The transition schema now admits literal `params: null`.

No registry activation, generation, pin, release, private017 mutation, native
or HTTP path, DTO/store/authority addition, or live caller change was made.
The only changed runtime-facing code is the dormant `clip.set` handler and the
existing selected-parameter history helper. `capture_clip_set` callers are
unchanged.

## Exact source/schema

Base: `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`.

Current worktree SHA-256 values:

| Path | SHA-256 |
|---|---|
| `astrid/sdk/timeline/_clip_scalar_commands.py` | `00073fb27f792cd0e061d8c5a01cb7e0dc0e82c6b77156b857d03f6a144141be` |
| `astrid/sdk/timeline/_selected_param_authority.py` | `8b19d56d2c28f1dc9e003f1a578e361397e0f73845319ee76cd60456ba211fdf` |
| `astrid/core/timeline/schema/edit-command.schema.json` | `27b76296a6c1a81495a1cdd80b13d765ebf7952af1967eb839d2fd3606413eab` |

The ordinary6ba floor remains the reviewed exact schema source
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(55 definitions / 29 clauses). This worker did not compose or regenerate a
full successor; the current correction is source-only and retains the
ordinary floor as the reconstruction boundary for the later reciprocal
Runtime ACK.

## Evidence

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_current_union_schema.py` — **178 passed**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_composed_schema.py` — **5 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m py_compile astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_selected_param_authority.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_current_union_schema.py` — **passed**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m json.tool astrid/core/timeline/schema/edit-command.schema.json` — **passed**.
- `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_selected_param_authority.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_current_union_schema.py` — **passed**. The untouched import-order finding in `tests/sdk/test_timeline_transition_schema.py` is pre-existing on ca9.
- `git diff --check` — **passed**.

No full or full* suite, browser, localhost, socket, Runtime/App integration, or
generated artifact test was run, as required by the brief.

