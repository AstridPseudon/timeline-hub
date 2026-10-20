# Agent parent `afterClipId` private source proposal

Published 2026-10-20 23:09 UTC for App2 and Runtime review. This is a private
source handoff only; it is not a schema freeze, Runtime pin, App activation, or
public release.

## Exact source

Base branch: `tl/agt-m2-track-mute-full-source-compose`

Base commit: `1c18c8c84cec366ce683349858fb2399435c9265`

Worker source patch SHA-256 (binary diff against that base, limited to the four
files below):

`62ab66f5c00cc8614ce13dfac2c6bf405cefb1ad4e29c25d29af5088e80b58d5`

Changed source and file SHA-256:

- `astrid/sdk/timeline/native_parent_media_commands.py` — `088b1d3a268907d6c9732149c6867806545e34110f5c05369755de0f92ce41ce`
- `astrid/sdk/timeline/_recording.py` — `0b2a55f46f5842a94875be6bd9894f8204a17def3b059393a9850676e2813efb`
- `astrid/sdk/timeline/commands.py` — `1e05b7d5fc0ed1c913c4277254e0b8504a4e5e31df8d2f544768f05e6c1e4685`
- `tests/editing_conformance/test_recipe_m2_parent_media.py` — `1edbecbde696c326b0c464628e8ef4c565f9b934d9d9582ca1c71edf082fba43`

The canonical schema is unchanged. Its full ordinary/group/transition/mute
source SHA-256 remains:

`astrid/core/timeline/schema/edit-command.schema.json` —
`21f313a7005f94a2525013ab9fd628afa626a7886bc098840a73ac012c0fcac2`

## Proposed carrier semantics

The existing `clip.add-media` command carries the declared parent insertion
intention in its existing `select` field:
`parent/clip:<raw-anchor-id>`. The standalone after-anchor capture clones the
raw anchor row and changes only the reserved destination `id`, effect identity,
asset alias, and authored start. It records the raw anchor entity, source
asset binding, source track, parent output rate, complete parent clip
membership/order, and each later row's track/timing reads in the same
recorder. It creates the row immediately after the anchor and shifts later
rows on that same track by `max(0.05, raw source timeline span)`. Other tracks,
occurrences, source metadata, and parent ownership remain untouched.

Missing or changed anchor/order/peer timing fails visibly. A disjoint-track
timing change replays successfully. Exact inverse, retry, identity collision,
and reserved asset/clip identities use the existing recorder and guarded
inverse machinery. Existing replacement capture is recognized by its preceding
`timeline.assembled-target` command and remains non-ripple.

No new DTO, endpoint, store, generation/pin/publication field, or schema field
is proposed. App2 should adapt its existing parent media producer only after
reviewing this source and the executable conformance tests; Runtime should
review the unchanged command/schema contract before any freeze.

## Executable evidence

- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py -k 'birth_after_a_boundary or after_capture or after_replay'` — 7 passed.
- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/editing_conformance/test_recording_clear.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py` — 267 passed in 182.72s.
- `git diff --check` — passed.

No full suite, browser, live socket, Runtime, or App qualification is claimed
by this handoff.
