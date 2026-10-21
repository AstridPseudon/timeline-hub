# Agent parent after-clip composition handoff

## Result

Composed the reviewed `9e24068c5` parent after-clip semantics onto the
current private `6a8dfb228` / existing `clip.add-media` source. The change is
Agent-only and uses the existing operation envelope and `select` carrier.

## Implemented

- A non-`parent` `clip.add-media` selection must be a raw
  `parent/clip:<id>` anchor.
- Capture resolves the original raw anchor before execution, clones its
  authored row, and changes only the reserved clip identity, effect identity,
  selected asset, and authored start. The new row is inserted immediately
  after the anchor.
- The inserted start is the raw anchor end using the canonical timeline span,
  with `max(0.05, span)`; later parent clips on the same track are shifted by
  that same amount. Other tracks, occurrences, placements, and shots remain
  untouched.
- Recording retains anchor row, owner/track, collection membership/order,
  parent output rate, source media binding, peer timing reads, and reserved
  created identities. Exact retries reuse the same command and IDs.
- Existing parent append, occurrence media, assembled replacement, inverse,
  reload, replay, and core v2 behavior remain on their existing paths.

The small `_recording.py` and `commands.py` adjustments allow the already
recorded after-selection to be reused by the structural birth and make prior
records available to distinguish assembled replacement from ripple birth.

## Scope controls

- No schema, operation, field, DTO, Runtime, App, generated client, package
  pin, endpoint, or activation changes.
- `astrid/core/timeline/schema/edit-command.schema.json` is unchanged;
  SHA-256: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
- No media authority is inferred from a mutable catalog, no silent append or
  whole-parent replacement was introduced.
- App2's ACK for the original source was not found; downstream App2 should
  request qualification against this new Agent source.

## Evidence

All commands ran in the worker worktree with the shared Agent venv and
Runtime import path:

```text
PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py
91 passed in 35.77s

PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_occurrence_media.py
64 passed in 8.99s

PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py -k 'after_capture_records_raw_anchor_media_rate_and_peer_reads or after_capture_refuses_a_missing_raw_anchor_without_appending or after_replay_refuses_changed_anchor_or_same_row_peer or after_replay_allows_disjoint_track_timing_and_preserves_exact_ids'
6 passed, 85 deselected in 2.34s

git diff --check
passed
```

No full, HTTP, browser, socket, or render suite was run.
