# Runtime carrier 051 final narrow review

Date: 2026-10-20 UTC

## Decision

**APPROVE — private M2 counterpart source only.**

This review does not approve public pinning, adoption, release, activation,
merge, or artifact authority. It does not run or claim the native `3730` pair.
Native `01455/29` and the group full-union qualification remain separate future
freeze work.

## Exact committed source

- Reviewed Runtime commit: `0511ba84d846f451111db628c52d25cf203c615a`
- Reviewed tree: `0a5bd960862875eac265deeedb543611675ca577`
- First parent/private carrier: `919c9017fda6b17d6e2420511fd588729b9e90e4`,
  tree `e9ec260a247bd44feef8ae996630d1a52a7a2497`
- Second parent/current source: `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`,
  tree `c225a680c645c67c3fe1f43b5e564b2a77a05d80`
- Current clip-test blob carried exactly:
  `183f14dbe64466c9a8c7aec5b34850da9272f107`

## Narrow diff and preservation checks

The exact `919..0511` delta contains only:

1. deletion of the accidentally committed product document
   `design/runtime-carrier-cas-text-current.md` (blob
   `91ef2683a7fc3bb8e200cfb78ec39ab34dc44845`), and
2. modification of `tests/test_timeline_clip_replacement.py` from blob
   `66a152346dde1fa0954bb95becb4958fe22370e3` to the required current blob
   `183f14dbe64466c9a8c7aec5b34850da9272f107`.

The four carrier helper/materialization tests and the 670-line ownership test,
plus `runtime_protocol/timeline_materialization.py`, are byte-identical from
`919` into `0511`:

- `tests/test_timeline_materialization_authority_review.py`
- `tests/test_timeline_materialization_continuation.py`
- `tests/test_timeline_materialization_join.py`
- `tests/test_timeline_projection_ownership.py`
- `runtime_protocol/timeline_materialization.py`

Compared with current `6ab`, all paths outside the established 17-path carrier
allowlist have zero blob mismatches. The candidate/current difference is the
expected 16 carrier paths (the accidental design document is absent from both
final/current trees), with the carried clip-test blob identical on both sides.

The required private contract remains exact:

- `contract/schemas/edit-command.json`: SHA-256
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`, 48
  `$defs` and 22 operation clauses;
- `runtime_protocol/schemas/timeline-commit-bundle.json`: SHA-256
  `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`;
- public floor fixture remains SHA-256
  `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`;
- the compatibility implementation and its tests are byte-identical to the
  independently reviewed `62b5f8e` repair.

No new product-side authority, caller-ID map, DTO, endpoint, route, version,
fake-birth path, skip, xfail, TODO, or HACK was added. The carried test
strengthens receipt/event and zero-write assertions; six simple assertion lines
are replaced by 36 assertion lines in the helper and neighboring cases. The
two added `pytest.mark.integration` annotations are ordinary routing markers
on the carried integration cases, not suppression markers.

## Evidence

Read-only source checks run for this review:

```text
git diff --check 919c9017fda6b17d6e2420511fd588729b9e90e4..0511ba84d846f451111db628c52d25cf203c615a
PASS

git diff --check 9f211fcdb66023a577a14111f99c87fb32ef573c..0511ba84d846f451111db628c52d25cf203c615a
PASS

blob comparison of candidate/current paths outside the 17-path carrier allowlist
PASS: 0 mismatches

retained carrier helper/materialization/ownership blob comparison
PASS: all five listed paths identical

compatibility source blob comparison against 62b5f8e
PASS: implementation and test blobs identical

private schema/bundle/public-floor SHA-256 and schema-shape checks
PASS: f802/48 definitions/22 clauses, bundle 3b17151, public floor a6f1aaa9
```

Inherited targeted evidence from the already-qualified source (not rerun here
to avoid duplicate qualification) is **164 passed, 20 deselected, 10 existing
strict xfailed**, plus generator, generator `--check`, artifact-manifest, and
`git diff --check` passes. No full suite and no duplicate `3730` native pair
were run.

## Required next step

Send this exact commit/tree/hash tuple to Agent for their narrow counterpart
review. After Agent ACK, coordinate exactly one `3730` native pair on this
committed source. Runtime must not run that pair itself. Keep public
pin/adoption/release held until those gates complete.
