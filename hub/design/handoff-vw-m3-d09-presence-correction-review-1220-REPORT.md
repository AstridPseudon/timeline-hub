# vw-m3-d09-presence-correction-review-1220

## Disposition

**APPROVE** `tl/vw-m3-d09-default-presence-fix-1218` at `0e6316dcb75572a69f1344798d0fc5ffdda70d57`, based on `tl/vw-m3-d09-required-semantic-cut-1209` at `19df93d325d7c6d41a457ddbe357bc042ae200ab`.

## Review

The completed 1218 diff is exactly the intended two-file scope:

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py`

The production correction checks key presence (`"mouth" in params`), so omitted `mouth` admits the default public motion path while explicit `None` and malformed/partial values fail closed to the private fallback. The existing public state mapping still maps `0.0` to `closed`, and the normal lipsync path still validates the existing ROI because it does not pass `allow_default_motion=True`.

The source-test correction builds public rows from the mutated case and the provider now asserts exact current props, basis, and requested frames. This addresses both findings in the 1212 review. The unchanged guards still reject stale/forged/partial/mixed rows and unknown public motion levels; existing assertions and the original integration markers/skips remain in place. No old public13/pixel/ROI re-review was performed beyond checking these unchanged hunks.

## Evidence

- `git -C /home/user/work/agent diff --check tl/vw-m3-d09-required-semantic-cut-1209..tl/vw-m3-d09-default-presence-fix-1218` — passed.
- Exact changed paths from that diff — the two files listed above, no others.
- Independent direct run from an isolated archive of the completed branch:

  ```text
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
  PYTHONPATH="$TMP:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -m integration \
    tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
    -k 'default_presenter_curve or explicit_invalid_presenter_mouth'
  ... 3 passed, 25 deselected in 5.44s
  ```

- Completed 1218 worker report: the targeted two-file plus neighbour run passed `31 passed, 2 skipped, 28 deselected`; the integration neighbour run passed `28 passed, 33 deselected`; Ruff, `py_compile`, and `git diff --check` passed. The two skips are the pre-existing motion-view markers for unavailable element maths; no new skip was added.

No full suite, browser, install, socket, physical, or product edit was performed by this review. The worker's first integration attempt encountered the known missing shared `remotion/node_modules` path, then the recorded rerun with the provisioned read-only runtime passed.

