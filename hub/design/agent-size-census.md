# Agent Timeline core size census

Read-only census captured at `2026-10-20T23:37:50Z` (UTC). The comparison
baseline is `origin/main` / `497714c73531f164082555ec81b61ca5bc8b6554`.
The current integration snapshot is `tl/integration` /
`19c3cfc1c6283659c6fc864581d56c3a99e41873`. The optional staged Main
candidate is `11511a9a90c1bd38edd2638b5cecd74f159a6179`.

This applies the 08:00 boundary: authored product code that implements
Timeline Read/See/Edit, including SDK timeline/edit/commit/compiler/primitives
and text adapters. The 10:34 owner ruling is also applied: the 20–26k figure
is a rough guide, not a limit or gate. This report does not recommend deleting
working features or changing behavior to reach a number.

## Count

Counts are committed UTF-8 Python blobs. `physical` is `splitlines()`;
`nonblank` counts selected lines whose `strip()` is nonempty. Whole-file rows
use every line in the blob. Mixed files use only the inclusive AST
`lineno..end_lineno` ranges named below. The CSV is the compact path/count
manifest; the path rules are disjoint.

| disjoint bucket | baseline physical / nonblank | current physical / nonblank | delta physical / nonblank | staged candidate physical / nonblank |
|---|---:|---:|---:|---:|
| Agent Read/Edit core | 34,284 / 30,050 | 40,828 / 35,954 | +6,544 / +5,904 | 40,828 / 35,953 |
| Agent See adapters (separate from Viewing render implementation) | 3,362 / 3,079 | 3,563 / 3,252 | +201 / +173 | 3,563 / 3,252 |
| Mixed SDK transport slices | 1,463 / 1,412 | 1,431 / 1,382 | −32 / −30 | 1,431 / 1,382 |
| **Scoped Agent total** | **39,109 / 34,541** | **45,822 / 40,588** | **+6,713 / +6,047** | **45,822 / 40,587** |

The staged candidate is a comparison snapshot, not a second current total. It
is not an ancestor of current: its parent is
`89cb041e4b27c1506338b0b58f2747b7c3ec682c`, and its merge-base with current
is `0542b429175d2ee773e7f90726b5a2de7c967217`. Its non-Timeline upstream
main/infrastructure, test, and generated-client differences are not charged
to these Timeline rows.

## Included path list

The Read/Edit core consists of all Python files under
`astrid/sdk/timeline/`, all top-level `astrid/sdk/timeline_*.py` except
`timeline_filmstrip.py`, all Python files under `astrid/packs/timeline/` except
`cli_visualize.py`, all Python files under `astrid/core/timeline/` except the
three See rows below, plus these SDK adapters:

- `astrid/sdk/_remote_timeline.py`
- `astrid/sdk/authoring_bundle.py`
- `astrid/sdk/authoring_remote.py`
- `astrid/sdk/authoring_revision_diff.py`

The separate Agent See adapter bucket is:

- `astrid/sdk/timeline_filmstrip.py`
- `astrid/packs/timeline/cli_visualize.py`
- `astrid/core/timeline/scene_answers.py`
- `astrid/core/timeline/onscreen.py`
- `astrid/core/timeline/shot_composition_projection.py`

These are Agent-side timeline projections or visual-review adapters. They are
not the Viewing-owned renderer implementation.

Mixed SDK transport is counted only at these boundaries:

- `astrid/sdk/remote.py`: the `RemoteTimelines` and `RemoteShots` classes.
- `astrid/sdk/workspace_client.py`: the hand-authored methods for timeline
  revisions, timeline CRUD/history/commit/inspection/diff, parent composition
  media, project shots, shot items, and shot text bindings. The generated
  operation map and generic client plumbing are not counted.

## Exclusions and ownership boundary

- `tests/`, `tests/editing_conformance/`, fixtures, docs, schemas, lockfiles,
  generated contract/client copies, generated registries, `dist/`, and binary
  package contents are excluded.
- `astrid/packs/rendering/**` and `remotion/**` are Viewing-owned rendering
  paths. They are not silently folded into Agent's total; the Agent-side See
  adapters above are the only See rows here.
- Agent render/presentation neighbors such as `astrid/sdk/project_render.py`,
  `authoring_render_preview.py`, and `render_shot_snapshot.py`, plus media
  producer/support files, remain outside this Timeline core census.
- Untouched generic Agent infrastructure is excluded. When a mixed file has a
  Timeline and non-Timeline responsibility, only the named Timeline class or
  method ranges are counted.

The counts are therefore a scoped authored-source footprint, not a claim that
every counted line is canonical command meaning or that every adjacent helper
is removable. They are also not a cross-repository compliance result: the
PLAN's rough guide is evaluated honestly across the four areas at the hard
stop, with planned duplicate/legacy deletions and behavior preservation still
governing the work.

## Method and verification

For each exact SHA, the census enumerated committed paths with
`git ls-tree -r --name-only`, read each selected blob with `git show SHA:path`,
and counted the selected line sets. Mixed selections were parsed with Python's
`ast` module and unioned by source line, so overlapping declarations cannot be
double-counted. Missing baseline paths contribute zero. The arithmetic is in
[`agent-size-census.csv`](agent-size-census.csv).

No product code, tests, branches, refs, dependencies, or shared paths were
modified. No test suite was requested or run because this task is read-only
source arithmetic.
