# Viewing Timeline Core — current M4 census

Frozen 2026-10-20T09:05:52Z from the three `tl/integration` branches before
measurement. This is a size census, not a target-achievement claim. Counts are
committed Git blob bytes and nonblank physical UTF-8 lines.

## Frozen inputs

| repo | baseline (`origin/main`) | current (`tl/integration`, frozen) |
|---|---|---|
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `46bd700b2b46ae1cab1e8a1502ed6504e81aa8d8` |
| Agent | `a411628f8fd6129f9c58c332019b56769d997384` | `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e` |
| App | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `18becfbede00038830b97e63345445eeef54fa42` |

Runtime is intentionally absent: its commit/inspection and visual-seam paths
belong to the Runtime-owned census. No branch name or unstable `HEAD` default
is used by the reproducer.

## Confirmed canonical scope

The exact flat manifest and counting code are:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs
```

It reads only committed blobs from the three absolute repository paths. The
JSON produced from those exact refs is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-current-core-census-freeze.json
```

| manifest row | baseline files / bytes / lines | current files / bytes / lines | delta files / bytes / lines |
|---|---:|---:|---:|
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,398 | 79 / 190,523 / 4,097 | +63 / +144,902 / +2,699 |
| Agent `astrid/packs/rendering/actions/timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 24,911 | 55 / 1,270,190 / 25,256 | +1 / +16,239 / +345 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 10,993 | 29 / 366,756 / 10,744 | 0 / −8,733 / −249 |
| Agent `astrid/core/timeline/onscreen.py`, `scene_answers.py` | 1 / 18,156 / 375 | 2 / 24,116 / 469 | +1 / +5,960 / +94 |
| Agent Remotion host source, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 573 | 10 / 27,058 / 613 | −1 / +2,794 / +40 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 6,932 | 30 / 293,804 / 7,164 | +1 / +10,870 / +232 |
| **Confirmed canonical total** | **140 / 2,000,415 / 45,182** | **205 / 2,172,447 / 48,343** | **+65 / +172,032 / +3,161** |

The manifest path arrays are the source of truth for every row; no product path
was inferred from a line-count total.

## Explicit exclusions

The following remain outside the confirmed total. They are classified in the
JSON manifest and are not silently folded into a deletion or policy decision.

| excluded category | baseline → current files / bytes / lines |
|---|---:|
| Composition generated registries/curves/timer declaration | 4 → 7 / 5,228 → 12,628 / 88 → 405 |
| Agent visualize schemas | 10 → 10 / 70,613 → 70,613 / 1,925 → 1,925 |
| Agent Remotion generated/declaration/test source | 5 → 4 / 14,636 → 14,228 / 419 → 408 |
| App fallback registries/theme shims | 4 → 0 / 4,785 → 0 / 229 → 0 |
| Agent old Composition reference `docs/reference/timeline-composition-v0.0.6/**` | 21 → 21 / 57,156 → 57,156 / 1,612 → 1,612 |
| App vendored Composition `vendor/timeline-composition/typescript/src/**` | 21 → 21 / 51,742 → 51,742 / 1,504 → 1,504 |
| App vendored Agent/browser text under the named vendor roots | 169 → 169 / 1,319,619 → 1,319,619 / 35,024 → 35,024 |
| package archives | 0 → 2 / 0 → 108,672 / 0 → 429 |

Tests are excluded from App active source: the scoped roots classify 26
baseline and 27 current test files separately. The Agent Remotion test is in
the generated/declaration/test bucket. Composition tests are outside its exact
`typescript/src/**` source manifest. The current App vendor Agent tree has 123
exact Agent-snapshot blob matches (882,979 bytes / 21,122 lines), including 15
matches to selected canonical Agent paths (24,931 bytes / 933 lines); all are
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
| D10 App vendored Agent/browser copies | `vendor/astrid-browser/{astrid/**,remotion/src/**}` plus `vendor/astrid-build-inputs/primary/astrid/**` | 169 / 1,319,619 / 35,024 |
| D09 Agent visualize private/evaluator area | `astrid/packs/rendering/actions/timeline_visualize/**` authored subset | 55 / 1,270,190 / 25,256 |
| D09 Agent scene/render adapters | explicit adapters plus `astrid/packs/rendering/rendering/elements/**` text | 29 / 366,756 / 10,744 |
| D08 App duplicate viewer math area | active non-test `PreviewPanel/**`, `compositions/**`, `render/**` | 30 / 293,804 / 7,164 |
| D10 App vendored Composition copy | `vendor/timeline-composition/typescript/src/**` | 21 / 51,742 / 1,504 |

The D09 and D08 buckets deliberately include public/retained neighboring code
because the corrected manifest measures the settled path boundaries; ledger
status and existing behavior evidence still govern any future deletion.

## Reproduction and coverage checks

```sh
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-current-core-census-freeze.json
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs > /tmp/vw-m4-current-core-census-freeze.repeat.json
cmp -s /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-current-core-census-freeze.json /tmp/vw-m4-current-core-census-freeze.repeat.json
```

The repeated JSON is byte-identical. The coverage check reconciles every path
under each measured source root: Composition source = authored + generated;
Agent visualize = authored + schemas + stage/docs/fonts/inspector assets;
Agent Remotion = core + adjacent + generated/declaration/test; and App active
roots = active + tests + fallback. The explicit Agent/elements lists, old
reference, vendor trees, and archives are each emitted as path arrays too.

The previous document’s historical candidate result (broad 143 → 208 files,
2,036,935 → 2,208,967 bytes, 46,000 → 49,161 lines; confirmed 140 → 205,
2,000,415 → 2,172,447 bytes, 45,182 → 48,343 lines) is retained only as a
minimal provenance footnote. Its Agent `f7584fad`, App `1be0efdd`, and
Composition `5e06f401` current pins are not this current census.
