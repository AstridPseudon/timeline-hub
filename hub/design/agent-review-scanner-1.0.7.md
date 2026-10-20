# Agent review: owner film clip-look scanner 1.0.7

Reviewer: Agent worker `agt-review-scanner-107` (2026-10-20). Review only; no
repository code changed, nothing pushed or merged.

## Verdict

**REJECT** for the exact artifact below. The candidate still reports malformed
look and audio-fade values as `status: complete`, contrary to the handoff rule
that malformed metadata must produce `incomplete`/error rather than a clean
result or silently dropped row.

## Artifact and flat-copy verification

- Archive: `artifacts/owner-film-viewing-tools-v1.0.7.tgz`
- Archive size: `15630` bytes
- Archive SHA-256: `baf2fd28f96670b02e4dc63e21bc680e2ab0339a97671515d79ab91f9cbd3e27`
- The archive was opened with Python `tarfile` in memory only; it was never
  extracted or executed in place.
- Members were copied to a fresh scratch directory and compared byte-for-byte
  with the flat `design/handoff-viewing-scanner-final-1.0.7-*` copies. All four
  matched:
  - `owner_film_cliplook_scan.py`: 34,961 bytes,
    `f195b21e05fc0f76f0483270ae77a3198926535f6ea83e5fb784a85be84b6480`
  - `tests/test_owner_film_cliplook_scan.py`: 26,401 bytes,
    `074ffcb9c140e87661aa5b82ac9e57e30776be05e29b288bc7ec956e91e1e51a`
  - `tests/conftest.py`: 385 bytes,
    `ea7d84927b97d78e2eb17fa87180ce2b7591f2c53645d1799b99f2c34197e430`
  - `README.md`: 5,795 bytes,
    `ef85115a1d294ae2cc46c9ad88b1f9346508bbad065e0b11977e914915300819`

The flat metadata has a packaging inconsistency: its `source_archive` and
`source_sha256` still identify the 1.0.6 archive, although its 1.0.7 archive
entry and member hashes are correct.

## Test run

Command, from the fresh scratch copy:

```text
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --agent-root /home/user/work/wt/agt-review-scanner-107 -q tests
```

Result: **40 passed in 8.78s**.

The fuzz harness wrote 10 JSON variants for each of 13 authored look,
transition, and audio-fade fields (130 variants total) under the worker
scratchpad, then scanned each with the same interpreter and Agent root. The
structurally malformed transition variants failed closed, but the following
malformed look/fade inputs did not:

- `parent_revision.payload.clips[0].entrance = "BAD_ENTRANCE"`: `status:
  complete`, `closure_errors: []`, and a `known` entrance inventory/finding.
- `parent_revision.payload.clips[0].entrance = ["BAD_ENTRANCE"]`: same wrong
  complete/known result.
- `parent_revision.payload.clips[0].opacity = true`: `status: complete`, no
  error, and the affected `opacity` is silently absent from the element
  finding.
- `parent_revision.payload.clips[3].params.fadeIn = "BAD_FADE"` and
  `[...] = ["BAD_FADE"]`: `status: complete`, no error, while the scanner
  emits a `known` `continuous_audio_fade` finding for the malformed value.
- `parent_revision.payload.clips[3].params.fadeInCurve = ["BAD_CURVE"]`:
  `status: complete`, no error, while `curve_honoured` is emitted as
  `knowledge: unknown` instead of making the closure incomplete.

The same pattern was reproduced across the 10-variant fuzz sets for visual
entrance/exit and crop values. Free-form string-valued transition mappings
were not counted as defects because the candidate explicitly permits those
IDs/types unchanged; list/non-dict transition values did fail closed.

## Regression checklist

The following prior 1.0.5/1.0.6 requirements pass in the 40-test suite and
source review:

- audio-fade findings retain openable parent and occurrence-child source paths;
- malformed transition values produce bounded closure errors;
- duplicate internal revision IDs make the closure incomplete rather than
  selecting one row;
- the scanner calls the single Agent projector;
- output is bounded to IDs/pins/properties/paths/ranges/classifications;
- canonical incoming transitions and explicit `asset=None` clears are kept;
- `curve_honoured` is emitted only for a present, non-linear curve;
- element/look overlap includes clips across tracks with half-open intervals.

## Blocking defect and likely fix

This is a concrete fail-open, not a stylistic concern. The scanner's
`_unreadable_look_names` probes `FieldSpec.stored_at` only, so audio fades in
`stored_at_audio` are never checked. The audio path then reads raw values and
only downgrades an invalid curve to `unknown` without adding a closure error.
For visual animation/number fields, the human-form `clip_fields.describe`
path can accept or normalize malformed stored values without raising, so the
scanner treats them as known or drops them as defaults.

The scanner should validate every declared stored field with the Agent codec,
including the audio-specific paths, and add only bounded authored source-path
errors for invalid values. Add regression cases for malformed strings, lists,
and non-dict values for each look/fade family; retain the existing allowance
for free-form transition strings/mappings if that policy remains settled. Fix
the 1.0.7 metadata's stale 1.0.6 source fields as part of repackaging.

## Not verified

- No owner-film canonical closure was supplied, so no owner-data run was made.
- No full Agent suite was run; the exact delivery test suite above was run.
- No macOS claim.

**REJECT**
