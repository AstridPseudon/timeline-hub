# VW-D09 same-film public source repair

## Result

The original private assertion remains byte-for-byte unchanged.  No Agent
product, public DTO, authority/projector, package pin, archive, or active caller
was changed.

This repairs the exact gap named by reviewer0218 REQUEST CHANGES: the current
tree had no same-film public replacement, while Main6 proof8195 approves the
independent-fade DIP interval and requires the incoming-COVERED control to be
retained.

The exact old film was evaluated through Composition14's public `evaluation`
entry (`prepareScene` / `querySceneFrame`) in a disposable source overlay:

* `out`: `am-snap-plate`, track `plate`, at `0`, hold `1`, `src` `/plate.png`,
  `fade_out: 0.5`;
* `in`: `am-footage`, track `fx`, at `0.5`, hold `1`, `src` `/footage.png`,
  `fade_in: 0.5`;
* 1920x1080 at 30 fps, the same `c01/l` app metadata and four visual tracks as
  the Main6 proof.

The canonical rows were exactly:

```text
(0,16)  COVERED / CONTENT
(16,30) DIP     / None
(30,45) COVERED / CONTENT
45      GAP     / None, no layers
```

Frame 15 retained `out=1` and `in=0`; frames 16..29 contained both real clip
IDs with both opacities strictly between zero and one; frame 30 contained only
`in` at opacity 1.  The preserved incoming-transition form of the same AM
clips was also queried canonically: all frames 0..59 were `COVERED / CONTENT`,
frame 22 contained `out` at 1 and `in` at 0.4666666666666667, and frame 60 was
`GAP` with no layers.

The source overlay used the reviewed AM-footage capability source at commit
`2e9fb6e260778e0ae6dc4a39a498d0f36a837ef6` and the current AM snap-plate
capability source.  Those are component-owned capability functions; no rows or
coverage formula were mocked.  Composition source was the existing built
`7bb54bbd64107e5090643ecca1e4d33164173e85` tree.  The Composition14 source
was needed only as the private evaluator build; it was not archived or pinned.

## Current pin and guards

The accepted public13 artifact was only read: SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, version
`0.0.13`, 77 tar members.  The private original-test SHA-256 before and after
was `80c31db3d2c74fecb5453abcf01f53ce3e4ee43c0d4b8b8f0a3634fa7ab0fa05`.
The worktree is clean and `git diff --check` passes.

## Exact mapping and adoption dependency

The old test is
`tests/core/timeline/test_onscreen_more.py::test_a_cross_fade_of_two_full_plates_is_covered_not_dip`.
Its exact fixture is the two clips above and its old expectation is one
`COVERED/CONTENT` span `(0,45)`.  The dormant replacement is the same fixture
queried per-frame through the canonical public evaluator, with explicit
`DIP/None` `(16,30)` plus the retained incoming-transition positive.  The old
test remains live; no retirement is proposed in this handoff.

The live dependency is paired adoption of the reviewed AM-footage capability
source and Composition14's source-built evaluator/registry path.  Until that
pair is qualified on the active pin tuple, current public13 returns `UNKNOWN`
for this film because `am-footage` has no admitted capability in the accepted
registry.  That is an honest current limitation, not a reason to weaken the
assertion or substitute a different film.  The active SDK callers still
include Scene answer preparation plus the legacy onscreen coverage consumers;
their one-to-one retirement remains blocked on reviewer approval and paired
adoption.

