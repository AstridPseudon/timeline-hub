# AM snap plate public positive — bounded patch ready; requiredD09 incomplete

Worktree: /home/user/work/wt/vw-m3-d09-am-plate-public-positive
Base: cf7448ed6c1298b172d004914cfe2bb8c99048e7

Read PLAN.md, COMMON.md and the current Viewing INBOX, including the 21:50 remaining-capabilities grant and 11:59 MAIN golden decision. No renderConfig field or golden policy change was made.

## Finding and change

First exercised the current historical-source reader and existing projector through prepare_filmstrip, Timeline serialization, real materializer, canonical render profile, normal final Root staging/callback and installed public12 host. Runtime document reads/admission are explicit test doubles; the actual preparation implementation is used. The callback aborts before any renderer runs. The positive failed before the change (UNKNOWN instead of COVERED/CONTENT); empty authored params stayed UNKNOWN. Element manifest defaults do not inject a fill into that empty clip. This was a missing component hook, not evidence for manufacturing an assetless default fill.

Extracted only the existing source/fill/background resolution and fill-token table into am-snap-plate/surface.ts. Both drawing and scene preparation call it. Registered preparePlateScene on the actual component using the existing prepareSceneCapability seam. It declares the viewport support already painted by AbsoluteFill when the selected backing is a proven opaque three/six-digit CSS hex colour. Support comes from that backing, never guessed image alpha. Unsupported CSS colours/alpha and raw clips with neither source nor fill remain UNKNOWN. Existing view, image, tint, wipe, mosaic and colour behavior remains intact; no manifest or theme changed.

Actual AM positives now pass through normal/owner-qualified registry dispatch: COVERED/CONTENT image, COVERED/EMPTY explicit #F7F4ED background, GAP, known full-frame bounds/opacity, one-sided fade DIP, translucent GAP, managed transparent-PNG backing, and the backing during component wipes/mosaic/pan/tint. Ten existing-draw variants at nine frames each preserve their pre-edit SSR hashes. The public12 DEFAULT_THEME still equals Agent's existing default; the rendered plate's default paper field is unchanged.

## Remaining blocker (do not delete D09 callers)

Immutable public12 deliberately marks **any clip.entrance / clip.exit and nonzero crop on an element** as unknown-animation-geometry in scene-evaluation, independently of the component's intrinsic capability. Exact cropped-plate, scale-in and fade-up positive replacements therefore cannot be earned by this authorized AM directory patch. The new tests retain the original private positive assertions and expose the actual public limitation; all original tests remain unchanged. Component enter/exitWipe positives do not substitute for outer animation positives.

The SDK check/onscreen/labels/reflow/motion/mouth/cache paths were not edited. A source-bound SDK caller replacement remains a separate Agent gate. This patch does not complete requiredD09 or certify a real Runtime, rendered pixels, image loading, audio, native environment admission or gate 6. No source factory, copied projector, new public type/package or authoring rewrite was introduced.

## Exact evidence

Commands run from the worktree above. All pytest commands used this exact environment/executable prefix:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules /home/user/work/venv-agent/bin/python -m pytest
```

Final command (append to that prefix):

```sh
-q -p no:cacheprovider -o addopts= --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-plate-public-positive/pytest-final tests/packs/rendering/test_am_snap_plate_scene_capability.py tests/packs/rendering/test_scene_host.py tests/packs/rendering/test_scene_source_carry.py tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
```

**108 passed in 34.95s** (14 new direct cases plus 94 existing neighbors). Full log: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-plate-public-positive/final-tests.log

Earlier commands, with that same prefix:

- `-q -p no:cacheprovider -o addopts= --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-plate-public-positive/pytest-before tests/packs/rendering/test_am_snap_plate_scene_capability.py`: **1 failed, 1 passed in 5.19s**, the intended missing-capability positive, before any product edit; before.log retained.
- `-q -s -p no:cacheprovider -o addopts= --tb=short --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-plate-public-positive/pytest-ssr-before tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_registered_plate_ssr_preserves_existing_draw_and_default_theme`: **1 passed in 4.00s**, records the pre-edit hashes; ssr-before.log retained.
- Same flags as the first command, basetemp `pytest-after`: **3 passed in 5.23s** after registering the hook; after.log retained.
- Same flags, basetemp `pytest-positives`: **4 failed, 10 passed in 10.65s** while expanding tests: the test incorrectly assumed a projected managed asset kept its raw P key, and three comparisons omitted visible_at's required element metadata argument. Corrected only the new fixtures, preserving all positive assertions; positives.log retained.
- Same flags, basetemp `pytest-fixed`: **14 passed in 13.80s**; fixed.log retained. Final 108-case run includes the additional private-stage peer/version assertions.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-plate-public-positive/typecheck.py
/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/rendering/test_am_snap_plate_scene_capability.py
git diff --check
```

All **exit 0**. Targeted strict TypeScript uses byte-equal copies of the plate and its direct source dependencies in an owned overlay, immutable public12, and read-only peers; noEmit, strict, moduleResolution=Bundler. Script/log retained; disposable overlay removed. This is not a whole-repo make check/full-suite result.

Public package SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, version 0.0.12, all **77 installed files hashed before/after each preparation fixture**. Private scopes are real directories and only package leaves link to the selected peers. React 18.3.1 and Remotion 4.0.509 asserted. Read-only peer worktree HEAD is f8164bef73215272562c4d6974acadbd82c2898a; neither polluted App nor scenegraph was used. No shared writes, installs, network, browsers, sockets, captures, renders, full suite or .git mutation.

## Artifacts and next step

Flat handoff files:

- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-plate-public-positive-exact.patch
- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-plate-public-positive-replacement-map.md
- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-plate-public-positive-filelist.txt

Agent can review this four-file component unit separately. RequiredD09 remains blocked on package-owned crop/outer animation positives and the subsequent separately authorized caller join. BLOCKED, rather than DONE, records that the requested complete positive set was not earned within this grant. commit-msg is supplied for the harness; no commit was run.
