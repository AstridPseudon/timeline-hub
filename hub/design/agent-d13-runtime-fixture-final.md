# Agent D13 runtime fixture final

## Exact skip removal

In `tests/packs/video_editing/test_runtime_publication_chain.py`, removed the
environment-dependent conditional `pytest.skip` that checked `ffmpeg`,
`ffprobe`, and `node` before the registered native final-render test.

## Replacement and lane behavior

The final-render test now imports and calls the existing
`tests.helpers.runtime.use_runtime()` helper at its start. That helper uses the
existing `tests.lanes.unavailable` convention: a missing required Runtime is a
visible failure when the named integration lane selects `integration`, while
non-required runs retain the established optional guard behavior. No
`ImportError` catch or new skip was added. Existing optional guards elsewhere
were not broadened.

## Mandatory run

Named central suite, restricted to the two original integration test IDs:

```text
registered-native-render-integration
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

Result: `2 passed in 152.68s (0:02:32)`.

The run used the provided `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`,
current pinned Node, private current Remotion project, and the central
`venv-agent-child-s2` environment.

## Source limits

Only the test fixture file was changed in this worker. Product source and the
reviewed D13 runtime/renderer/host/epoch/fence/proposal implementation were not
modified. The legacy refusal/artifact-preservation test and the native
assemble, lost-ACK restart, revision-pinned render, MP4 decode, and undo
assertions remain unchanged.

## Additional evidence

The affected legacy refusal test passed directly: `1 passed in 0.74s`.
`git diff --check HEAD` passed. No full suite was run.
