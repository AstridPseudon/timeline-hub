Blocked: the evidence challenges the producer-only diagnosis. No product code was changed.

The exact ordinal **1297** reproduces RED on unchanged test source. Its `media.admit` step has no effects and preserves the preceding parent image, but Runtime’s `timeline_commit_auth.py:826–842` compares that intermediate image with the final candidate. An effect binding requires a valid effect ordinal; adding one to an empty patch would invent an effect.

Added [a focused genuine-provider regression](/home/user/work/wt/agt-F-D115-effect83-sol-0932/tests/sdk/test_effect_image_prepared_candidate_runtime.py):

- Unchanged final parent: **PASS**
- Same commands grouped into one step: **PASS**
- Unchanged intermediate parent: **FAIL**, at the same strict guard

Runtime remained clean at `1daca2a33f6d7b10053e07c539a54843e3984e19`. All 83 original test-source hashes remain identical.

Validation used `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45`, with the prescribed pinned Runtime environment and retained JUnit XML:

- Exact `test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]`: **1 error**
- `tests/sdk/test_effect_image_prepared_candidate_runtime.py`: **2 passed, 1 failed**
- Runtime `tests/test_timeline_inverse_sequential_authority.py`, with `ASTRID_CHECKOUT="$PWD"`: **28 passed**
- `ruff check`, `mypy`, `py_compile` on the new file, and `git diff --check`: **PASS**

The initial Runtime-control invocation lacked `ASTRID_CHECKOUT` and produced 28 setup errors; the corrected invocation passed.

Retained the [83-node source manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-effect83-sol-0932/evidence/effect83-source-manifest.json), XML, and exact service recipe under worker evidence. Wrote `commit-msg` and `BLOCKED`; no full or 83-case body was submitted.

Recommended next step: Runtime ownership review of unchanged intermediate-parent propagation in `step_output`, preserving authentication for changed images. The sample remains RED; this regression is **not merge-ready**.