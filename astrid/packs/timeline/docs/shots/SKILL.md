---
name: timeline-shots
description: Label sections, reuse a published shot, arrange occurrences, and inspect the result.
---
# Reuse and arrange shots

Open the timeline, label its sections, place a published shot again, arrange
the occurrences, then inspect every placement. The timeline already has
picture cuts at the section starts.

```python
from astrid.sdk.timeline.api import Timeline
from astrid.sdk.timeline.native_occurrence_shared import capture_occurrence_place_shared
from astrid.sdk.timeline_structure import label_chapters

tl = Timeline.open(project, timeline)
label_rows = [
    {"name": "Opening", "at": 0},
    {"name": "Next section", "at": 4},
]
tl.commit(lambda t: label_chapters(t, label_rows), label="Label sections")

# Reuse a published occurrence. The new placement keeps its shot identity.
source = "occ-earlier"
source_shot = next(row["shot_id"] for row in tl.bundle["placements"]
                   if row["occurrence_id"] == source)
shared = capture_occurrence_place_shared(
    tl.bundle, f"occurrence:{source}", "occ-reuse", on=8,
)
tl.commit([shared], label="Reuse Earlier shot", key="reuse-earlier-shot")

tl.commit(lambda t: t.arrange(
    [source, "occ-later", "occ-reuse"], at=0, gap=0,
), label="Arrange shots")

landed = Timeline.open(project, timeline)
placements = sorted(landed.bundle["placements"],
                    key=lambda row: row["placement"]["start_ms"])
for row in placements:
    print(row["occurrence_id"], row["shot_id"], row["placement"]["start_ms"] / 1000)
reuse = next(row for row in placements if row["occurrence_id"] == "occ-reuse")
assert reuse["shot_id"] == source_shot
```

Chapter labels point to authored cuts. Shared placements keep the same shot;
each occurrence has its own start time.
