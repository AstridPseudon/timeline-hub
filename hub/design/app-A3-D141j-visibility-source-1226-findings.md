# A3/P2 D141j source preparation

The private candidate records four read-only seams in the actual App caller
chain:

1. useAstridShotsHost records the accepted prepared head and occurrence IDs.
2. useShotGroups records the canonical input immediately before projection and
   its complete result.
3. TimelineEditorCore records the values it forwards immediately before the
   TimelineCanvas/ShotGroupOverlay path.

The source control mounts the real host hook, real useShotGroups, and real
TimelineEditorCore with a finite synthetic contract. The retained artifact
proves head timeline-rev-2, occurrence occ-5, five active occurrences, five
group results, and exact ordering. These are synthetic control observations;
they are not observations of 27026 or any historical browser run.

Cause remains UNKNOWN. No diagnostic body, service route, browser journey,
native request, product repair, wire change, fixture change, pin, generated
file, or worker merge request was made.
