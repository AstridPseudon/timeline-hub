# CURRENT capture scene-props hook

Implemented on Agent base `7261b4ad5827466b2e17f1a30bf35d2fd05e0700`.
Only product change: `astrid/packs/rendering/rendering/renderers/remotion/run.py`
(9 added lines, 1 replaced line). One new direct test file. No repo reports.

Read PLAN, CURRENT run.py, presenter `802669926e3d18372b3909fd25a0c565beb39bfb`,
inactive public scene transport / role fix `2f53b3674924f02821e94f46ad5a5fc7b1d4db87`,
and the selected-cut aggregate ORCHREPORT. The latter accurately describes its
source54b9 donor, but CURRENT lacked its callback. No broad09 was applied.

`capture_remotion_frames(..., on_scene_props=None)` now forwards a supplied
callback to the existing locked executor. At run.py:1168-1170 it observes
`on_scene_props(merged_props, frame_numbers)` synchronously AFTER final JSON
serialization, alpha-theme neutralization and effect-asset injection, and BEFORE
capture, inside the existing materializer/asset-server ExitStack lifetime.
The props include exact timeline, resolved assets, resolved theme and review.
The sorted/deduplicated tuple is the same object passed to the persistent
capture session; CLI sequence flags encode that exact frame set. No extra
metadata frames, serialization, projector or renderer is introduced.

Omitted and explicit None retain the old locked-executor keyword shape.
Video renders never call the observer. Observers must treat props as read-only;
exceptions propagate unchanged and abort capture before submission, with the
normal props/public-assets/server/materializer/scratch cleanup. Callback success
is preparation evidence, not proof that subsequent capture succeeded: callers
must discard retained observations if capture fails or omits requested frames.

## Exact basis seam for the source-owner join

The donor callback intentionally retains its TWO arguments; no basis DTO or
new callback argument was invented. CURRENT frame capture does not compute or
forward a RenderProfile. Its existing authority is
`_canonical_profile(timeline_path, _load_registry_mapping(assets_path), theme_path)`
from `astrid/packs/rendering/shared/rendering_backend/__init__.py:235`, which uses
`resolve_render_profile` / `_remotion_canvas` in `astrid/core/rendering/profile.py`.
From that profile, use width, height and fps_rational numerator/denominator for
`remotion/src/host-scene.ts:7`'s existing `{fps,width,height}` basis. Resolve it
from the SAME frozen materialized input paths; do not reload a mutable working
copy later. Preserve fps_rational as the exact rate until the existing public
numeric-fps boundary. Thumbnail `frame_resolution` is only output resizing.

The direct test deliberately supplies pinned theme canvas 800x600@24 and a
partial authored override `{width:640,fps:29.97}`. The existing profile selects
640x1080, fps_rational=(2997,100), even though merged theme canvas retains
height=600 and the thumbnail is 4x3. Therefore reading merged theme canvas alone
would be wrong. No new default/theme/basis inference was added. The inactive
host transport still refuses RenderClockTail; that existing limitation is not
changed or qualified by this hook.

## Verification

Exact reproducible commands: adjacent `exact-tests.txt`.
Final targeted command: **41 passed in 3.47s, exit 0**: 11 new callback cases
plus 30 unchanged native-window/frame-session/scratch neighbors.
New tests exercise real CURRENT capture batching, locked command preparation,
timeline serializer, theme resolution, managed-asset integrity/staging/registry
resolution, frame resize and cleanup. Existing seams replace launcher validation,
registry regeneration, effect staging, port selection, HTTP server and capture
submission. Synthetic PNGs only test the resize/output contract; they are not
rendered-pixel evidence. Both CLI and persistent submission paths are observed.

Cases cover final props including opaque nested null/false/empty values,
post-staging params, alpha themes, exact frame tuple and selection, live staged
files/server, callback ordering and once-per-batch behavior, omitted/None call
compatibility, identical serialized Node props across omitted/None/observer,
video exclusion, callback exception identity/no capture, capture exception and
missing requested-frame refusal, and lifecycle cleanup on each outcome.

New-test lint passed. Renderer standalone lint exits 1 on five existing F
errors; including I yields seven diagnostics. Exact HEAD-vs-working diagnostic
comparison is unchanged (4 F401, 1 F822, 2 I001), exit 0. Kept those unrelated
baseline issues untouched. `git diff --check` passed. Flat patch applies with
`--whitespace=error-all` to a disposable two-file HEAD baseline; applied outputs
match worktree bytes. Logs live in the assigned worker ORCH directory.

No browser, real rendering/capture/SSR, socket, full suite, installation,
network, central test request, git commit/checkout/merge, or push occurred.
No new xfail/skip or changed existing expectations. First focused run: 9 passed;
final expanded run: 41 passed. No implementation blocker or disputed plan decision.

## Next step

Review/land this current-base prerequisite through the harness. Agent source
owner then joins frozen post-resolve/historical source and projector occurrence
facts with this exact props/frame lifetime and the canonical profile seam.
The hook does not certify source, activate SDK checks/labels/mouth consumers,
replace private evaluation, or qualify D09/M3/Gate 6. Renderer-independent saving
and known-scene behavior remain unchanged. No full or browser grant is needed
for reviewing this bounded implementation; any later live qualification belongs
to the manager's central service grant.
