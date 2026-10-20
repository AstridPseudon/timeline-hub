# Viewing Timeline Core — current M4 census

Refreshed 2026-10-20 from the three integrated heads after the latest M3/M4
cuts. This is a size census, not a target-achievement claim. Counts are
committed Git blob bytes, physical UTF-8 lines (`splitlines()`), and nonblank
physical lines (`strip()` nonempty). The same owned Read/See manifest is used
for main and current; it excludes generated clients/registries, tests,
fixtures, archives, vendor copies, and untouched infrastructure.

## Pinned inputs

| repo | baseline (`origin/main`) | current (`tl/integration`) |
|---|---|---|
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` |
| Agent | `a411628f8fd6129f9c58c332019b56769d997384` | `d0a5072bbe7b7ce9489f43aa0a81027ec400343b` |
| App | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `20ea14c26526fe4924354f10a177aebbaf6002bc` |

Runtime is intentionally absent: its commit/inspection and visual-seam paths
belong to the Runtime-owned census. No branch name or unstable `HEAD` default
is used by the reproducer.

## Confirmed canonical scope

The exact flat manifest and source methodology remain:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs
```

It reads only committed blobs from the three absolute repository paths. The
prior frozen JSON remains preserved as raw evidence; the rows below are the
refreshed pinned-tree result, with physical and nonblank counts recorded
together.

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-current-core-census-freeze.json
```

| manifest row | baseline files / bytes / physical / nonblank | current files / bytes / physical / nonblank | delta files / bytes / physical / nonblank |
|---|---:|---:|---:|
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 190,569 / 4,442 / 4,097 | +63 / +144,948 / +2,892 / +2,699 |
| Agent `astrid/packs/rendering/actions/timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 54 / 1,292,896 / 28,504 / 25,663 | 0 / +38,945 / +804 / +752 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 29 / 363,113 / 11,053 / 10,680 | 0 / −12,376 / −328 / −313 |
| Agent `astrid/core/timeline/onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 24,162 / 568 / 470 | +1 / +6,006 / +116 / +95 |
| Agent Remotion host source, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 32 / 314,411 / 8,195 / 7,563 | +3 / +31,477 / +662 / +631 |
| **Confirmed canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **206 / 2,203,235 / 53,452 / 49,103** | **+66 / +202,820 / +4,205 / +3,921** |

The manifest path arrays are the source of truth for every row; no product path
was inferred from a line-count total.

## Explicit exclusions

The following remain outside the confirmed total. They are classified in the
JSON manifest and are not silently folded into a deletion or policy decision.

| excluded category | baseline → current files / bytes / physical / nonblank |
|---|---:|
| Composition generated registries/curves/timer declaration | 4 → 7 / 5,228 → 12,628 / 95 → 414 / 88 → 405 |
| Agent visualize schemas | 10 → 10 / 70,613 → 70,613 / 1,941 → 1,941 / 1,925 → 1,925 |
| Agent Remotion generated/declaration/test source | 5 → 4 / 14,636 → 14,228 / 481 → 469 / 419 → 408 |
| App fallback registries/theme shims | 4 → 0 / 4,785 → 0 / 246 → 0 / 229 → 0 |
| Agent old Composition reference `docs/reference/timeline-composition-v0.0.6/**` | 21 → 21 / 57,156 → 57,156 / 1,781 → 1,781 / 1,612 → 1,612 |
| App vendored Composition `vendor/timeline-composition/typescript/src/**` | 21 → 0 / 51,742 → 0 / 1,668 → 0 / 1,504 → 0 |
| App vendored Agent/browser text under the named vendor roots | 169 → 160 / 1,319,619 → 1,309,546 / 36,332 → 36,049 / 35,024 → 34,762 |
| package archives (bytes only; binary line counts are not meaningful) | 0 → 6 / 0 → 284,571 |

Tests are excluded from App active source: the scoped roots classify 26
baseline and 37 current test files separately. The Agent Remotion test is in
the generated/declaration/test bucket. Composition tests are outside its exact
`typescript/src/**` source manifest. The current App vendor Agent tree has 121
exact Agent-snapshot blob matches (868,026 bytes / 21,695 physical / 20,756
nonblank lines), including 15 matches to selected canonical Agent paths
(24,931 bytes / 968 physical / 933 nonblank lines); all are
excluded, so there is no App/Agent double count.

## Adjacent execution/live-scene bucket

These three unchanged paths are explicitly excluded from the 818-line
execution/live-scene bucket at both snapshots:

```text
remotion/src/astrid-frame-worker.mjs       18,569 bytes / 365 lines
remotion/src/LiveSceneClip.tsx              1,114 bytes / 16 lines
remotion/src/ThreeTimelineComposition.tsx  16,837 bytes / 437 lines
subtotal                                  36,520 bytes / 818 lines
```

They are adjacent execution/live-scene infrastructure, not confirmed Timeline
Core. No target claim or policy escalation is made for these already-excluded
paths.

## Five largest remaining ledger-scope path buckets

These are current measured facts for existing open/held viewing-ledger scope,
not new cleanup units or deletion claims. Several buckets contain retained
code, so their full size must not be read as removable size.

| existing ledger scope | current manifest bucket | files / bytes / lines |
|---|---|---:|
| D10 App vendored Agent/browser copies | `vendor/astrid-browser/{astrid/**,remotion/src/**}` plus `vendor/astrid-build-inputs/primary/astrid/**` | 160 / 1,309,546 / 36,049 / 34,762 |
| D09 Agent visualize private/evaluator area | `astrid/packs/rendering/actions/timeline_visualize/**` authored subset | 54 / 1,292,896 / 28,504 / 25,663 |
| D09 Agent scene/render adapters | explicit adapters plus `astrid/packs/rendering/rendering/elements/**` text | 29 / 363,113 / 11,053 / 10,680 |
| D08 App duplicate viewer math area | active non-test `PreviewPanel/**`, `compositions/**`, `render/**` | 32 / 314,411 / 8,195 / 7,563 |
| D10 App vendored Composition copy | `vendor/timeline-composition/typescript/src/**` | 0 / 0 / 0 / 0 |

The D09 and D08 buckets deliberately include public/retained neighboring code
because the corrected manifest measures the settled path boundaries; ledger
status and existing behavior evidence still govern any future deletion.

## Integrated deletions and held debt

These are source-history facts, not new deletion approvals. They are listed so
the refreshed totals do not re-credit excluded or held work:

* Merged: App private trim math (`93cd2f7d4`/`9d518546d`) and the old
  `lib/audioFade.ts` plus test (`887f26265`) are gone; broader D08 host and
  audio/parity work remains open.
* Merged: the dead HTML inspector (`c1a1d4fdb`, integrated by `a760ecca0`) is
  gone: `inspector_viewer.py`, its CSS/JS assets, and its private test. This is
  not the D09 private visibility evaluator.
* Merged: App fallback shims and App vendored Composition/static copies are
  gone (`564a21805`, `1b4ac8b68` and the bounded D10 App landing). These are
  excluded from the canonical total; the Agent D10 source-adapter copy remains
  held pending corrected custom-winner/catalog proof.
* Held: D09 `onscreen.py` private evaluator, motion/mouth/ROI/crop/statistics
  callers, and source-identity/parity gates; D08 mixed
  `VisualClip`/`TimelineRenderer` hosts and full audio parity; and the
  remaining Agent D10 source adapters. No held unit is counted as deleted.

The delivery note must also account for main infrastructure touched outside
this census: Agent process-custody/PID-reuse guards; short-lived Remotion
attempt-temp accounting and owner-root cleanup; and retained source-carry,
source-identity, and verified-source request guards. These are not Viewing
product cuts and are not included in the canonical rows.

## Reproduction and coverage checks

The historical script and JSON above remain preserved as raw evidence for the
earlier frozen pins. The refreshed recount reused the same manifest/path
selection against the three pinned current SHAs, adding physical
`splitlines()` and nonblank `strip()` counters in memory; no repository,
dependency, or shared install was written. The coverage rule is unchanged:
Composition source = authored + generated; Agent visualize = authored +
schemas/stage/docs/fonts/inspector assets; Agent Remotion = core + adjacent +
generated/declaration/test; and App active roots = active + tests + fallback.
The explicit Agent/elements lists, old reference, vendor trees, and archives
remain excluded and were rechecked against the refreshed trees.

The previous document’s historical candidate result (broad 143 → 208 files,
2,036,935 → 2,208,967 bytes, 46,000 → 49,161 lines; confirmed 140 → 205,
2,000,415 → 2,172,447 bytes, 45,182 → 48,343 lines) is retained only as a
minimal provenance footnote. Its Agent `f7584fad`, App `1be0efdd`, and
Composition `5e06f401` current pins are not this current census.
