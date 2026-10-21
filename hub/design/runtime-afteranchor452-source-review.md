# Runtime after-anchor source review — Agent 452eceb

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK** for Agent `452eceb391408185bfcc0c9e029e271d0ae3a229`.

This is a bounded source/schema peer ACK only. It confirms that the existing
`clip.add-media@1` carrier can carry an after-anchor video raw-window row whose
`hold` is absent or explicit `null`, while ordinary parent append/replacement
and `clip.add` remain positive-hold-only. It does not qualify a Runtime
acceptance path, native Agent/Runtime pair, App caller, publication, pin,
generation, activation, or writer retirement.

## Exact source identity

- Commit: `452eceb391408185bfcc0c9e029e271d0ae3a229`
- Parent: `a905fa29b1bb47739df438f4203ed987be588e46`
- Commit tree: `18fc7e0b1cde4df1a24637509fa14b2351340c9e`
- Parent tree: `5871915b4ed820e1a9c17a44f20ffd683f05df8c`
- Changed paths are exactly:
  - `astrid/core/timeline/schema/edit-command.schema.json`
  - `astrid/sdk/timeline/native_parent_media_commands.py`
  - `tests/editing_conformance/test_recipe_m2_parent_media.py`
  - `tests/sdk/test_timeline_materialization_schema_union.py`

Changed-file SHA-256 values match the source report:

```text
astrid/core/timeline/schema/edit-command.schema.json        e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da
astrid/sdk/timeline/native_parent_media_commands.py         935fab0dac38b4d6f4b16cb7f3254d1624496931e6425b93e07e6b9f0e367f16
tests/editing_conformance/test_recipe_m2_parent_media.py    f1860f7bb447438de52981fc70ab833c686d4b94b5adcfdfc8519554671e6c9d
tests/sdk/test_timeline_materialization_schema_union.py     8b12ba5b7b64c11dbebc55452c819dab7dee3387a84482558b2fe9c2c720ba82
```

## Schema and floor identity

The current Agent schema is raw SHA-256
`e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da`, and its
existing test serialization/canonical floor is
`0e4e3e78e3c80dafd79bc47ccf98100525c72c98ecb4c189d19b8ac6bcc46314`.
Inventory is **62 definitions / 36 closed operation clauses**.

The existing floor helpers reconstruct these unchanged floors:

```text
ordinary source       6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
private S2             f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f
private carrier        613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3
project data           39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d
groups                 27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb
voiceover              65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e
extent                84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5
remove                c49a6058cfb49fec3dd12e8d93868de6433f121b07a56a943257e34b239f9b7c
track mute            0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890
opacity               9b4f16f87fffc00da010e2dbea469ca6bfc021695c5b453c821d1d4553336708
full move set         ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7
literal union         da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068
reference/order       c47a00135a2beb9df35cbbf201ef6b7f900904f4afeb74efe3cf12871271598e
```

Unchanged fixture goldens are
`recipe_m2_parent_media.json` =
`22f1d1e94f3fbfada8cfc37519c30cfc96024a5a9a03a927a79a8ffcc85415b5` and
`recipe_m2_clip_add.json` =
`cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff`.

No frozen schema or fixture was edited. No Runtime/generated DTO path is in
the changed-path set, and `afterClipId` is absent from the Agent schema and
the source diff.

## Contract review

`ClipAddMediaArgs.row` retains the original positive-hold row branch and adds
only the minimal row alternative with `hold` absent or `null`. JSON Schema
cannot distinguish `select: parent/clip:<id>` from ordinary append at the row
definition, so the native handler supplies the operation-context guard:

- `raw_window` is true only for a non-replacement after-anchor selection.
- Missing/null hold is rejected before `_clip` for ordinary append and
  replacement.
- `_clip` derives `to - from` only when the raw-window branch is video; image
  rows still require a positive hold.
- The existing positive numeric check rejects zero, booleans, non-finite and
  malformed ranges/speeds.
- `clip.add` continues to use the unchanged `ClipAddArgs` row schema with
  required positive `hold`.

The existing after-anchor source clone, `max(0.05, timeline_duration)` floor,
speed-aware placement, same-track ripple, source-window preservation, opaque
row preservation, raw anchor/media/order selections, and inverse/replay guards
remain in place. The focused tests exercise both mirror compilations and
final mirror equality.

Live callers of this successor's new absent/null after-anchor capability:
**NONE**. Existing internal Agent capture/auto-placement call sites are
pre-existing and unchanged; no App, Provider/session, Runtime, pin,
generation, activation, publication, or public-artifact caller changed.

## Evidence

Exact source/import/collection preflight passed: target identity and four-path
diff matched, the Agent schema imported with 62 definitions/36 clauses, the
parent-media test module imported, and `git diff --check` passed.

Focused after-anchor and guard nodes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k 'birth_after_a_boundary or after_capture_records_raw_anchor_media_rate_and_peer_reads or after_capture_refuses_a_missing_raw_anchor_without_appending or after_anchor_reconstructs_missing_or_null_video_hold_in_source_units or after_anchor_explicit_zero_hold_refuses_atomically or ordinary_parent_media_birth_keeps_positive_hold_requirement or after_replay_refuses_changed_anchor_or_same_row_peer or after_replay_allows_disjoint_track_timing_and_preserves_exact_ids'
12 passed, 84 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k 'refusals_preserve_input or ordinary_parent_media_birth_keeps_positive_hold_requirement'
24 passed, 72 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_add.py -k 'invalid_rows_refuse_without_mutation or required_complete_row_and_closed_args'
20 passed, 34 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py -k 'only_carrier_additions or literal_three_union_reconstructs_each_reviewed_source_floor or complete_reviewed_private_s2_is_preserved_without_a_copied_frozen_schema'
3 passed, 22 deselected
```

A direct Draft 2020-12 preflight accepted after-carrier missing/null/positive
rows, refused after-carrier zero/bool rows, refused `clip.add` missing/null/
zero/bool rows, reported 62/36 schema inventory, found no `afterClipId`, and
found no Runtime/generated DTO changed path.

No full suite, Runtime/App acceptance, native/socket/browser/render,
generation, pin, registration, activation, or publication run was requested
or performed. Published014 cannot accept this future source until the matching
normal Runtime schema generation/contract is supplied.

## Recommendation

Retain the Agent source successor and this bounded SOURCE ACK. Runtime should
regenerate or otherwise match the private schema only in a separately reviewed
counterpart; then perform the explicitly requested matched Agent/Runtime
qualification. Do not infer public/published014 acceptance from this source
review.
