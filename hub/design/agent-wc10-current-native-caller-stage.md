# Agent WC10 native caller stage

Status: **STAGED — HOLD / UNMERGED**

## Live caller changed

The only production caller changed is `astrid/sdk/remote.py:482-643`,
`RemoteTimelines.create_empty` and its two private native-result helpers.

It now:

- preserves the existing Runtime `create_timeline` shell call, including the
  caller-derived `-shell` idempotency key and project/timeline/name arguments;
- refuses noncanonical legacy config visibly before creating a shell; the
  accepted native input is the exact empty default `{"tracks": []}` (or
  omitted config);
- checks immutable timeline history for the caller-derived `-head` receipt;
- sends the existing raw `timeline.init` command through `TimelineSession` and
  returns its accepted receipt/result;
- leaves `TimelineSession`'s durable exact flight in charge of ambiguous
  retry, and replays the accepted init receipt rather than recapturing over a
  later edit or inverse;
- exposes Runtime conflict/refusal as a draft failure and contains no
  `publish_parent_composition` call or automatic legacy fallback.

The existing first-clip client journey was retargeted to call this public
creator and assert the native init history entry before first track/clip,
reload, inverse, and redo.

## Direct evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/v10/test_timelines_create.py tests/sdk/test_timeline_create_native.py tests/editing_conformance/test_pristine_initialize.py`
  → **38 passed, 2 xfailed**. The two strict xfails preserve the old positive
  expectations while the old publisher-only fake/custom legacy canvas cannot
  satisfy the frozen native init schema.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_create_native.py tests/v10/test_timelines_create.py tests/editing_conformance/test_commit_runtime_first_clip.py`
  → **All checks passed**.
- The broader `ruff check` including `astrid/sdk/remote.py` reports 120
  pre-existing monolithic-file `E701`/`I001` violations; it was not used as a
  clean signal and no unrelated reformat was applied.
- The requested local integration test could not bind its daemon socket in the
  sandbox (`PermissionError: [Errno 1] Operation not permitted`).
- Central targeted request
  `agt-m2-wc10-current-native-caller-stage`, files
  `tests/editing_conformance/test_commit_runtime_first_clip.py tests/sdk/test_timeline_create_native.py tests/v10/test_timelines_create.py`
  → **setup failure**, `ModuleNotFoundError: No module named 'runtime_protocol'`;
  no product test result was produced.

## Hold condition and next evidence

Do not merge this migration yet. Normal installed-pair/launcher proof is still
absent: the corrected Runtime proof reached the installed launcher but stopped
at the pre-timeline project mutation because the fixture expected the existing
`result['data']` envelope. Runtime owns that fixture correction and the normal
source/schema/client-origin assertions. The custom-canvas positive also remains
absent because the frozen `TimelineInitArgs` schema cannot represent that old
config without introducing a forbidden new operation/schema change.

Next evidence is the reviewed Runtime correction run against the exact paired
source/schema/client, followed by the real native first-clip/reload/inverse/redo
journey. No App native-init activation or public schema/client byte change is
part of this stage.
