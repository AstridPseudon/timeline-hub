# App2 after-anchor 452 dormant parity delta review

Date: 2026-10-21 UTC

## Verdict

**APPROVE** the exact completed dormant App delta at App commit
`91927b3cfc613ef395927e5de04cca51b8a678bc`, tree
`2c0781c72e3a6d5d5fb2ddc50302c2501d32daff`, parent/base
`bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`.

This approval is source/parity-only. It does not authorize an App caller,
provider/session activation, Runtime/generated schema or pin, native/HTTP
qualification, publication, generation, or writer retirement.

The Agent prerequisite is the exact source-approved candidate
`452eceb391408185bfcc0c9e029e271d0ae3a229`, tree
`18fc7e0b1cde4df1a24637509fa14b2351340c9e`. Its four changed paths and
changed-file hashes are the ones in the retained Agent source review:

```text
astrid/core/timeline/schema/edit-command.schema.json
  e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da
astrid/sdk/timeline/native_parent_media_commands.py
  935fab0dac38b4d6f4b16cb7f3254d1624496931e6425b93e07e6b9f0e367f16
tests/editing_conformance/test_recipe_m2_parent_media.py
  f1860f7bb447438de52981fc70ab833c686d4b94b5adcfdfc8519554671e6c9d
tests/sdk/test_timeline_materialization_schema_union.py
  8b12ba5b7b64c11dbebc55452c819dab7dee3387a84482558b2fe9c2c720ba82
```

The Agent raw schema hash is
`e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da`; its
canonical test serialization hash is
`0e4e3e78e3c80dafd79bc47ccf98100525c72c98ecb4c189d19b8ac6bcc46314`.
The unchanged parent-media and clip-add fixture hashes remain
`22f1d1e94f3fbfada8cfc37519c30cfc96024a5a9a03a927a79a8ffcc85415b5` and
`cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff`.

## Exact App delta

Only these two paths changed from App base; the branch diff is 46 insertions
and 19 deletions:

```text
src/tools/video-editor/commands/parentClipAddCapture.ts
  6e036a410faea95f3104e602d19285b904975f85f29f9eb7c6af3d66541411a6
src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts
  9415a4ea8ff89c2fc3fa4348d1657c773f0315cb9a67b9d090d24da6ac82fc03
```

The product change is row-local: after-anchor `clip.add-media` accepts a
missing or explicit-null raw video `hold` through the existing raw-window
validator; that validator derives source duration from `to - from`, then
placement divides by the authored speed. The cloned raw row preserves the
absent/null field. Non-null holds still use the existing positive finite
check. Ordinary parent append remains strict.

The direct delta tests cover:

- `preserves a missing raw video hold and derives placement from source seconds`
  and the explicit-null parameterization (test lines 209-231);
- `refuses a missing/null non-video after-anchor hold without mutation` (233-246);
- `keeps a missing/null ordinary parent birth strict` (248-259);
- explicit zero refusal and the existing positive sub-0.05 floor (276-295);
- complete baseline command/record equality, ordered reads, selections,
  bindings, writes, created asset/clip IDs, and both derived mirror writes
  (59-174, including `derived_writes` entries at 132-135);
- JSON reload, reserved identity/ownership and selection guards (176-195),
  source transition/opaque preservation (197-207), and the existing
  execute/replay parity checker (310-355).

The Agent-side changed test IDs inspected were
`test_after_anchor_reconstructs_missing_or_null_video_hold_in_source_units`,
`test_after_anchor_explicit_zero_hold_refuses_atomically`,
`test_ordinary_parent_media_birth_keeps_positive_hold_requirement`,
`test_after_capture_records_raw_anchor_media_rate_and_peer_reads`,
`test_after_replay_refuses_changed_anchor_or_same_row_peer`,
`test_after_replay_allows_disjoint_track_timing_and_preserves_exact_ids`,
`test_exact_capture_replay_scoped_birth_and_inverse`,
`test_asset_alias_inverse_is_guarded_by_dependents_and_aba`, and
`test_literal_three_union_reconstructs_each_reviewed_source_floor`.
The retained Agent source review also records the 7-control adversarial
probe and natural two-mirror probe. I did not replay the retained 150/59
lanes or any broad suite.

The Agent handler explicitly computes `raw_window` only for a non-replacement
after-anchor selection; ordinary append and assembled replacement retain the
positive-hold requirement. App has no assembled-target/clip.add-media
replacement caller in this dormant delta. Its separate existing
`clip.swap-media` path is unchanged and is not evidence of activation.

## Caller and boundary checks

`git grep` over candidate `91927b3cf` found no non-test caller of
`captureParentClipAddMediaAfterAnchor`,
`finishParentClipAddMediaAfterAnchor`, or
`executeParentClipAddMediaAfterAnchor` after excluding their declaration and
direct test file. The only `afterClipId` occurrence newly relevant to this
review is the existing negative assertion; no wire field, cast, manual
generated edit, Provider/session path, or UI activation was added. Existing
unrelated prepared-media `afterClipId` APIs remain outside this dormant delta.

No assertion was removed or weakened, and no `it.fails`, skip, or expected
failure was added. The App delta is limited to the helper and its direct
test, as required.

## Verification

I ran the exact candidate snapshot from an isolated temporary extraction with
the shared `node_modules` symlink read-only and Vitest cache disabled:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts
```

Result: **2 files, 18 tests passed**. The parity export contained 10 samples:
6 accepted (including one absent-hold and one null-hold raw-video sample) and
4 refused.

Retained source evidence, not replayed here: Agent source review 16 focused
tests plus 7 adversarial controls and mirror probe; the prior App parity
review's exact Agent comparison; and Runtime's bounded source ACK. No full,
browser, socket, HTTP/native Door, generation, pin, or public qualification
run was performed.

## Decision and next step

The exact dormant App candidate is approved for the source ledger and may be
merged as-is. Keep it dormant until a separately reviewed compatible normal
Runtime/generated counterpart and matched native qualification exist. The
stale prose in the direct test's unchanged baseline/parity comments still
names the older `3b3208c43` in places, while the parity checker output names
Agent452; this is documentation-only and does not alter the approved bytes or
behavior.

Commit message path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-afteranchor452-dormant-delta-review-0516/commit-msg`.
Completion marker: `DONE` in the same worker directory.
