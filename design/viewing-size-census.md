# Viewing-owned TIMELINE CORE size census

Measured 2026-10-20 from committed Git blobs. This is the authoritative
Viewing slice of the PLAN §3 TIMELINE CORE boundary, not a whole-repository
count and not a claim that the 20–26k-line target has been met.

## Revisions

| repository | `origin/main` baseline | `tl/integration` current |
| --- | --- | --- |
| Agent (`/home/user/work/agent`) | `a411628f8fd6129f9c58c332019b56769d997384` | `f7584fad7c7cbd548cf340bb501d09d3520ea9e3` |
| App (`/home/user/work/app`) | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` |
| Composition (`/home/user/work/composition`) | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `5e06f40146573a529896cc812229eb890c53c81a` |

The Runtime is not repeated here: its timeline commit/inspection and visual
seam code belong to the Runtime-owned census. Untouched worker/execution
infrastructure, generic `astrid_runtime`, generated contracts/clients, and
unrelated packs are outside this Viewing report.

## Canonical authored source

Bytes are exact blob bytes, including comments and JSON/YAML metadata. Lines
are nonblank physical UTF-8 lines and are a secondary readability metric. The
delta is current minus baseline.

| owned slice | files main → current (Δ) | bytes main → current (Δ) | nonblank lines main → current (Δ) |
| --- | ---: | ---: | ---: |
| Composition evaluator/default source | 16 → 79 (+63) | 45,621 → 190,523 (+144,902) | 1,398 → 4,097 (+2,699) |
| Agent `timeline_visualize` adapters | 54 → 55 (+1) | 1,253,951 → 1,270,190 (+16,239) | 24,911 → 25,256 (+345) |
| Agent scene/render adapters | 29 → 29 (0) | 375,489 → 366,756 (−8,733) | 10,993 → 10,744 (−249) |
| Agent public/private scene adapters | 1 → 2 (+1) | 18,156 → 24,116 (+5,960) | 375 → 469 (+94) |
| Agent Remotion scene host | 14 → 13 (−1) | 60,784 → 63,578 (+2,794) | 1,391 → 1,431 (+40) |
| App preview/player/render adapters | 29 → 30 (+1) | 282,934 → 293,804 (+10,870) | 6,932 → 7,164 (+232) |
| **Viewing-owned canonical total** | **143 → 208 (+65)** | **2,036,935 → 2,208,967 (+172,032)** | **46,000 → 49,161 (+3,161)** |

The current 49,161 authored lines are above the PLAN target. Excluding code
that is genuinely outside this boundary is measurement hygiene; it is not
deletion progress and does not establish target achievement.

## Boundary and manifest

The reproducible manifest is the committed script
[`scripts/viewing-size-census.mjs`](../scripts/viewing-size-census.mjs). Run:

```sh
node scripts/viewing-size-census.mjs --json
```

It uses only `git ls-tree` and `git show` against the three absolute source
worktrees above. It does not checkout, build, install, follow the worktrees'
working files, or mutate `.git`.

The selected boundary is:

- Composition: all `typescript/src/**`, except generated registries/curves and
  `remotion-timer-compat.d.ts`. This captures the evaluator, scene API, clip
  look/timing/audio seams, and built-in element/default metadata.
- Agent: authored files under
  `astrid/packs/rendering/actions/timeline_visualize/**` except stage/docs,
  fonts, inspector assets, and schemas; the explicit scene/render adapter
  files and element seam under `astrid/packs/rendering`; `astrid/core/timeline/onscreen.py`
  and `scene_answers.py`; and authored `remotion/src/**` excluding generated,
  declaration, and test files. The explicit adapter list is in the script.
  Other Agent timeline model/compiler/edit-command/read code is Agent-owned,
  not silently included here.
- App: non-test source in exactly
  `src/tools/video-editor/components/PreviewPanel/**`,
  `src/tools/video-editor/compositions/**`, and
  `src/tools/video-editor/render/**`, excluding the fallback directory. There
  is no separate `player` directory in this revision; the player surface is
  represented by the preview/composition roots.

This deliberately excludes untouched generic main infrastructure, unrelated
rendering packs (`assemble_timeline`, `html_canvas_effect`, `sprite_sheet`,
`timeline_storyboard`, and live-scene/transcript-only roots), generated
contracts/clients, tests/fixtures, documentation, build output, and archives.

## Generated, duplicate, and archive accounting

These bytes are not added to the canonical total.

| category | files main → current (Δ) | bytes main → current (Δ) | nonblank lines main → current (Δ) |
| --- | ---: | ---: | ---: |
| Composition generated registries/curves/timer declaration | 4 → 7 (+3) | 5,228 → 12,628 (+7,400) | 88 → 405 (+317) |
| Agent visualize schemas | 10 → 10 (0) | 70,613 → 70,613 (0) | 1,925 → 1,925 (0) |
| Agent Remotion generated/declaration source | 5 → 4 (−1) | 14,636 → 14,228 (−408) | 419 → 408 (−11) |
| App fallback registries/theme shims | 4 → 0 (−4) | 4,785 → 0 (−4,785) | 229 → 0 (−229) |
| **Generated/declaration total** | **23 → 21 (−2)** | **95,262 → 97,469 (+2,207)** | **2,661 → 2,738 (+77)** |

The App’s vendored Composition source is counted transparently but not added
to canonical Composition:

| duplicate | files | bytes | nonblank lines | status |
| --- | ---: | ---: | ---: | --- |
| `vendor/timeline-composition/typescript/src/**` total | 21 → 21 | 51,742 → 51,742 | 1,504 → 1,504 | duplicate present at both revisions |
| of which generated/declaration (`*.generated.*`, `*.d.ts`) | 5 → 5 | 6,193 → 6,193 | 113 → 113 | already included only in the duplicate row |

The current Agent package archive is
`remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz` (58,008 bytes)
and the current App package archive is
`vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz` (50,664 bytes).
Neither archive is counted as newly authored source. Neither exists at the
corresponding `origin/main` ref in this census.

## Remaining cuts and interpretation

The census does not close any deletion ledger row:

- **D08** (App duplicate what-is-on-screen math) remains in progress; actual
  frame/audio parity is still open. The App adapter count therefore remains
  current authored code, not an assumed future deletion.
- **D09** (Agent private visibility/evaluator math and `onscreen.py`) remains
  held/in progress. Public scene transport does not prove source/asset/theme/
  occurrence joins, caller migration, or the required positive/pixel coverage.
  The private 375-line baseline/current evaluator is intentionally visible in
  the table.
- **VW-AUDIO-STEP / App D08b** remains open: the continuous audio policy still
  needs both-consumer and physical parity proof. No audio path was discounted
  from the current count.
- **D10** (vendored Composition copies) remains held pending coordinated App/
  Agent package adoption. The duplicate is shown above rather than silently
  treated as canonical or as a new archive-authored source.

No browser, socket, renderer, install, network, or full-suite run was needed
for this read-only census. The shared dependency graph was not touched; no
before/after link-manifest mutation occurred. A central integration check must
compare its before/after shared-graph manifest and block on topology drift
rather than silently establish a new baseline.
