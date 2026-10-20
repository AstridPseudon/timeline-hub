# App timeline-core size census

Read-only census of App `tl/integration` at current `75df44e99bed22db39430e420d82764126c9a316`. The comparison baseline is `origin/main` at `580508eed1bf6ed95caaf476c9d69a4672472a2f`. The complete file manifest, per-file counts, symbol slices, and excluded/debt paths is [app-size-census.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-size-census.json).

## Count

Counts are committed-blob physical lines (`splitlines`, blanks included) and nonblank lines (`strip()` nonempty). The core count includes authored timeline Read/See/Edit commands, commit/outbox/history, projections, timing/data adapters, timeline UI writers, text/transcript views, popup graph producers, shared placement producers, and the App Runtime timeline slices. It excludes tests/helpers, fixtures, generated contract data and clients, untouched generic infrastructure, build/dist output, vendor trees, package archives, binaries, and retained generic Supabase completion code. The generic `src/integrations/runtime/client.ts` and `dataProvider.ts` are counted only by the declared timeline/commit/media symbols in the manifest; neither whole file is treated as timeline code.

| exact tree | files | physical | nonblank | delta |
|---|---:|---:|---:|---:|
| `origin/main` `580508e` | 194 | 63,715 | 59,067 | — |
| current integration `75df44e` | 204 | 65,764 | 61,017 | — |
| current − main | +10 | +2,049 | +1,950 | measured |

The current count is a scoped inventory, not a compliance result. It does not establish the PLAN’s 20–26k target, which requires cross-repository cuts and proof of the final boundary.

Viewing-owned live UI is reported separately to avoid double counting and does not change ownership: main 32 files / 10,088 physical / 9,264 nonblank; current 33 / 10,330 / 9,497; delta +1 / +242 / +233. This is PreviewPanel, compositions, render roots, and the three render-state/store hooks; it is not in the core totals.

## Separate debt and cuts

These buckets are not added to the core total. They are reported so duplicated or retired source is not mistaken for integrated core or silently lost.

| bucket | main | current | treatment |
|---|---:|---:|---|
| Vendored authored Composition source, 17 files | 1,573 / 1,416 nonblank | 1,573 / 1,416 | deletion debt while the single package adoption gate is pending |
| Vendored generated Composition registries, 4 files | 95 / 88 | 95 / 88 | generated, separately counted |
| App fallback/generated registries, 4 files | 246 / 229 | 0 / 0 | already deleted on current; not re-counted as an integrated core reduction |
| Vendored authored defaults, 13 JSON files | 24 / 24 | 24 / 24 | deletion debt; includes vendored animation/transition/theme defaults |
| Supabase canonical-writer cuts, 29 production files | 7,914 / 7,095 | 0 / 0 | D03 cut is deleted on current; retained completion/billing/relational effects are excluded |
| `vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz` | absent | 50,664 bytes | binary artifact; not line-counted |

## Staged, not integrated

These are expected additional changes and are deliberately not relabeled as current integration:

- Public12 source stage `tl/app-m3-public12-isolated-source-stage`: six paths (package/lock, immutable `0.0.12` artifact, Vite package test, renderer sequence test, installed-theme test). Its text-source numstat is +94/−135 against its own `090e1162` base; current tuple adoption remains pending.
- Render safety stage `tl/app-m3-render-current-safety-refresh-r1`: seven product paths, with five source files at +124/−20 against its own `b8064ecf1` base; test-only observer files are excluded. It is not in current `75df44e`.
- Continuation storage composition `tl/app-m2-continuation-storage-compose`: five product paths, 831 → 1,616 authored product lines, +785; it is a source composition, not integrated here.

## Top remaining writer/deletion targets

Status is linked to the [current App deletion ledger](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.app.md) and the listed regression tests. “Open/in-progress” means the old writer remains; no row is closed by this census.

| ledger row | current target | replacement boundary | regression evidence to retain |
|---|---|---|---|
| `D01-app-whole-parent` | `dataProvider.ts` `saveTimelineAtHead/saveTimelineInOrder`; `useTimelinePersistence.ts` | one command-session commit | `dataProvider.test.ts`, `useTimelinePersistence.test.tsx` |
| `D01-app-shot-graph` | popup `shotCompositionAdapter.publish`; `ShotEditorView.tsx` direct publishes | native shot/config commands | `ShotEditorView.test.tsx`, `shotCompositionEditor.test.ts` |
| `D01-app-popup-add` | `shotTimelineDataProvider.ts` add path | `occurrence.add-media` | popup/ShotEditor journey tests |
| `D01-app-popup-swap` | `shotTimelineDataProvider.ts` swap path | `occurrence.swap-media` | popup/ShotEditor journey tests |
| `D01-app-bootstrap` | `createDefaultTimeline.ts` | constrained Runtime creation plus guarded initialization commands | `createDefaultTimeline.test.ts` |
| `D01-app-split` | `useClipSplitting.ts`, `useTimelineCommandsService.ts` | captured native split batch | `three-products.spec.ts`, clip editing tests |
| `D01-app-duplicate` | `AstridTimelineEditor.tsx`, shot-group pack helpers | native occurrence duplicate with reserved identities | `AstridTimelineEditor.test.tsx`, shot-group tests |
| `D01-app-placement` | `placementService.ts` and its three callers | owner-addressed placement through outbox | `placementService.test.ts`, placement ingress tests |
| `D01-app-ordinary-batch` | `useTimelineOps.ts` patch/project-data path | one atomic supported native batch | `useTimelineOps` tests, command-session tests |
| `D01-app-element-routes` | `runtime/element-adapter.ts`, `ElementsLibraryPanel.tsx` | exact element command identity/revision path | `element-adapter.test.ts`, element route tests |

The render producer continuation remains an additional open ledger row (`D01-app-render-producer-continuation`) and is not counted as a canonical writer merely because `useRenderState.ts` admits/polls work.

## Limits and method

The file list is generated from `git ls-tree` at the two exact SHAs. Missing paths count zero for that tree. Runtime slices use method boundaries, with symbol names and line ranges recorded in the manifest. The census did not inspect or count generated contract clients, test data, fixtures, old generic shared timeline hooks, package lock contents, vendor package internals, or binary contents as authored lines. No 20k compliance claim is made.

No product code, tests, dependencies, shared folders, branches, or Git refs were modified. No test suite was run; this was a read-only inventory. Checks performed:

```text
git rev-parse origin/main HEAD                                      PASS
python -m json.tool <absolute manifest>                             PASS
git status --short --branch                                         PASS (clean worker tree)
```
