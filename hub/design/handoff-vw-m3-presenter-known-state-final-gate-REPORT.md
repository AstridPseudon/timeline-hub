APPROVE

Implemented final gate cleanup:

- Preserved public normalized presenter state and motion/codebook behavior.
- Kept legacy compatibility ROI separate and optional.
- Regenerated stale `artifacts.json`.
- Wrote commit message and `DONE` marker.

Tests:

- Presenter scene/crop: **17 passed**
- Neighbor suite: **38 passed, 2 skipped**
- Artifact manifest tests: **8 passed**
- Node syntax, Ruff, manifest check, and `git diff --check`: **passed**

No full suite, browser, install, network, pixel-threshold, or product behavior changes performed.