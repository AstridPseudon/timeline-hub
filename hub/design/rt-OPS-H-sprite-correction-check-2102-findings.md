# OPS H independent findings

## Verdict

**PASS** for the correction packet's authenticity, coordinates, and bounded
scope. **L15 product acceptance remains FAIL.** This check adds no behavior
credit and does not revisit the original review judgment.

## Custody

The correction JSON points to the authentic reviewer JSON at the actual author
root. Its SHA-256 is
`bbb6c75a9a1a338ab68b27c9ebc9d026afb53146b0d9aa8690a6535d972c741b`, matching
the packet. The author report, findings, source map, validation, and handoff
are current post-review overwritten custody files, not recovered author
preimages. Their recorded current hashes match. Both the author and reviewer
raw `log.txt` files also match their recorded hashes and remain retained.

No input root was written during this check. Historical files were not
restored, reconstructed, or treated as available.

## Coordinates and L15 identity

The exact L15 commit is `1c3a2ce725c1afbaafa01e91fd2f8c5479a61ac4`, with parent
`a92c91fa8e7338098cc2f75d1adedcacc8d34447`. The cited Git blobs and the
0.0.13 package bytes hash exactly as listed in `evidence/review.json`.
Python source parsing succeeds for each cited Python blob.

The broad cross-seam test at lines 147–195 uses the sprite projection helper
and has no `host_project` 0.0.13 marker. The marker at lines 198–227 belongs to
the separate half-frame fallback test. Therefore the retained 87-pass run
does not establish the original broad 0.0.13 matrix.

The managed production path calls `project_runtime_parent_composition`, while
the modified sprite SSR helper calls `project_shot_composition`. A passing
sibling using the managed projection cannot be transferred to the modified
helper.

## Causal and L16 boundaries

The source contains the authorized intact `<row>-over` fallback, but retained
logs show only empty `intervals[0]` failures and omit the case tuple, planning
reason, fallback identity/track, and rendered comparison. The exact causal
case is therefore **UNKNOWN**.

The current L16 worktree is separate dirty WIP at the same committed head and
receives no L15 credit. The L15 package-marker/caller gap remains separate from
any L16 repair. Test-service files remain operational envelopes, not complete
v2 commit request/reply bodies.
