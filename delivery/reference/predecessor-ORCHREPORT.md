# Owner-film clip-look hard-stop scan

## Result

Owner-film canonical data is **not present on this Viewing machine**. I did not
inspect fixtures, examples, tests, credentials, databases, `.aws`, `.git`, or
`node_modules`, and I do not claim a clean/no-overlap result. The hard-stop
condition is therefore **incomplete / unverified**, not clean.

The machine-readable limited-search result is
`owner-film-cliplook-scan.json`. The reusable read-only scanner is
`owner_film_cliplook_scan.py`; both are ORCH-owned and no product framework was
changed.

## Authoritative references checked

- Settled plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`, especially the 2026-10-20 owner-review decision: element/custom-effect clips honor clip look (`opacity`, crop, fades, `entrance`/`exit`) and overlapping independent fades intentionally dip.
- Current mirrored plan: `/home/user/timeline-hub/hub/kit/PLAN.md`, same decision at lines 248–249. The requested R4 path `/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4` and requested prior-report path `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/luna/reports/` are absent on this machine.
- Viewing design: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing.md` and `viewing-coordination.md` establish the canonical Runtime parent-revision/shot/internal closure and registered-element seam.
- Offline inspection contract: `docs/reference/timeline-offline-inspection.md` requires render-free declared-input inspection and exact pinned closure; `docs/packs/data-storage.md` rules out treating generic/arbitrary records as project data.

## Exact limited search

Command:

```sh
PYTHONPATH=/home/user/work/wt/vw-m3-owner-film-cliplook-scan \
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-cliplook-scan/owner_film_cliplook_scan.py \
  --search --json-out /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-cliplook-scan/owner-film-cliplook-scan.json
```

The scanner walked only these named roots, to depth 5, matching only
`project.json`, `timeline.json`, or `canonical_document.json` and excluding
`.git`, `.aws`, `credentials`, `node_modules`, `tests`, `fixtures`, and
`examples`:

| Root | Exists | Matches |
|---|---:|---:|
| `/home/user/work/wt/vw-m3-owner-film-cliplook-scan/projects` | yes | 0 |
| `/home/user/work/agent/projects` | yes | 0 |
| `/home/user/peteromallet/astrid-agent/projects` | yes | 0 |
| `/home/user/banodoco/banodoco-workspace-runtime/projects` | no | 0 |
| `/home/user/banodoco/reigh-app/projects` | no | 0 |
| `/mnt/user-data` | yes | 0 |

No candidate path was found. No Runtime door, browser, network, media fetch,
render, or database query was run.

## Scanner contract

When the owner orchestrator supplies one read-only duplicate of the exact
Runtime `canonical_document` closure, run:

```sh
PYTHONPATH=/home/user/work/wt/vw-m3-owner-film-cliplook-scan \
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-cliplook-scan/owner_film_cliplook_scan.py \
  --input /OWNER-PROVIDED/canonical_document.json \
  --json-out /tmp/owner-film-cliplook-scan.json
```

The required duplicate shape is the canonical document with
`parent_revision.payload`, pinned `shot_revisions`, pinned
`internal_timeline_revisions`, and `dependency_manifest`. It must be a
read-only copy, not credentials or a raw DB/table dump. If the closure is
missing or projection fails, the result is `status: incomplete` and
`clean_claim: false`; no no-overlap statement is emitted.

The scanner uses only existing Agent helpers:

- `project_runtime_parent_composition` for the canonical parent/occurrence
  projection and authored pins;
- `load_default_registry` for exact registered effect resolution, including
  `elementRef.packId` when present;
- `clip_fields.describe` and `clip_fields.yaml` for declared look property
  names; no suffix or shape inference;
- `resolve_render_profile` / existing `capture.rate` for the authored rational
  FPS pin; and
- `clip_start_frame` / `clip_end_frame` for half-open frame intervals.

Unknown/unregistered non-built-in element references are reported as explicit
`unknown_candidate` rows, never guessed from a clip-name suffix. The report
includes project/timeline/revision, occurrence/shot/internal revision pins,
authored and projected clip IDs, same-track overlap frame intervals, look
property names/source paths, source kind, registered source path, and compile
availability. It does not dump captions, scripts, or raw payloads.

## Direct checks

- `python3 -B` in-memory scanner smoke with a synthetic non-owner canonical
  closure: **PASS**; preserved `[30000, 1001]` FPS, found 2 registered element
  candidates, and reported one `[30, 60)` overlap with look fields.
- Incomplete-closure smoke: **PASS**; returned `status: incomplete`.
- Python syntax compilation with `compile(...)`: **PASS**.
- `git diff --check`: **PASS** (worktree has no product changes).
- Full/browser/network/install/live-socket tests: **not run** and not needed for
  this read-only preparation.

## Required next step / blocker

Owner orchestrator must provide the exact read-only duplicate path to the
canonical owner-film closure (project ID, timeline ID, selected revision and
all pinned occurrence/shot/internal payloads). After that path is supplied, run
the scanner once and report its JSON. Until then, this task cannot produce the
requested owner-film clip risk list and cannot certify condition 3.
