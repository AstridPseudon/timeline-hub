# Fix T1: canonical shared shot-layering fixture

PASS

The canonical fixture now has one current-shape composition graph per case:
top-level occurrence records carry `occurrence_id`, `shot_id`, `revision_id`,
`at_ms`, and `duration_ms`; child timelines are under each pinned shot
revision's `internal_timeline_revision.timeline`. Parent tracks and loose clips
are represented in `parent_composition.config`.

The focused test rejects recursive exact `UNKNOWN` values, rejects the old
`shots`/`loose_clips`/`main_tracks` case-input shape, validates occurrence and
revision/timeline links, and asserts the seven settled cases and expectations:
above/below/same row, transparency, suffix tracks, multiple occurrences,
merged audio, namespaced visual groups, and missing-row fallback warning.

Updated canonical fixture SHA-256:

`3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e`

T2/T3 must vendor this exact file byte-for-byte and pin this digest in their
consumer tests. Runtime production code does not load this conformance fixture;
the Runtime test reads it directly from the checked-in conformance path.

Checks:

- `python -m pytest -q --basetemp=/tmp/w-47d479135f-shot-layering-final.jJBs5V tests/test_shot_layering_fixture.py` — `3 passed, 1 warning` (existing `Unknown config option: timeout` warning).
- `git diff --check` — passed (no output).
- Read-only cross-check: `PYTHONPATH=/home/user/work/agent python -c '...parse_shot_composition...'` — all 7 case inputs accepted by Agent's canonical validator.
