# MAIN image-cap pixel instrument report

## Result

Prepared one small diagnostic-only instrument:

`tools/measure_main_image_cap.py`

Final worker-file SHA-256: `14273d682c07047e5be807224a714de835b8314ea4f947fe68afb2c76b9997`.

It uses PIL/numpy only. The frozen source-vector and render-proof handoffs
were read first. The source handoff says MAIN materializes hold4 from raw
hold5, with valid numeric-30-fps frames 90/105/119; it explicitly leaves the
visual golden to actual capture. The render-proof handoff remains blocked on
capture, so this report makes no actual frame or opacity claim.

The instrument compares each captured RGB pixel to an explicit opaque control
and the actual background using `(observed - background) / (control -
background)` over one fixed interior ROI. It reports robust median RGB
fractions, channel values, residuals, 8-bit quantization intervals, RGBA
summaries, and control confidence. PNG alpha is summarized only and is never
used as layer opacity.

Inputs are fail-closed for missing files, non-PNG/RGB(A) modes, wrong
dimensions, missing/duplicate/wrong frame numbers, absent background/control,
wrong-color or uninformative control, uninformative background, and too few
informative ROI channels. No input is resized, realigned, or rounded into
frame membership.
The background can be an actual PNG or the controller's explicit constant
MAIN background `RGB(5, 8, 20)`, but exactly one is required.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python tools/measure_main_image_cap.py --self-test
PASS: synthetic fractions 1, 0.5, 1/30; wrong-color, uninformative-control, wrong-dimension, and uninformative-background controls fail closed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff format --isolated tools/measure_main_image_cap.py
1 file left unchanged

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --isolated tools/measure_main_image_cap.py
All checks passed!

git diff --check
PASS (empty)
```

A CLI missing-input probe also returned exit 2 with a JSON
`{"status":"FAIL_CLOSED"}` result. No browser, renderer, listener, network,
full suite, or actual PNG capture was run. No shared dependency was changed.

## Controller handoff

The controller can consume the exact invocation in the sibling
`handoff-vw-m3-main-cap-pixel-instrument-READY.md`, using its captured frame90
as the opaque control and `--background-rgb 5 8 20`. The fixed ROI in that
command is `(192,108,1536,864)`; it is an interior coordinate selection, not
an instruction to resize or align frames. The controller's existing 25-point
measurement should not be treated as a substitute for this independent report.

## Decisions and limits

- The source's predicted values are recorded only as context by the source
  handoff; this instrument does not assert 1, 0.5, or 1/30 for captured frames.
- A caller-supplied control is mandatory. Frame90 may serve as that control
  only when the capture controller has validated it against RGB240, as its
  current plan does.
- Quantization bounds conservatively enumerate independent 8-bit ±0.5 input
  intervals for observed/control/background RGB values. They are diagnostic
  bounds, not a new product threshold or oracle.
