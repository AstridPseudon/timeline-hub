---
name: timeline-shots
description: Turn timeline sections into shots, reuse shot content, and inspect every occurrence.
---
# Timeline shots

Load this skill when a section should become a stored shot or shot content
needs another occurrence. Start with the timeline skill for project selection
and the Runtime-backed edit path.

Inside a `tl.commit` edit, call `timeline_structure.label_chapters(t, labels)`
with one `{name, at}` row per section, then run
`python3 -m astrid timelines restructure <timeline> --project <project> --dry-run`.
Review the proposed walls and renderer-equivalence check. If they pass, run the
same command without `--dry-run`; each labeled section becomes a stored shot.
The command refuses a restructure that would change rendered frames or audio.

To use a section again, duplicate one of its placed occurrences. Each duplicate
gets its own shot and occurrence identities, so repeat the operation for each
additional use. Set `source_occurrence_id` to the occurrence for that section,
then read back every placement:

```python
from astrid.sdk.timeline.api import Timeline
from astrid.sdk.timeline.store import fetch_bundle
from astrid.sdk.timeline_editing import duplicate_authoring_shot
from astrid.core.timeline.authoring_bundle import publish_authoring_candidate

tl = Timeline.open(project, timeline)
writer = tl.session.client._remote._transport
for number in (1, 2):
    candidate = fetch_bundle(project, timeline, client=tl.session.client)
    source = next(row for row in candidate["placements"]
                  if row["occurrence_id"] == source_occurrence_id)
    duplicate_authoring_shot(candidate, source["shot_id"],
                             new_shot_id=f"shot-reprise-{number}",
                             occurrence_id=f"occ-reprise-{number}")
    publish_authoring_candidate(candidate, writer,
                                idempotency_key=f"reuse-opening-{number}")
tl = Timeline.open(project, timeline)

tl.commit(lambda t: t.arrange(["occ-reprise-1", "occ-reprise-2"], at=12, gap=1),
          label="Place opening reprises", idempotency_key="place-opening-reprises")

for row in sorted(tl.bundle["placements"], key=lambda item: item.get("at_ms") or 0):
    print(row["occurrence_id"], row["shot_id"], row.get("at_ms"))
```

Each duplicate starts at the source occurrence's position. Arrange the copies
at their intended time, then list all placements; confirm each occurrence ID,
shot ID, and start before reporting the result.
For spoken shots, check word anchors remain unambiguous; Runtime rejects
duplicates whose anchors resolve to the same spoken word.
