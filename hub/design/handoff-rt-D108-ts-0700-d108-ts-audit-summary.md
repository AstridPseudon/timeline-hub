# D108 App/Composition TypeScript source audit

Verdict: **FAIL for App; PASS for Composition source accounting**. This is a
read-only source verdict. No Vitest, TypeScript compiler, lint, browser,
provider, build, install, or live-service command was run.

## Identity and reconstruction

The audit consumed manifest SHA-256
`37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504` and the
reverse-audit report. It archived each fresh upstream commit into a private
`/tmp` directory, applied the exact recorded patch, computed Git tree/blob
objects without writing the Git object database, and compared the result to
the recorded applied tree.

| repo | fresh commit/tree | applied commit/tree | patch SHA-256 | tree |
|---|---|---|---|---|
| App | `d11417a59` / `e9079c61` | `5391d71d8` / `204a9216697953f765b5bd550aefa5822503a44c` | `6ea5ce83b888a3f789c1b38d53f0180195ce27cf6248286116d22ff11c9a19a1` | exact |
| Composition | `67b8aa3d0` / `62f4456b` | `ccd3a1084` / `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `14f43521a1423d00fad4ac12774ed80e20ed3d5f4f0e235aec9cf5fff265aad3` | exact |

App has 1,335 exact test-file blobs, 66 modified, 193 added, and 2 deleted.
Composition has 17 added and 2 deleted test files. App source-blob checks
were 1,338 total; 1,336 pass. The two expected identity exceptions are the
fresh-gate transition for `src/app/onboarding/WelcomeConnection.test.tsx`:

- recorded upstream blob `30fdfd9527f2da15bbaced1c792f44f1ec96ee41` is from
  the captured gating base, while fresh `d11417a59` is
  `13de70b05d0ad287b83205ded4be91e962294b8b`;
- the actual applied blob is
  `04ca84de9c34443625b0942fd4b00cbcad36228f`, differing from captured old
  blob `26df345b4496372cc93d2e805976e89ccca4bb56` only by the applied source
  transition/trailing newline, not by predicate content.

`WelcomeConnection.sameOrigin.test.tsx` blob
`52a491d8c5d483ad97ecc802fa0569b8bd0d42dd` and
`WelcomeJourney.integration.test.tsx` blob
`9438787642d765e7c5a0fd6876b7a3a03b749e74` are exact retained applied blobs.
The changed WelcomeConnection file retains its incoming and local-hand-off
predicates at current source lines 79–185, including the separate-window,
reparented-tab, reload, same-tab, local-choice, and three-row unsupported
browser matrix. No D105a source from old `0b6cee` was used for credit.

## Predicate accounting

The strict named-predicate census is in `d108-ts-audit.json`; its matcher no
longer ordinal-pairs a missing named test with an unrelated current test.

App: 14,733 upstream test units, 15,993 applied units, 1,257 exact units in
modified files, 92 named matched units changed, 36 mechanically removed
assertion lines, 78 added assertion lines, and no matched timeout or
skip/todo/only delta. The remaining 91 named unmatched upstream units are:

- 49 `NewChatMenu.test.tsx` units: intentional U3b retirement in
  `app-U3b-freeze-plan-0647.md:41` and
  `app-U3b-live-first-return-sol-2022.md:17`;
- 13 `TourChatPanel.test.tsx` units: intentional non-restoration because the
  old switch is absent; replacement is the real integration suite,
  `app-U3b-live-first-return-sol-2022.md:20`;
- 5 `timeline-save-utils.test.ts` command-runner units plus the one
  structured-validation unit: D52 `APP-A4-D37-EXECUTOR`,
  `deletion-ledger.app.md:74`;
- `sha256.test.ts:689`: retired command-runner/parity predicate, covered by
  the same D52 ledger row;
- renamed/adapted current predicates in `main.bootstrap-order.test.tsx`,
  AgentChat/AgentChatMenu, `useTimelineHistory.test.ts`,
  PanelFullscreenFrame, element-adapter, and the three-products summary
  guard: manually mapped to the current applied source and the U3b/D69/D01
  decisions; their exact current line/body records are retained in the JSON.

One App unmatched predicate is not cleared:

`src/integrations/runtime/dataProvider.test.ts` upstream line 625,
“loads project-scoped canonical revisions and restores through a current-head
CAS”, has no current named predicate. Its six positive history/restore/CAS
assertions were replaced by refusal behavior in the applied source. The
retirement context is documented by `runtime-api-surface.md:9,25` and D01 in
`deletion-ledger.app.md:6`, but that row is still OPEN/WAITS; there is no
exact approved decision authorizing rewriting this passing positive behavior
to refusal. This is the finite App FAIL gap.

The principal matched changes were accounted as follows:

- bootstrap order and self-hosted font predicate: approved current mapping in
  `deletion-ledger.app.md:62` and `handoff-app-F-quality-quality-fonts-1054.md:5`;
- current head-pair additions (`headPublicationId`) in
  `dataProvider.parity.test.ts:462` and `dataProvider.test.ts:406` are strict
  current-shape additions, not relaxed comparisons;
- vendor-lock count/fixture changes are additions/stricter exclusions;
- AgentChat/menu/model-line renamed labels, selector structure, immediate
  model-start behavior, and removed old-image predicates are the U3b current
  menu contract (`app-U3b-final-review-0738.md` and
  `app-U3b-live-first-return-sol-2022.md`);
- voice behavior is explicitly retained as the gated matrix at applied
  `AgentChat.test.tsx:919–951`, matching the D69 voice restoration
  (`app-U3-D69-voice-restore-1626.md` and
  `app-U3-D69-voice-review-1633.md`);
- PanelFullscreenFrame’s applied source restores `aria-modal=true`, body
  scroll, and shell-root/Escape predicates at lines 18, 71–78, and 81–108;
  this is the exact D69 restore-needed behavior, not a weakening;
- TimelineRenderer’s source identity is tightened to
  `bundled:2rp@0.1.0`, matching D10’s immutable public-package decision in
  `deletion-ledger.viewing.md:43`;
- useTimelineHistory and element-adapter changes follow the Runtime-owned
  history/current CAS decisions in `deletion-ledger.app.md:7,50`;
- three-products browser changes retain or strengthen body, retry identity,
  recovery, closure, and history predicates. The retry accounting is the
  exact D53 row at `deletion-ledger.app.md:88`; the normalized command shape
  is D82 at `deletion-ledger.app.md:109`.

Unresolved App label-signature review: `timeline-save-utils.test.ts:343,
586,640` removes explicit display-label/signature-strip predicates and
replaces them with identity/full-config signatures. The known source
classification records the resulting label-bearing signature mismatch as
unresolved (`app-full8bd8-current-classification.md:24–45`); no source-only
approval was found for treating those removed label predicates as equivalent.
This is reported as a second App review gap, separate from the one unmatched
project-revision test.

## Composition

Composition has 2 upstream test units and 74 applied units, with no changed
upstream units. The two deleted scaffold predicates map to the exact
`VW-ROOT-SCAFFOLD` ledger replacement (`deletion-ledger.viewing.md:68`):
`scripts/gen-registry.test.mjs`, `typescript/tests/registries.test.ts`, and
the immutable package smoke. The deleted `theme-api-smoke.ts` has no runtime
test call; its compile/type-smoke replacement is the exact
`VW-ROOT-THEME-API` row (`deletion-ledger.viewing.md:69`). All 257 Composition
source/blob checks pass and the computed applied tree is exact.

## Method limits and evidence

`d108_ts_source_audit.py` is syntax-checked with Python `ast.parse` and uses
only stdlib Git-object/archive/patch/hash reads. It does not import or execute
product code. No TypeScript parser was available or acquired. The lexical
matcher records 77 specific syntax limits (regex/template/TSX and similar
unmatched-call shapes); every limit is listed in the JSON. Therefore this is
source accounting, not semantic AST equivalence or runtime qualification.

