# Preliminary Agent Timeline-core size census

Captured `2026-10-21T01:59:11Z` (UTC). This is a read-only census at the
exact current commit `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`, compared
with the same path rules at `origin/main`
(`497714c73531f164082555ec81b61ca5bc8b6554`). It follows PLAN section 3:
the 20–26k figure is a rough guide, not a hard cap or gate.

## Scoped result

`physical` counts UTF-8 blob lines using `splitlines()`; `nonblank` counts
those lines after `strip()`. The selected paths are disjoint.

| bucket | origin/main physical / nonblank | current physical / nonblank | delta physical / nonblank |
|---|---:|---:|---:|
| Agent Read/Edit core | 34,284 / 30,050 | 41,156 / 36,253 | +6,872 / +6,203 |
| Agent See adapters | 3,362 / 3,079 | 3,986 / 3,647 | +624 / +568 |
| Mixed SDK transport slices | 1,463 / 1,412 | 1,431 / 1,382 | −32 / −30 |
| **Scoped Agent total** | **39,109 / 34,541** | **46,573 / 41,282** | **+7,464 / +6,741** |

These are authored-source footprint numbers, not a claim that every line is
new Timeline meaning or removable. No source deletion is proposed to reach a
number.

## Exact path boundary

Read/Edit core is exactly:

- all committed Python under `astrid/sdk/timeline/`;
- top-level `astrid/sdk/timeline_*.py`, except `timeline_filmstrip.py`;
- all committed Python under `astrid/packs/timeline/`, except
  `cli_visualize.py`;
- all committed Python under `astrid/core/timeline/`, except
  `scene_answers.py`, `onscreen.py`, and
  `shot_composition_projection.py`;
- the adapter files `astrid/sdk/_remote_timeline.py`,
  `astrid/sdk/authoring_bundle.py`, `astrid/sdk/authoring_remote.py`, and
  `astrid/sdk/authoring_revision_diff.py`.

The current/baseline Read/Edit subcounts are:

| exact path group | origin/main | current | delta |
|---|---:|---:|---:|
| `astrid/sdk/timeline/**/*.py` | 7,415 / 6,484 | 14,090 / 12,455 | +6,675 / +5,971 |
| `astrid/sdk/timeline_*.py` minus filmstrip | 6,304 / 5,583 | 6,587 / 5,856 | +283 / +273 |
| `astrid/packs/timeline/**/*.py` minus visualize CLI | 5,775 / 5,127 | 6,201 / 5,507 | +426 / +380 |
| `astrid/core/timeline/**/*.py` minus the three See files | 14,342 / 12,453 | 13,643 / 11,856 | −699 / −597 |
| four SDK adapter files above | 448 / 403 | 635 / 579 | +187 / +176 |

Agent See adapters are exactly:

- `astrid/sdk/timeline_filmstrip.py`;
- `astrid/packs/timeline/cli_visualize.py`;
- `astrid/core/timeline/scene_answers.py`;
- `astrid/core/timeline/onscreen.py`;
- `astrid/core/timeline/shot_composition_projection.py`.

The mixed SDK transport bucket does not count whole files. It counts the
`RemoteTimelines` and `RemoteShots` classes in `astrid/sdk/remote.py`, plus
the hand-authored timeline/revision/shot/text-binding methods in
`astrid/sdk/workspace_client.py`. Generic client plumbing and generated
operation maps are excluded. The selected method names are the timeline CRUD,
history, commit, inspection, diff, revision, parent-composition media,
project-shot, shot-item, and shot-text-binding methods; the reproducible AST
selection is the method-name set in the selector below.

The exact mixed-file selector is:

```text
remote.py classes: RemoteTimelines, RemoteShots
workspace_client.py methods:
get_project_shot_revision, get_project_timeline_revision,
get_project_parent_composition_revision, publish_parent_composition,
replace_parent_composition_media, create_timeline, rename_timeline,
create_timeline_document, update_timeline_document, list_timelines,
commit_timeline, list_timeline_commits, get_project_verified_document,
get_project_verified_document_object, get_timeline, inspect_timeline,
create_timeline_view, list_timeline_history, replace_timeline_clip,
diff_timeline, archive_timeline, recover_timeline, list_project_shots,
create_project_shot, get_project_shot, update_project_shot,
archive_project_shot, recover_project_shot, add_shot_item,
promote_project_shot_candidate, remove_shot_item, reorder_shot_items,
list_project_shot_text_bindings, set_project_shot_text_binding,
get_project_shot_text_binding, set_project_shot_text_binding_by_id,
rebind_project_shot_text_binding
```

The five See files are Agent-side projections/adapters only. The renderer and
rendering implementation remain Viewing-owned and are not counted here.

## Timeline additions in shared `generic_host.py`

The whole `astrid/core/execution/generic_host.py` is excluded as generic host
infrastructure. Relative to `origin/main`, its Timeline-specific additions
are the `PreparedTimelineInputs.prepare(...)`, `values.prepare_snapshot(...)`,
`values.mint_source(...)`, and `PreparedTimelineInputs.handoff_source(...)`
excerpts. They contain **20 inserted physical / 16 inserted nonblank lines**;
because the old one-line `return values` becomes a four-line mint-source
try/except, the net selected excerpt delta is **+18 physical / +15 nonblank**.
Neither figure is included in the scoped Agent total.

## Authored tests and fixtures (context only)

These are deliberately not core-target lines and no fixture cleanup is being
requested. The context selection is all `tests/editing_conformance/**/*.py`,
all `tests/editing_conformance/fixtures/**`, all `tests/timeline/**/*.py`,
all `tests/packs/timeline/**/*.py`, all `tests/core/timeline/**/*.py`, the
timeline-named `tests/core` files, and the explicitly timeline-focused SDK
tests (`test_timeline*`, `test_timing*`, `test_native_timeline*`, scene,
capture, admission, authority, and timeline workspace-client tests).

| context | origin/main files / lines | current files / lines | delta files / lines |
|---|---:|---:|---:|
| authored tests | 104 / 26,223 physical (21,589 nonblank) | 208 / 56,086 (47,513) | +104 / +29,863 (+25,924) |
| authored JSON fixtures | 0 / 0 | 32 / 33,408 (33,408) | +32 / +33,408 (+33,408) |

The fixture count is context, not product size. It includes current editing
conformance fixtures and does not justify deleting or weakening any positive
behavior expectation.

## Exclusions and ownership

- `tests/`, fixtures, docs, schemas/contracts, lockfiles, manifests,
  generated clients and generated registries are outside the core total.
- `astrid/packs/rendering/**` and `remotion/**` are Viewing-owned rendering
  paths. They are intentionally not folded into Agent's See number, avoiding
  cross-area double counting.
- Whole generic infrastructure, including `generic_host.py`, is excluded;
  only the Timeline excerpt above is disclosed separately.
- Binary artifacts, vendored Composition packages, stale `dist/`, and
  unrelated packs are excluded.

## Remaining deletion/dead-path ledger state

The current Agent deletion ledger still has these rows open, held, or pending;
they are not silently treated as deleted in the census:

| status group | rows / remaining path or responsibility |
|---|---|
| in progress | `D13` generic-host assembled-timeline direct publish; `D01a` popup occurrence add/swap fallback; `D01b` canonical placement loop; `AG01` local journal/history/save consumers; `AG02` legacy SDK/CLI snapshot saves (numeric parent consumer only deleted); `AG03` cut-sheet merge/save (partial); `WC7` whole-document publish path (attached migrated slices only) |
| held | `AG-M2-TB01` direct text-binding writers; `AG-M3-CAP-01..04` candidate/source admission positives; `AG05` duplicated capture projection; `WC1` whole authoring-candidate publisher; `WC3` remote parent-media publisher; `WC5` authoring-remote publisher; `WC6` rendering-doc detached publisher; `WC8` whole-document merge; `WC10` Runtime parent-composition route; `AG-MAT-V01..V03` obsolete private-carrier fixtures; `AG-CATALOG-PROMOTION` Runtime preservation gate |
| rejected/unmerged preservation rows | `AG-CUTOVER-01..05`; these are retained as ledger decisions because positive behavior preservation is incomplete, not counted as product code |

Rows already marked deleted in the ledger include `D05`, `D06`, `D07`, `WC2`,
`WC4`, `WC9`, `AG-RECOVER`, and `AG-M2-DEAD-LEAF-01`. The open rows above
remain the authoritative cleanup list; this report adds no new framework,
threshold, or deletion decision.

## Reproduction

From this worktree, the path families can be printed for either exact SHA with:

```sh
git ls-tree -r --name-only "$SHA" | awk '
  ($0 ~ /^astrid\/sdk\/timeline\/.+\.py$/) ||
  ($0 ~ /^astrid\/sdk\/timeline_[^\/]+\.py$/) ||
  ($0 ~ /^astrid\/packs\/timeline\/.+\.py$/) ||
  ($0 ~ /^astrid\/core\/timeline\/.+\.py$/) ||
  ($0 == "astrid\/sdk\/_remote_timeline.py") ||
  ($0 == "astrid\/sdk\/authoring_bundle.py") ||
  ($0 == "astrid\/sdk\/authoring_remote.py") ||
  ($0 == "astrid\/sdk\/authoring_revision_diff.py") {print}
' | sort
```

Remove the five See paths from that output for Read/Edit, and count them
separately. For every whole-file row, use `git show "$SHA:$path"`; for the
two mixed files, parse the committed blob with Python `ast`, select the named
classes/methods, and union each selected node's inclusive `lineno..end_lineno`
range before counting. Missing baseline paths contribute zero. This is the
same path/range method used for both SHAs, so the delta is comparable.

Verification was arithmetic/source inspection only. No product code was
changed and no test or suite was run, as required for this read-only census.
For transparency, `git diff --check origin/main...HEAD` exits 2 on three
pre-existing unrelated blank-at-EOF warnings in
`astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py`,
`astrid/sdk/timeline/_media_inputs.py`, and
`docs/design/agent-fixture-trim-current.md`; this worker added none of them.
