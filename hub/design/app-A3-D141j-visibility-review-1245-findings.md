# A3/P2 D141j independent source visibility review

## PASS_SOURCE_VISIBILITY — no new findings

Prior `D141J-VIS-001` is resolved in the authenticated terminal candidate.
The source no longer derives the active association from the collector's first
or last accepted head. Each accepted canonical read gets a distinct identity,
and the exact accepted-read occurrences array is retained in a `WeakMap` and
used at the active-occurrences, useShotGroups input/result, and pre-overlay
seams.

The independently regenerated synthetic artifact contains two complete ordered
chains: `timeline-rev-2`/`accepted-read-1`, then
`timeline-rev-3`/`accepted-read-2`. The same checker passes the artifact. A
stale second active association is rejected with exit 1, proving that unrelated
event order or a cached first head cannot qualify the second render.

All original twelve predicates remain present; the repeat-read case is
additive. Cause remains `UNKNOWN`; the diagnostic body and historical 27026
observation were not run.
