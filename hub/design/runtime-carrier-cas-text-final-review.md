# Runtime carrier CAS/text final review

Date: 2026-10-20 UTC

## Decision

**APPROVE — private carrier source only, with required current-test carryforward.**

This approves the completed private composition for manager-to-manager review. It
does not approve native Agent/Runtime adoption, public pinning, release,
activation, merge, or the coordinated `3730` pair.

## Exact sources

- Completed composition: Runtime commit `919c9017fda6b17d6e2420511fd588729b9e90e4`,
  tree `e9ec260a247bd44feef8ae996630d1a52a7a2497`.
- Reviewed private carrier parent: `7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`,
  tree `d20b745c26a33c2ea4e20863f846335c8cf33e1e`.
- Current source parent: `9f211fcdb66023a577a14111f99c87fb32ef573c`,
  tree `d22726d982ac279277c4b0210495170556e3309d`.
- New current integration head: `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`,
  tree `c225a680c645c67c3fe1f43b5e564b2a77a05d80`.

The completed source is a true two-parent composition of the reviewed carrier
and current `9f`; it is not the current `6ab` tree and was not merged here.

## Review findings

- The `919` versus `9f` diff is exactly the established 17-path private-carrier
  allowlist. All current `9f` tracked blobs outside it match byte-for-byte.
- The private Agent schema remains the f802 source: command schema SHA-256
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`; the
  private bundle is `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`.
  The ordinary `0.2.14` 55-definition/29-operation source was not imported.
- The a51 selected-media CAS-byte helper and its tests are retained. The current
  unplaced-shot text service/tests are retained, including receipt-first exact
  retry and the original four positive text cases.
- The 81 catalog-promotion implementation and current-head fence are retained.
  The fence still checks the project-scoped `shot_revision_heads` at current,
  inverse-source, and accepted-historical-slot authorization sites, while the
  existing `_same_materialization_slot`/C4 proof remains in force.
- The c45 historical-render retry test and the current audit, empty-shell, and
  fresh-bootstrap guards remain outside the carrier allowlist unchanged.
- No new product authority, DTO, endpoint, schema fixture, skip, or xfail was
  found. The only added repository document is the intentional carrier handoff
  `design/runtime-carrier-cas-text-current.md`; no accidental fixture/report was
  added.

## Required current delta

Current `6ab` is `9f` plus only
`tests/test_timeline_clip_replacement.py` (`+215/-41`). Its blob is
`183f14dbe64466c9a8c7aec5b34850da9272f107`, while the completed composition
still has the `9f` blob `66a152346dde1fa0954bb95becb4958fe22370e3`.

Therefore the strengthened current clip tests—disjoint stale rebase, stronger
receipt/event and zero-write assertions, public unsealed refusal coverage, and
the verified generic-image positive—are **REQUIRED current-test carryforward**
when this carrier is applied to `6ab`. Until that exact test delta is carried and
requalified, this review makes no native adoption-ready claim.

## Evidence

Completed composition evidence, inherited from the source worker:

- normal private generation, `generate.py --check`, artifact-manifest check,
  and `git diff --check`: PASS;
- direct carrier slot lane: `10 passed, 45 deselected`;
- central targeted carrier/neighbor lane: `164 passed, 18 deselected, 10
  existing xfailed`;
- the exact new catalog-head fence test: `1 passed`;
- no full suite and no duplicate coordinated `3730` native pair.

Independent final-review checks:

```text
compose diff vs 9f is exactly the 17-path allowlist: PASS
no added skip/xfail markers or removed assertion lines: PASS
no fixture/report paths beyond the intentional design handoff: PASS
git diff --check 9f..919 and 9f..6ab: PASS
compile current tests/test_timeline_clip_replacement.py: PASS
pytest -q -p no:cacheprovider --collect-only tests/test_timeline_clip_replacement.py:
  10/24 tests collected, 14 deselected
```

No product files were changed in this review worktree. Manager next steps are
Agent peer review of `919`/`e9ec260`, carryforward and requalification of the
`6ab` clip-test blob, then exactly one coordinated `3730` pair.
