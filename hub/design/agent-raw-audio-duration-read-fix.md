# Agent raw-audio duration-read correction

Status: corrected Agent source on `tl/agt-m2-raw-audio-duration-read-fix`, based
on `8f15518e` (tree `721d3f14`); Runtime pairing remains held pending the
committed and independently approved single-FD counterpart.

## Exact source change

- `astrid/sdk/timeline/_trim_commands.py:24-52` retains the existing authored
  `trim.source` dependency and uses the exact source `media_id`/digest pin for
  `Recording.read_media(..., ['duration_seconds'])`. The returned positive or
  absent tagged state is the value used for source-end/default validation.
- `astrid/sdk/timeline/_recording.py:101-140` is the private request-scoped
  media-read seam. It accepts only an exact raw pin, rejects selection-bearing
  metadata, and records the read as an ordinary command read:

  ```json
  {
    "ref": "media:sha256:<digest>",
    "path": ["duration_seconds"],
    "state": {"state": "present", "value": 8}
  }
  ```

  Runtime metadata without a usable duration is recorded as
  `{"state":"absent"}` before the existing positive-number validator refuses
  the trim, so the refusal remains zero-write. No command field, DTO, store,
  registry duration, or public endpoint was added.
- `astrid/sdk/timeline/commands.py:156-167` verifies media reads before the
  handler during replay/accept. `astrid/sdk/timeline/inverse.py:349-363,444-447`
  preserves authored inverse guards while intentionally not re-probing a
  transient Runtime metadata read during undo.

## Counterexample closed

Before this correction, capture with the same raw pin and
`duration_seconds: 8` recorded `trim.source` but no duration read. Replaying
with the same pin and `duration_seconds: 7` therefore succeeded and changed
the trim from `0..8` to `0..7`. The new permanent regression
`test_raw_audio_trim_replay_refuses_changed_request_duration_before_writes`
proves the replay fails with `dependency_changed` (`original media read
changed`) before any write. The positive test also proves the exact read claim,
same-value replay, and inverse restoration.

## Evidence

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_clip_trim.py` — **122 passed**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/timeline/test_cli_commit_trim.py tests/sdk/test_timeline_commit_provider.py` — **126 passed**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_parent_media.py` — **25 passed**.
- Changed-module `py_compile` — passed; `git diff --check` — passed.

No full suite, browser/socket suite, actual raw legacy Agent/Runtime pair, or
Runtime test was run here. Do not consume rejected Runtime `ab4c`; coordinate
only after corrected single-FD `e220...`/`89fb...` is committed and independently
approved.
