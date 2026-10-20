# Review and run commands

Source/controller preparation only. **No grant, central request, browser, socket or current capture has been run.** Existing historical MAIN outputs are read only. The following shell aliases expand to the exact paths used:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=vw-m3-current-root-cap-three-stills-prep
OWN=$ORCH/workers/$WORKER
P=$ORCH/design/handoff-$WORKER-
PY=/home/user/work/venv-agent/bin/python
NODE=$OWN/node
```

Executed offline commands (exit 0 unless the preserved setup correction below says otherwise):

```sh
$PY -B ${P}controller.py freeze
$PY -B ${P}controller.py preflight
$PY -B ${P}offline-checks.py
$NODE --check ${P}render.mjs
$NODE --check ${P}resolve.mjs
```

Python AST parsing of all three handoff Python files also passed. No pyc is retained.

Native targeted tests were run in OWN/offline, a temporary snapshot of Agent `4ef1391c2c104d5d11b3a27265035c51be296045`. Its unchanged tests/conftest.py, tests/lanes.py, tests/process_groups.py, tests/__init__.py, tests/editing_conformance/test_compile_contracts.py, audio_compile_contract.json, visual_compile_contract.json, main_image_cap_raw_closure.json and tests/packs/rendering/test_managed_timeline_render.py were read from that Git commit. No source or test expectation was edited. Exact command (with aliases above expanded during execution):

```sh
cd $OWN/offline
PATH=$OWN:$PATH PYTHONPATH=$OWN/offline PYTHONDONTWRITEBYTECODE=1 ASTRID_PACKS_PATH='' \
  $PY -B -m pytest -q \
  tests/editing_conformance/test_compile_contracts.py::test_single_occurrence_cap_through_normal_managed_projection \
  tests/editing_conformance/test_compile_contracts.py::test_cap_fade_editor_projection_keeps_clamped_timing_and_authored_source \
  tests/editing_conformance/test_compile_contracts.py::test_cap_fade_public_source_clock_and_half_open_draw_cap \
  --basetemp=$OWN/pytest-temp -o cache_dir=$OWN/pytest-cache
```

Result: **5 passed in 3.63s**, no skip/xfail. The first collection attempt lacked visual_compile_contract.json in this manually selected snapshot; it exited4. The missing exact Git file was added and the same command passed. Both outputs remain in `targeted-tests.log`. The ephemeral test snapshot and its own caches have been removed. The native managed-transport helper is a test double; this proves no live admission.

The exact S2 serialized list-form fade input was also evaluated through public12's unmodified `dist/evaluation.js`: clipOpacity at90/105/119 =1/0.5/0.033333333333333326; prepareScene draw/own durations120 and queryTrackFrame at120 gives no layers. This is pure evaluation, not pixels (`pure-evaluation.json`). It used the same Node and the OWN public12 overlay before cleanup.

Independent review inputs: controller.py, render.mjs, replay.py, resolve.mjs, manifest.json, preflight.json, offline-postflight.json, dependencies.json, five replay JSONs, offline-checks.py/log, targeted-tests.log, and this report. Refreeze is not needed for review. A later manager may rerun **preflight**; it replays the frozen Git source in a new short0700 temp, verifies the manifest, all77/wholegraph/six peers/Node/Chrome tree pre/post and removes that temp.

Fresh preflight resources: free `13301075968` B; required `12986365667` B =10GiB reserve + source/package staging +2GiB headroom +3 full raw RGBA frames. Free margin `314710301` B at measurement. Disk/quiet are rechecked at execution and while children run. Peak source archive memory ~78MB plus Python/Node/compiler/browser memory; no numeric RAM admission is claimed. Three PNG estimate <1MiB for the flat input, actual sizes recorded only after capture. No MP4 or full-suite request.

## Manager-only next step after independent review

Do not run capture directly. First inspect fresh preflight and arrange the normal quiet window. No QUIET marker may be active when this controller runs. The controller acquires `/tmp/timeline-viewing-browser.lock` nonblocking and keeps it until the run and postflight finish. Short own `/tmp/vw-cap-*`0700 is passed to Chrome/test children; webpack caching is disabled; temp/cache/config/bundle are removed in finally.

Add this exact named suite line to the central service only after review:

```text
composition e2e-viewing-current-root-cap-three-stills /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-root-cap-three-stills-prep-controller.py capture
```

Then the manager (not this worker) may create `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-root-cap-three-stills-prep-CAPTURE-GRANT.txt` with these exact three lines:

```text
composition e2e-viewing-current-root-cap-three-stills /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-root-cap-three-stills-prep-controller.py capture
controller_sha256=079fa981108214b0dac2d7f1453ae95fc716e2444ae4d6457d3cec538178dc97
manifest_sha256=4127d7e25aba66d57862af09a46368004fcda0a95c5c531ae80c0b0ae490dff9
```

This text is a review template, **not a grant**. There is no CAPTURE-GRANT.txt or CAPTURE-STARTED at handoff. The manifest also binds all renderer/resolver/replay hashes, exact source/projected/serialized/public12 members and original MAIN files. Any changed approved byte requires fresh review.

The manager then submits ONE request:

```sh
R=$($ORCH/bin/request-test $WORKER e2e-viewing-current-root-cap-three-stills) && $ORCH/bin/wait-test "$R"
```

If wait-test returns124, wait on the SAME result; never resubmit. The capture mode also checks the central snapshot cwd, request target/suite and running status. It creates its own exclusive one-attempt CAPTURE-STARTED only after grant/lock validation. All failure outputs remain; an attempted failure needs a new manager decision, not an automatic retry.

Expected outputs after that single window: actual metadata.json; frame-90/105/119.png with actual PNG SHA256/bytes; comparison.json containing all-pixel RGB histogram/raw hash, RGBA extrema, full-resolution RGB max difference and count above2/255 for each exact MAIN PNG, plus actual RGB-based opacity estimate; postflight.json with full graph/tool/source verification. Metadata must be1920x1080/fps30/duration120. No resizing/padding/realignment/exemptions. Approved known intended pixel differences: **none**; source differences are described in REPORT.md. A mismatch fails and stays visible.
