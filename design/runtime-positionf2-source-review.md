# Runtime source review: literal flat clip position

**Disposition: SOURCE ACK.** This is a bounded review of Agent commit
`f2a2cfbb58926b7c9d47d206ae294acf376b0c2e` (tree
`8c5674a5e329ab8dc5dcb4711251268a61b81847`). It does not qualify a Runtime
DTO, generated pair, HTTP path, activation, pin, or freeze.

## Contract checks

- The carrier remains version-1 `clip.set`; no new operation, DTO, endpoint,
  scene, stored scale, nested position object, or `params` alias was added.
  The only source implementation change is the existing scalar capture
  docstring (`astrid/sdk/timeline/_clip_scalar_commands.py:113-115`); writes
  continue through the generic scalar recorder (`:89-110`).
- `ClipSetArgs.values` is closed and declares exactly the eight flat leaves
  `x`, `y`, `width`, `height`, `cropTop`, `cropBottom`, `cropLeft`, and
  `cropRight` as numbers (`astrid/core/timeline/schema/edit-command.schema.json:2095-2139`).
  `clear` admits the same leaves, has `uniqueItems`, and the generic scalar
  overlap check rejects set/clear overlap (`:2141-2158`; `astrid/sdk/timeline/_scalar_commands.py:34-40`).
  JSON validation plus `json.dumps(..., allow_nan=False)` rejects null,
  strings, expressions, booleans, objects, arrays, and non-finite numbers.
- Capture and execution write literal values or remove presence only:
  there is no clamp, normalization, rounding, defaulting, display-scale
  conversion, or time-map dependency for these leaves. Opaque siblings and
  timing remain untouched. The direct conformance cases cover absent,
  present-null, present-empty-string, present-expression, and present-opaque
  old tags, plus all eight set/clear leaves.
- `_target` binds the selected parent/occurrence owner and exact clip ref and
  pins the parent/source images (`astrid/sdk/timeline/_scalar_commands.py:14-31`).
  `_clip_basis` records clip type and media identity reads, including the
  scoped asset registry where applicable (`:52-65`). The conformance cases
  exercise parent and explicit occurrence targets, stable source/owner
  state, disjoint-leaf rebase, same-leaf stale refusal, and A→B→A inverse
  refusal.
- The raw timeline schema independently keeps all eight fields as numeric
  top-level `TimelineClip` properties. No position/scale storage was added.

## Floor and union identity

The exact Main014 floor commit is `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
(tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`). Its
`astrid/core/timeline/schema/edit-command.schema.json` bytes hash to
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, and
the position commit's parent has the identical hash. The position commit's
current schema hash is `b06d49c1be645ec6631bad109963697a3e5eb956786953751fd57b650be19836`.
No `5672d2b7...` / raw-union schema identity appears in this checkout or its
position diff; the current-union test explicitly restores the frozen S2
`ClipSetArgs` slice before comparing it.

## Evidence and limits

Direct command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_clip_position.py
167 passed in 6.34s
```

The handoff's existing evidence was also inspected: the broader position/
provider lane is recorded as 168 passed and the current-union schema lane as
34 passed; neither broad lane was repeated. `git diff --check` passed. The
Main witness at `src/tools/video-editor/lib/timeline-data.ts:44-76` confirms
flat fields, and `src/tools/video-editor/hooks/useTimelineCommandsService.ts:732-735`
rounds only `at`, so UI narrowing does not widen or normalize this raw
carrier.

No Runtime/App2 live callers changed: **NONE**. No generation, freeze, pin,
activation, public014/privateC3d mutation, HTTP, socket, browser, render, or
full-suite evidence is claimed.
