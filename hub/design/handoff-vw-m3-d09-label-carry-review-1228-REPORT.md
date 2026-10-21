# D09 label existing-row carry — independent source-binding review

Decision: **APPROVE** `d9c863aa7` (`fix(rendering): carry bound scene rows to labels`).

Reviewed the actual changed hunks against declared base `c9ac7c7b0`.

The patch stays on the existing `CaptureSceneLabels` carrier. Fresh rows come
from the retained successful callback; cache rows remain admitted only through
the existing exact cache-key, source/basis/address, PNG-integrity, and payload
validation path. A mismatch remains a cache miss followed by fresh capture.
The new label adapter checks source identity, frame, fps/canvas basis, exact
clip/address mapping, then delegates formatting to the existing
`labels_for_scene`; ordering, opacity, bounds, and visibility are therefore
the public answer semantics. No authored metadata certificate, source
factory, store/authority field, private geometry/pixel math, or `saveNoNode`
change was introduced.

The direct regression covers an ordinary source-bound positive (including
top-first ordering, opacity, full-frame/unknown bounds, declared bounds, and
visibility data) plus stale-frame and forged-source rejection. Existing
assertions were retained.

Evidence, run on an isolated `git archive` of `d9c863aa7` with
`PYTHONPATH=<archive>:/home/user/work/runtime` and the shared Agent venv:

- `pytest -q tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py` — **17 passed**.
- `pytest -q tests/packs/rendering/test_scene_cache_payload.py -k transport` — **38 passed**.
- `pytest -q tests/packs/rendering/test_scene_source_carry.py -k transport` — **20 passed, 39 deselected**.
- `ruff check` on all three changed source files and the changed test — **passed**.
- `git diff --check c9ac7c7b0 d9c863aa7` — **passed**.

No full, browser, native, live-socket, install, or broad suite was run. No
blocker or changed-hunk failure found.
