# D09 overlay private visibility consumer — no safe deletion

Reviewed current Agent `tl/integration` and the settled D09 source report.
There is no safe product patch for this worker.

The admitted public capture route already exists at
`astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:112-116`:
`CaptureSceneLabels.labels()` calls the source/frame-guarded `frame()` method,
then `labels_for_scene()` at `overlays/labels.py:27-40`. That formatter uses
retained public Scene answer rows and supplied exact address mappings; it does
not duplicate visibility math. `overlay_labels_frame()` uses this branch when
`capture` is present (`labels.py:107-112`).

The remaining private query is the ordinary fallback at
`overlays/labels.py:53-60`, where `labels_for()` calls
`core.timeline.onscreen.visible_at`. It is still reached by
`_filmstrip_cache.py:20-26` for PNG-only/mixed-cache rows and by
`overlay_labels_frame()` at `labels.py:113-114` when no capture is supplied.
Those callers only have snapshot config/fps, not exact resolved Root props,
assets/theme, source/occurrence identity, or retained public rows. The
current D09 source report specifically requires those exact
source/occurrence/frame-bound public labels before this fallback can be cut.

Removing it would either lose original positive overlay output or require an
unbound public query; returning blanket UNKNOWN/empty labels is not allowed.
The public capture branch is therefore an intentional source-bound adapter,
while the ordinary `labels_for()` call is a still-required fallback, not a
safe deletion target. No code or tests were modified.

Evidence:

- Overlay neighbors: **17 passed**.
- Cache/public-row neighbors: **38 passed**.
- Transport source-carry neighbors: **20 passed, 39 deselected**.
- Native source-carry setup was not qualified locally: the combined targeted
  attempt had **78 passed, 19 setup errors** because the default shared
  Remotion peer path lacks `react`; no shared install/write was attempted.
- `git diff --check` passed and the worktree is clean.

Exact prerequisite: the existing source owner must make exact public Scene
rows available to ordinary and PNG-cache label callers, bound to source,
occurrence, frame, and the original ordering/opacity/box/advisory semantics.
Only then can `labels.py:56` and its fallback callers be migrated without
changing behavior.
