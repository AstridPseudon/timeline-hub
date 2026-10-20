# Independent Agent review: parent `afterClipId` source

**Result: APPROVE**  
**Reviewed:** 2026-10-20 23:13 UTC  
**Scope:** D01 source-only review of `tl/agt-m2-parent-afterclip-guarded-source` against `tl/agt-m2-track-mute-full-source-compose` (`1c18c8c84cec366ce683349858fb2399435c9265`).

The source patch is limited to the four files named by the handoff. The
canonical `astrid/core/timeline/schema/edit-command.schema.json` is byte-for-byte
unchanged; its SHA-256 is
`21f313a7005f94a2525013ab9fd628afa626a7886bc098840a73ac012c0fcac2` on both
base and source. The existing `clip.add-media` envelope and its existing
`select` carrier (`parent/clip:<raw-id>`) carry the behavior; no new API, DTO,
endpoint, store, freeze, or public artifact is introduced.

## Source contract review

- The raw parent anchor is required and is resolved as an explicit
  `parent/clip:<id>` reference. There is no display-ID or occurrence inference.
- The recorder captures the complete parent clip selection, including
  membership and order, plus the whole anchor row, source asset binding,
  parent output rate, track, verified media selection, and reserved asset/clip
  identities.
- The source clone matches Main's duplicate behavior: preserve the authored
  source row and opaque metadata; change only the reserved clip identity,
  effect identity, selected asset, and authored start/end-equivalent timing.
  The insertion is immediately after the anchor. Every later clip in the same
  track is read as a whole row and shifted by
  `max(0.05, source timeline span)`; other tracks and occurrence-owned data are
  untouched.
- The existing guarded inverse and rebase machinery consumes the recorded
  membership/order and read claims. Missing/changed anchor, order, track,
  rate/media binding, peer timing/extent, or identity is refused. Exact retry
  preserves the command and reserved IDs.
- The source's preceding `timeline.assembled-target` exception keeps explicit
  replacement non-ripple, matching the existing Main replacement path.

## Evidence

The handoff's reported focused 7-test and neighboring 267-test results were
accepted as prior evidence and not duplicated. I ran the decisive controls:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_m2_parent_media.py \
  -k 'after_capture_records_raw_anchor_media_rate_and_peer_reads or after_capture_refuses_a_missing_raw_anchor_without_appending or after_replay_refuses_changed_anchor_or_same_row_peer or after_replay_allows_disjoint_track_timing_and_preserves_exact_ids'
6 passed, 85 deselected in 1.16s
```

An inline Python control using the same fixture/recorder/replay helpers passed
both missing controls: changing a later same-track peer's `hold` (concurrent
extent) was refused, and adding a new same-track member was refused by the
recorded collection membership guard. A second inline control passed exact
inverse and refused inverse after that peer extent change.

A third inline control changed the raw anchor to a video span with
`from=2,to=6,hold=4,speed=2`; the inserted and shifted rows both used the
expected two-second timeline duration. This confirms the source-span/rate
calculation against Main's duration rule.

No product files were changed. No full, browser, live-provider, Runtime, or
App qualification suite was run. App/Runtime qualification remains open as
required by D01.
