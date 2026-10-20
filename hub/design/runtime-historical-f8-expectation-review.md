# Runtime historical raw expectation review

Decision: **APPROVE**.

## Exact review scope

- Runtime review branch: `tl/rt-m2-review-historical-raw-test-f8`
- Review range: `a0d200358fe2eb4a7b84514149cce78a42176138..f8f775f41f5478e13c705f5646bfe534c2514b6d`
- Changed path in that range: `tests/test_timeline_public_s2_mixed_cli_journey.py`
- Reviewed hunk: `_views`, lines 209–217 at `f8f775f`.

The new expectation is strict for both accepted fixture shapes:

- a registered historical raw asset resolves from its required `object_id`;
- a registered literal asset resolves from its present `media_id`;
- a null source fails;
- the source must have exactly one equal `dependency_manifest.media[*].media_id`;
- a missing, duplicate, or mismatched manifest pin fails by assertion/unpacking;
- `projected["source_object_id"]` remains equal to that exact accepted pin.

There is no fallback to a generated/adopted ID, no pin synthesis, and no
projection change. The diff changes no authored, opaque, source-range,
timing, head, guard, path, body, key, receipt, retry, restart, undo, or
history assertion.

## Ancestor fixture review

The `a0d2003` ancestor changes are setup-only and remain outside the reviewed
expectation hunk. The genuine WAV is stored as a separate CAS object; the
historical parent is deep-copied into scoped child identities; the seed carries
the remapped media dependency edge; and the original archived timeline is
checked byte-for-byte through `verify_baseline(...) == old_baseline`.

The cloned raw registry continues to assert no authored `duration`, and the
fixture checks the cloned parent has the new audio `object_id` without changing
the original archived parent. The literal fixture remains independently
authored with its registered `media_id` and measured WAV duration. No media
adoption or original-film mutation was added.

## Evidence

- `git diff --check a0d2003..f8f775f` — passed.
- AST parsing of both touched test modules — passed.
- Central historical-only gate
  `rt-m2-historical-raw-view-source-assertion-raw27-historical-only-integration-1020190819-25828`,
  suite `raw27-historical-only-integration --files tests/test_timeline_public_s2_mixed_cli_journey.py`:
  **1 passed, 1 deselected, exit 0**.
- That gate used Agent `27e823a5ddeb4f8995c436b44c8d42f728350919` / tree
  `7f43878c1f37abf1a8bef6d79b44df51d1ced50a`, Runtime `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`,
  and normal producer/artifact `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` / `f021`.
- Literal qualification is separate evidence and was not relabeled as part of
  this historical-only gate. No full suite, unchanged-tree rerun, or new
  product qualification was run for this review.

No blocking finding. The exact source tuple is acceptable for merge.
