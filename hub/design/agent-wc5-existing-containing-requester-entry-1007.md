# Agent WC5 existing containing requester entry

Date: 2026-10-21 UTC

## Result

Closed reviewer0957's source reachability gap with one dormant private join in
the existing `astrid/packs/video_editing/shared/draft_voiceover.py` core:
`_sync_draft_voiceover(..., requester_entry=True)` at lines 735-798.  After
the normal pinned composition/script read and ordinary `plan_draft_voiceover`
plan, the private branch forwards the exact candidate and script mapping plus
the current four-field target (`project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`) to the reviewed
`_requester_sync_draft_voiceover` adapter.  It also forwards the existing
settings, selection/adoption choices, timing policy/padding, and outbox path.

The requester adapter remains the source of the real outer chain:

```text
_prepare_requester_speech_inputs
  -> existing task admission for video_editing.sync_draft_voiceover
     with execution_request.inputs[] / input_manifest mirror
     and runtime_dependencies.publication.admitted_target
  -> read-only outer observation and managed authoring_proposal
  -> build_producer_batch
  -> TimelineSession.queue_proposal
  -> TimelineSession.flush
```

The inner `generation.generate_speech` identity remains requester-owned.  The
outer action identity remains `video_editing.sync_draft_voiceover`; the outer
proposal is read from its managed output and is not synthesized or replaced.
The original base revision/publication pair is passed unchanged to the
requester adapter and then to the existing Timeline outbox session.

The branch is dormant: the public `sync_draft_voiceover` wrapper and the
managed action call `_sync_draft_voiceover` without `requester_entry`, so no
live caller was changed and the current public path remains intact.  The
future containing release must supply the internal requester entry and then
qualify the real Runtime workflow; this source branch does not claim HTTP,
native, worker, render, browser, install, pin, schema, or live qualification.

## Regression

`tests/packs/video_editing/test_draft_voiceover.py::test_private_requester_entry_forwards_current_target_and_source`
enters the existing private core (not the requester helper directly), verifies
the exact candidate/script/target/outbox handoff, proves the legacy bound
publisher is not used, and checks that a no-op plan still returns `unchanged`
without entering the requester branch.  The existing requester regression
continues to prove the admitted outer descriptor, managed proposal identity,
producer-batch validation, `queue_proposal`, and `flush` shape offline.

## Callers

- Dormant private source join: `_sync_draft_voiceover` ->
  `_requester_sync_draft_voiceover` (guarded by `requester_entry=True`).
- Live callers changed: **NONE**.
- No new public method/action/DTO/store/authority, Speech root, worker commit,
  Runtime route, pin, schema, or 017 widening.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider \
  tests/packs/video_editing/test_voiceover_requester.py \
  tests/packs/video_editing/test_draft_voiceover.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py
92 passed in 6.80s
```

```text
/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/packs/video_editing/shared/draft_voiceover.py \
  astrid/packs/video_editing/shared/voiceover_requester.py \
  tests/packs/video_editing/test_voiceover_requester.py
All checks passed!
```

`git diff --check`: passed.

The broader Ruff invocation including
`tests/packs/video_editing/test_draft_voiceover.py` reports 32 legacy style
violations across that compact-style file (mostly pre-existing); no unrelated
style cleanup was made.  No full suite, HTTP/native/live
socket, render/browser, install, or pin suite was run or requested.
