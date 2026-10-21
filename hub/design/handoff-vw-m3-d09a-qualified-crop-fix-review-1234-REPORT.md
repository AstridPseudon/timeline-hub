# vw-m3-d09a-qualified-crop-fix-review-1234

## Verdict

**APPROVE.** The correction restores the qualified selected public crop and
the original private-crop tripwire, while preserving the settled semantic
motion/private pixel fallback split.

## Review

- `_public_mouth_facts` now retains the validated public rectangle whenever
  explicit `mouth` is present and valid. Omitted `mouth` still admits only
  qualified public semantic states and returns `rect=None`.
- `render_lipsync` chooses `_public_crop` for that qualified rectangle and
  calls the existing `model.mouth_box` only when no public rectangle exists.
- The direct aggregate test restores the original tripwire:
  `pytest.fail("public ROI used private crop")`.
- The hunk does not add public fields, DTOs, geometry capabilities, pins, or
  activation changes. It does not alter explicit-null/raw-invalid,
  stale/forged/mixed/UNKNOWN, `0.0 -> closed`, strict `> 2%`, or the `799`
  denominator rules. No changed-hunk counterexample was found.

## Evidence

The completed source worker reports this exact pinned targeted command:

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

Result: **37 passed in 7.76s**. This includes the original aggregate positive,
the restored qualified-public tripwire in both fresh/cache modes, and the
strict-threshold/crop neighbors. Node was v20.19.4 with SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

Additional read-only in-memory probe against the author source plus exactly
the handed-off correction passed:

```text
isolated qualified-tripwire: PASS
eligible omitted-mouth semantic + private ROI fallback: PASS
```

The probe asserted that qualified explicit public ROI never calls
`mouth_box`; omitted-mouth public rows never call private `mouth_state` and
call the old `mouth_box` fallback once for pixels.

`git diff --check`, AST parsing, and source Ruff checks passed in the source
worker. No full suite, browser, physical capture, install, network, or shared
dependency write was run.

