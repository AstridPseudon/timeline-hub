# vw-m3-d09a-qualified-crop-preserve-fix-1234

## Verdict

**PASS.** Corrected the NEW state-split selected-crop regression with the
smallest existing-helper split.

## Source correction

`_public_mouth_facts(..., allow_default_motion=True)` now still returns the
validated public rectangle when explicit valid `mouth` input is present, while
omitted `mouth` retains public semantic states with no ROI. `render_lipsync`
uses `_public_crop` for that qualified explicit rectangle and calls the old
`model.mouth_box` only when no public rectangle is available. Thus the omitted
default can use public semantic motion with the old private pixel fallback,
without consulting private `mouth_state` for admitted public rows.

Null/raw-invalid, stale, forged, mixed, UNKNOWN, and closed-0.0 handling is
unchanged. The original 3-of-3 aggregate, strict `> 2%`, and 799-denominator
assertions remain unchanged.

The direct aggregate test restores the exact original tripwire:

```python
monkeypatch.setattr(model, "mouth_box", lambda *_args: pytest.fail("public ROI used private crop"))
```

The prior independent review recorded the required regression: author commit
`8aeba6ac401487a45688789337d9aee7797d420e` failed with that tripwire because
it unconditionally called `model.mouth_box`; the qualified public path passed
on `tl/integration`. The corrected source passes it.

## Qualification environment

- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`
- Node version: `v20.19.4`
- Node SHA-256:
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Composition artifact:
  `/home/user/work/wt/vw-m3-d09a-qualified-crop-preserve-fix-1234/remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- Artifact SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Read-only peer graph:
  `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`
- Registry project:
  `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b`

## Tests

Exact targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
env -u NODE_OPTIONS -u NODE_PATH \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
ASTRID_COMPOSITION_TEST_ARTIFACT="$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz" \
TMPDIR=<private-worker-temp> \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
tests/packs/rendering/test_presenter_crop_equivalence.py
```

Result: **37 passed in 7.76s** (original aggregate 28 plus nine neighbors,
including the direct strict-2% counterexample).

Additional checks:

- `git diff --check`: passed.
- AST parse of both touched files: passed.
- Ruff source check on `builtin.py`: passed.
- The test file’s existing import-format `I001` is present on the base
  `tl/integration` file and was left untouched to keep this repair minimal.

No full suite, browser, physical capture, install, network, or shared
dependency write was run. Temporary private test state was cleaned up.
