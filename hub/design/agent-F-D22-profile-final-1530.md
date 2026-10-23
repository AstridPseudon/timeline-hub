# F-D22 final profile artifact review

Status: **PASS**.

`957fbe955` is directly stacked on reviewed `42476c08a` and deletes only the
introduced root `report.md`. The final cumulative diff from
`58316fd6e0ce8a1fb3b2b3826ec71906d29080de` has exactly these four authorized
test files:

- `tests/packs/rendering/test_am_snap_plate_scene_capability.py`
- `tests/packs/rendering/test_remotion_backend.py`
- `tests/packs/rendering/test_remotion_layer_tail_compat.py`
- `tests/packs/rendering/test_remotion_typecheck_mappings.py`

All four final blobs equal their reviewed `42476c08a` blobs. The root report is
absent from `HEAD`; no tracked report was added. `git diff --check` and
compileall of all four files passed. The working tree is clean.

Reused independent PASS evidence: `34 passed, 6 failed`, representative
`6 passed, 3 failed`, mapping `3 passed`, mutation probe passed, Ruff `2149`,
and type baseline `1912`. The six residual failures are unchanged: the raw
manifest child `runtime_protocol` import, three outer-geometry `GAP` versus
`UNKNOWN` controls, and two audio fade vectors lacking `audio.render_source`.
No full or known-red suite was rerun, as directed.
