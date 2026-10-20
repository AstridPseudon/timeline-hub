# READY — MAIN image-cap pixel measurement instrument

The diagnostic code is in the worker branch at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-pixel-instrument-measure.py`

It is independent of MAIN's renderer and does not choose an expected visual
golden. It accepts exactly the frozen fixture's source image (16x16 RGB240),
PNG stills for frames 90, 105, and 119 (each 1920x1080 RGB/RGBA), an explicit
opaque control PNG, and either an actual 1920x1080 background PNG or the exact
constant RGB background. The ROI is mandatory and supplied in absolute pixel
coordinates; there is no resize, realignment, or frame-membership rounding.

After the capture controller has produced the three PNGs, its current
background basis can be consumed with frame90 as the control:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-pixel-instrument-measure.py \
  --source /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-image-cap-source-vector-image.png \
  --background-rgb 5 8 20 \
  --control /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-capture-controller-frame-90.png \
  --frame 90=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-capture-controller-frame-90.png \
  --frame 105=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-capture-controller-frame-105.png \
  --frame 119=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-capture-controller-frame-119.png \
  --roi 192 108 1536 864 \
  --output /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-pixel-instrument-measurement.json
```

Use a captured background PNG instead of `--background-rgb` if one exists;
never provide both. The ROI is a fixed interior rectangle, not an alignment
instruction. The analyzer reports each input/frame RGBA summary, but has the
explicit invariant `png_alpha_is_layer_opacity: false`; only RGB source-over
relationships are measured.

The output reports per-frame observed fraction, per-channel RGB estimates,
conservative 8-bit quantization bounds, residuals, informative-channel share,
and control confidence. It does not turn the source fixture's predicted
fractions into assertions or claim an actual opacity before capture.

Built-in calibration:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-pixel-instrument-measure.py \
  --self-test
```

This verifies synthetic fractions 1, 0.5, and 1/30, and fail-closed wrong
color, uninformative control, wrong dimensions, and uninformative background
cases.

Manager handoff: exact9aaf8778 diagnostic copied flat above; repo tools branch is evidence-only and MUST NOT be merged. Worktree may be recycled normally. No actual opacity assertion is authorized by this instrument.
