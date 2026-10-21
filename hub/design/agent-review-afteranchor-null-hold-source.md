# Agent after-anchor missing/null-hold source review

Date: 2026-10-21 UTC

## Verdict

**APPROVE SOURCE** for the private Agent successor at the exact final
harness commit below. This approves the bounded source/schema correction only.
It does not approve an App or Runtime consumer, a generated/public schema or
pin, activation, publication, HTTP/native Door qualification, or a native
pair.

## Exact reviewed identities

- Final harness commit: `452eceb391408185bfcc0c9e029e271d0ae3a229`
- Final tree: `18fc7e0b1cde4df1a24637509fa14b2351340c9e`
- Parent/base: `a905fa29b1bb47739df438f4203ed987be588e46`, tree
  `5871915b4ed820e1a9c17a44f20ffd683f05df8c`
- Immutable old Agent comparison: `3b3208c43903b770010de0649691cfa566447822`,
  tree `84120e176540fbc2281dcff4b7186ec8ae413274`

The old `3b3208c43` source was read with `git show`; it was not modified. The
successor diff has exactly these four paths:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `astrid/sdk/timeline/native_parent_media_commands.py`
- `tests/editing_conformance/test_recipe_m2_parent_media.py`
- `tests/sdk/test_timeline_materialization_schema_union.py`

Changed-file SHA-256 values match the worker handoff:

```text
edit-command.schema.json                 e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da
native_parent_media_commands.py          935fab0dac38b4d6f4b16cb7f3254d1624496931e6425b93e07e6b9f0e367f16
test_recipe_m2_parent_media.py           f1860f7bb447438de52981fc70ab833c686d4b94b5adcfdfc8519554671e6c9d
test_timeline_materialization_schema_union.py
                                          8b12ba5b7b64c11dbebc55452c819dab7dee3387a84482558b2fe9c2c720ba82
```

Schema identity is raw SHA-256 `e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da`;
the canonical formatted schema hash is
`0e4e3e78e3c80dafd79bc47ccf98100525c72c98ecb4c189d19b8ac6bcc46314`.
Unchanged parent-media and clip-add fixture hashes are
`22f1d1e94f3fbfada8cfc37519c30cfc96024a5a9a03a927a79a8ffcc85415b5` and
`cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff`.

## Contract findings

- `ClipAddMediaArgs.row` keeps the original positive-hold `$ref` as its first
  alternative and adds only a minimal raw-row alternative for the private
  after-anchor carrier. The alternative requires `id`, `clipType`, `track`,
  and `at`; `hold` may be absent or null, but an explicit zero matches neither
  alternative. `clip.add` still uses the unchanged positive-hold
  `ClipAddArgs` schema.
- The handler sets `raw_window` only for a non-replacement after selection.
  Missing/null hold is rejected before `_clip` for ordinary append and
  replacement. The existing `_clip(raw_window=True)` derivation is reached
  only for a verified video kind and computes source seconds as `to - from`;
  image and verified-image generic `media` rows still refuse missing/null
  hold. No caller-supplied duration is authoritative: capture clones the raw
  anchor row and derives its start from the anchor's authored start, source
  duration, and speed. Tampering with the captured source window is refused.
- Verified media remains the exact Runtime selection. The parent output rate,
  raw anchor row, source asset, after-anchor membership/order, same-track peer
  rows, and reserved asset/clip identities are read or bound before writes.
  The ripple is `max(0.05, clip_timeline_duration(source))`, preserving source
  units and speed-aware placement; other tracks and occurrences remain
  untouched. Cloned opaque/metadata fields remain source-owned.
- Both mirror writes are natural recorder writes: the first is the
  pre-create peer-ripple compilation and the second is the final compilation
  after the new birth. No synthetic recorder repair was added.
- Existing inverse/replay/identity-guard code is unchanged. The focused
  after-anchor controls retain exact inverse behavior, retry identity, anchor/
  peer/order refusal, disjoint-track rebase, and the existing parent-media
  dependent/ABA guards. The successor does not silently upgrade the old
  capture path.
- The schema-floor helper strips only the new after-anchor alternative. The
  retained 150 parent-media/clip-add results and 59 schema-union results from
  the worker handoff remain the applicable floor evidence; the exact
  three-union reconstruction node also passes independently below.

## Evidence run for this review

All commands were read-only with shared dependencies untouched:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  'tests/editing_conformance/test_recipe_m2_parent_media.py::test_after_anchor_reconstructs_missing_or_null_video_hold_in_source_units' \
  tests/editing_conformance/test_recipe_m2_parent_media.py::test_after_anchor_explicit_zero_hold_refuses_atomically \
  'tests/editing_conformance/test_recipe_m2_parent_media.py::test_ordinary_parent_media_birth_keeps_positive_hold_requirement' \
  tests/editing_conformance/test_recipe_m2_parent_media.py::test_after_capture_records_raw_anchor_media_rate_and_peer_reads \
  tests/editing_conformance/test_recipe_m2_parent_media.py::test_birth_after_a_boundary_keeps_it_until_an_explicit_delete \
  'tests/editing_conformance/test_recipe_m2_parent_media.py::test_after_replay_refuses_changed_anchor_or_same_row_peer' \
  tests/editing_conformance/test_recipe_m2_parent_media.py::test_after_replay_allows_disjoint_track_timing_and_preserves_exact_ids \
  tests/editing_conformance/test_recipe_m2_parent_media.py::test_exact_capture_replay_scoped_birth_and_inverse \
  'tests/editing_conformance/test_recipe_m2_parent_media.py::test_asset_alias_inverse_is_guarded_by_dependents_and_aba' \
  tests/sdk/test_timeline_materialization_schema_union.py::test_literal_three_union_reconstructs_each_reviewed_source_floor
```

Result: **16 passed in 2.58s**. The selected nodes covered missing/null video
source-window births, explicit-zero refusal, ordinary missing/null refusal,
media/rate/anchor/order reads, mirror behavior, exact inverse/replay, and the
schema floor.

The compact in-memory adversarial probe (same `PYTHONDONTWRITEBYTECODE`,
`PYTHONPATH`, and Agent venv) passed **7 controls**: image and generic
image-backed `media` missing/null refusal, caller source-window tamper refusal,
exact reserved IDs/read guards, and source-window floor placement.

The separate in-memory mirror probe passed: **two natural mirror writes** were
verified as pre-create ripple followed by final birth compilation.

Also passed during identity review:

```text
git diff --check HEAD^ HEAD
```

No full suite, matrix, native/Door, HTTP, browser, render, activation, pin,
generation, or public artifact test was run or claimed. No product edits were
made by this review worker.

## Handoff

The source successor is approved for the manager's source ledger. Keep it
dormant until separately reviewed compatible App/Runtime sources exist and
their normal qualification proves the pair; this source review alone does not
authorize a consumer pin or public schema activation.
