# Agent full10744 Sprite classification

Date: 2026-10-20

## Result and source identities

The classified run is the completed historical run
`agent-full-remotion12-s2-integration-1020164133-10744`, requested against
commit `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1` and exact source tree
`6de356067d251e644101da19272c5424fa4f3a68`. Its recorded result is:

`14,717 passed, 17 errors, 452 skipped, 4 xfailed, 565 subtests passed in 3300.88s`.

The full run was not rerun, cancelled, relabelled, or used as current
qualification. Its command used Python `venv-agent-child-s2`, Node
`20.19.4`, `agent-remotion-current` as the Remotion project, and the
`agent-remotion-0012/node_modules` peer set.

Current source before this worker's test-only setup edit was commit
`d999197aedc471f7b133e664f8086a0efc6cb66`, tree
`ffa464e51e39dcf03b484be46c6397ee83855769`. The Sprite test file is byte
identical between the pinned full tree and current source before the edit
(SHA-256 `b150fab9792d35429128994a38a1ef2f11c22b8e51473955eaa730d505764cfa`).
The shared host fixture is also unchanged (SHA-256
`6f04c7ea5778165ea1f6b2b66b1c2427b6f480e5efafbbfee498922996710bff`).

## Common trace and classification

All 17 nodes stop during pytest setup with the same error:

```text
fixture 'native_host' not found
available fixtures: ... sprite_ssr, ...
```

The trace points to `tests/packs/rendering/test_sprite_scene_capability.py`
and occurs before any Sprite geometry, UNKNOWN, declaration, source-selection,
SSR, or installed-bytes assertion executes. The module-local
`pytest_plugins` declaration does not make `test_scene_host.py`'s fixtures
available to the xdist full-suite workers. The earlier 33-pass Sprite lane
explicitly collected both `test_sprite_scene_capability.py` and
`test_scene_host.py`, which masked this setup defect by collecting the fixture
module as a test module.

| # | Exact node | Classification | Evidence reached | Disposition |
|---:|---|---|---|---|
| 1 | `test_compiled_sprite_bounds_keep_logical_units_and_source` | Historical test setup | `native_host` setup only | Fixed by scoped fixture registration; geometry/source assertions retained. |
| 2 | `test_compiled_sprite_editor_units_snap_once` | Historical test setup | `native_host` setup only | Same bounded fix; canvas-unit assertions retained. |
| 3 | `test_sprite_registered_ssr_preserves_drawing` | Historical test setup | `sprite_ssr` dependency setup only | Same bounded fix; SSR hash assertion retained. |
| 4 | `test_public_sprite_offcanvas_run_in_mixedscale_and_integrity_addresses` | Historical test setup | `native_host` setup only | Same bounded fix; off-canvas, mixed-scale, provenance, and source-address assertions retained. |
| 5 | `test_known_sprite_bounds_do_not_invent_media_alpha[extra0]` | Historical test setup | `native_host` setup only | Same bounded fix; known geometry and UNKNOWN alpha/coverage assertions retained. |
| 6 | `test_known_sprite_bounds_do_not_invent_media_alpha[extra1]` | Historical test setup | `native_host` setup only | Same bounded fix; known geometry and UNKNOWN alpha/coverage assertions retained. |
| 7 | `test_sprite_missing_dimensions_and_decorations_stay_unknown[params0-None]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN geometry and no-entry SSR assertion retained. |
| 8 | `test_sprite_missing_dimensions_and_decorations_stay_unknown[params1-entry1]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN geometry and entry SSR assertion retained. |
| 9 | `test_sprite_missing_dimensions_and_decorations_stay_unknown[params2-entry2]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN geometry and entry SSR assertion retained. |
| 10 | `test_sprite_missing_dimensions_and_decorations_stay_unknown[params3-entry3]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN geometry and entry SSR assertion retained. |
| 11 | `test_sprite_missing_dimensions_and_decorations_stay_unknown[params4-entry4]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN geometry and entry SSR assertion retained. |
| 12 | `test_sprite_stepped_strip_and_hidden_frames_use_the_draw_clock` | Historical test setup | `native_host` setup only | Same bounded fix; draw-clock, hidden-frame, strip, and geometry assertions retained. |
| 13 | `test_sprite_renderer_selected_source_wins_over_static_fallback` | Historical test setup | `native_host` setup only | Same bounded fix; selected source and unknown-owner refusal assertions retained. |
| 14 | `test_sprite_unsupported_outer_geometry_stays_unknown[outer0]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN outer geometry assertion retained. |
| 15 | `test_sprite_unsupported_outer_geometry_stays_unknown[outer1]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN outer geometry assertion retained. |
| 16 | `test_sprite_unsupported_outer_geometry_stays_unknown[outer2]` | Historical test setup | `native_host` setup only | Same bounded fix; UNKNOWN outer geometry assertion retained. |
| 17 | `test_sprite_public12_declarations_and_installed_bytes` | Historical test setup | `native_host` setup only | Same bounded fix; all package declaration, 77-file digest, symlink, typecheck, and installed-byte assertions retained. |

Classification total: **17 historical environment/test-fixture errors; 0
new source regressions; 0 product failures reached**.

## Bounded fix

Added `tests/packs/rendering/conftest.py` with the rendering-scope plugin
registration for the existing `test_scene_host` fixture module, and removed
only the ineffective duplicate module-local registration from the Sprite test.
No Sprite assertion, fixture input, geometry expectation, UNKNOWN expectation,
declaration check, installed-byte check, product source, Composition artifact,
Node installation, or shared runtime was changed.

The prior 33-pass lane's component and Sprite test source were compared before
the edit. The current AM-sprite component remains SHA-256
`fc79cee164d9d7aeb2a008d9d924e7b41710856b0b630bbc91137ff504b5172e`; the
public12 archive remains SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

## Current targeted evidence

Both runs were queued through the central named test service, after the setup
edit, and used no full suite:

1. `renderer-peers12-integration --files tests/packs/rendering/test_sprite_scene_capability.py`
   with Node 20.19.4, current public12 peers, and xdist `-n 2`:
   **17 passed in 37.98s**.
2. `native-script-current-integration --files tests/packs/rendering/test_sprite_scene_capability.py`
   with Node 20.19.4 and current Remotion:
   **17 passed in 44.26s**.

The first run is the relevant setup proof: the same whole Sprite file passes
under parallel workers, so the historical full-suite setup error is repaired.
The current targeted run also provides serial confirmation. No installed-child
profile mismatch was inferred: the historical run failed before `native_host`
could inspect or use the child profile, and the current Sprite file passes in
the pinned current Node/public12 environment. A child-profile refresh is not
requested by this classification; any future refresh must be owned by the
profile owner and must name exact source/profile differences first.

No full rerun, browser/live-socket run, pixel/audio qualification, or product
change was performed.
