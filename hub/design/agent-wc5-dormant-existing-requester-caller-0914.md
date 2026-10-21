# Agent WC5 dormant requester caller

Date: 2026-10-21 UTC

## Result

Added one private, deliberately dormant source adapter in
`astrid/packs/video_editing/shared/voiceover_requester.py`:
`_requester_sync_draft_voiceover`.

The adapter composes the existing seams only:

```text
containing operation's exact candidate/scripts/admitted_target
  -> _prepare_requester_speech_inputs
  -> existing client.tasks.create(action=video_editing.sync_draft_voiceover)
     with spec.runtime_dependencies.publication.admitted_target
     and execution_request.inputs[] / input_manifest exact mirror
  -> existing astrid.sdk.observe_task_invocation (read-only completion)
  -> existing managed authoring_proposal object read
  -> existing build_producer_batch validation
  -> TimelineSession.open
  -> TimelineSession.queue_proposal
  -> TimelineSession.flush (durable requester outbox acceptance)
```

The descriptor is passed as the existing `settled_speech_input` file input;
the ordered descriptor array and `input_manifest` are asserted identical.
The outer action remains `video_editing.sync_draft_voiceover`; inner speech
roots remain requester-owned through the reviewed helper. The outer proposal
identity is consumed from the worker's managed output and is not synthesized
or replaced by the requester. The adapter checks the existing four-field
`admitted_target` before queueing and passes the original base revision and
publication to `TimelineSession.open`.

No public/default caller was changed or enabled. `rg` confirms **live callers:
NONE**: the only references to `_requester_sync_draft_voiceover` are its
non-test definition and the compact fake-transport regression. The actual
non-test dormant chain is the source chain shown above, retained for later017
containing-operations proof. No new action, mode, DTO, Runtime endpoint,
store, worker root, commit, pin, generation run, or activation was added.

## Evidence

All commands were run from the worker worktree with shared Runtime source
read-only on `PYTHONPATH`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider \
  tests/packs/video_editing/test_voiceover_requester.py \
  tests/packs/video_editing/test_draft_voiceover.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py
91 passed in 7.68s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider \
  tests/editing_conformance/test_recipe_native_voiceover.py \
  tests/sdk/test_timeline_producer_guard.py \
  tests/sdk/test_timeline_sync.py \
  -k 'voiceover or producer or proposal or outbox'
32 passed, 81 deselected in 4.93s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider \
  tests/packs/video_editing/test_voiceover_requester.py::\
  test_dormant_requester_joins_outer_admission_and_existing_producer_outbox
1 passed in 0.87s
```

```text
/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/packs/video_editing/shared/voiceover_requester.py \
  tests/packs/video_editing/test_voiceover_requester.py
All checks passed!
git diff --check
passed
```

An initial collection attempt without the existing Runtime source on
`PYTHONPATH` failed before test collection with `ModuleNotFoundError:
runtime_protocol`; it ran no test body. The corrected commands above are the
evidence.

## Boundary / next step

The regression uses a fake admission, read-only observation result, managed
proposal bytes, and fake `TimelineSession` solely to prove orchestration shape.
It is not Runtime, HTTP, native worker, generation, render, pin, browser, or
full-suite qualification. The current Runtime source ACK approves the input
carrier only; later017 must supply the containing operation and any live
outer admission/acceptance qualification on the approved Runtime/Agent pair.
