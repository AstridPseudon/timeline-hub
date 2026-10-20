# D09 post-inspector dead-leaf sweep

Removed `timeline_visualize.model._expected_hash`, a private helper with zero
static, dynamic, export, registration, and resource callers. The visualization
model resource and all active model, sweep, scene-answer, public package, and
cache paths remain intact.

Targeted visualization neighbors passed: **51 passed in 50.44s**.

No full, browser, render, socket, network, install, or managed-proof suite was
run. No tests were changed. The remaining similarly named hash helper in
`astrid/core/timeline/resolution.py` is unrelated and active.
