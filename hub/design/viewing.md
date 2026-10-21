# Viewing architecture and M4 build contract

Status: M0 complete, M1 recorded, M3 active, and M4 delivery incomplete. The
current source-only Composition frontier is `tl/integration`
`7bb54bbd64107e5090643ecca1e4d33164173e85` (tree
`20467712e66dbadff4d562c0d5baae22b8c077a7`). PLAN.md remains the project
authority; M5 has not started.

## Architecture

The immutable consumer artifact remains `@banodoco/timeline-composition`
0.0.13: source `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`, tree
`13e375534fffd704305eced5686699d2c8c9c948`, 77 files, SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
The current 7bb source-only tree is newer source, not a published 0.0.14
artifact. No source14 archive or pin exists.

Composition is the one evaluator for the supplied scene. Its public root and
`./evaluation` entry points provide the Timeline Composition, scene
preparation/query, theme, registry, modifier, duration, transition, and pure
audio-envelope helpers. Agent and App remain hosts: they supply the selected
timeline and pinned linked closure, authorized assets, canvas and rational fps,
resolved theme, registries, readiness, and the identity being displayed.
Composition does not fetch Runtime data, save, accept history, certify source
authority, or reconcile application state.

Agent owns the authored-timing compiler. Composition evaluates compiled
scene/audio inputs and supplies the existing scene/transition helpers; it is
not a second authored-timeline compiler. This is one public evaluator seam,
not proof that every viewer/private caller has already been unified: D09
private callers and private ROI/crop/statistics machinery remain active
pending their managed Scene proof and equivalent caller coverage.

The normal explicit-theme path is the existing Main path: imported
`theme.json` enters project CAS through `media.import_file`, is passed as
`inputs.theme`, materialized by GenericHost, resolved by the existing resolver,
and arrives as `props.theme`. When absent, the existing builtin default remains
in force. Do not infer authority from a theme slug or caller-only value, and do
not add a ThemeDocument, `themeSource`, resolver, DTO, copied theme, or new
producer requirement. This records the orchestrator's 02:04 ruling; the
deferred preparation/source-selection contracts are not part of M4.

The evaluator is not the frame/audio parity proof. Gate 6 is an independent
App Player/final-export comparison on the same delivered closure, with
picture-only and audio-only negative controls. Existing private pixel checks,
timing checks, and renderer readiness do not close that gate. Unknown font
metrics, media alpha, custom-element internals, and RenderClockTail stay
unknown rather than guessed.

Saving is renderer-free: commit, reload, retry, rebase, undo, and history
acceptance must work with Composition, Node, and the renderer stopped. Preview
failure reports unavailable input honestly; it never blocks or rewrites the
save path. Runtime owns admission and the immutable accepted closure. No second
certification, source factory, universal renderer DTO, or snapshot rewrite is
introduced here.

## Identity and fallback rules

Native inspection and managed render labels are different facts:

- Native inspection uses the factual `inspection.revision_id`. A newly observed
  `head_revision_id`, receipt, or save status never relabels old frames.
- Managed rendering uses the admitted `snapshot_label` for the delivered
  immutable config and linked closure. It is not a native revision claim.
- A failed fresh target keeps the last cached config, closure, and label as a
  cached fallback while reporting the target unavailable. A fresh label is
  allowed only after the source-qualified config and closure are delivered;
  acknowledgement or an old loaded config alone is insufficient.

App's initial canonical read must pair the accepted basis with the factual
local `editProjection` through the existing callback, generation, and race
guards. This accepted-basis/local-projection pairing is a local preview config
fact, not authored or wire data. Only the matching delivered config/closure
may receive its local or accepted label; a local suffix remains local until
that matching accepted basis is installed.

The capture callback remains a narrow, synchronous, read-only observer after
the final scene props JSON is written. It observes resolved assets/theme and
staged parameters inside the existing asset-server lifetime. It is not source
certification or consumer activation. The Agent final-props callback and
`CaptureSceneLabels` prerequisites are inactive until the current source join
is qualified.

## Current source evidence

The current 7bb source-only delivery was already verified; this publication
does not rerun it. Its retained artifacts are:

| artifact | SHA-256 |
| --- | --- |
| source patch | `327178ed354ed9f624addecd86f859820f0607b27d779d9f355adcce84f50063` |
| source bundle | `f06812274384792bb6a3d5103448d3eada33ca6f869550ce463481f60e615981` |
| manifest | `e4cad42b1106bbd85eb6d3440a6eba2c215d38d1e3ee0a392366cd68c3c6db5d` |

The central purity suite for that exact source is
`composition-full-1021014707-6851`: **84 passed, 0 failed, 0 skipped**. The
unchanged strict purity guard is included in that result. This is evidence for
the 7bb source tree, not a claim that a package archive was published.

The approved scanner 1.0.8 and installed carrier inputs remain unchanged:

- scanner: `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- carrier: `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`

The bounded Viewing census was completed before the final Composition 7bb
refresh. Preserve that captured identity rather than relabelling it as a 7bb
census:

| captured scope | files | bytes | physical lines | nonblank lines |
| --- | ---: | ---: | ---: | ---: |
| exact Main baseline | 140 | 2,000,415 | 49,247 | 45,182 |
| actual current home integrations | 197 | 2,227,916 | 53,657 | 49,316 |
| current minus Main | +57 | +227,501 | +4,410 | +4,134 |

The measured Composition identity for that tuple was `4788e107f…` (tree
`585e8c47…`); Agent and App were the recorded current heads in the census
report. The tuple is bounded evidence, not a current-all-repo census, final
M4 freeze, foundation-complete claim, or size gate.

## Current qualification boundary

Gate 6 remains **OPEN**. The sole authorized public13 physical lane has no
positive result in the retained evidence. The latest authorized attempt
`vw-m3-gate6-approved909-physical-execute-e2e-viewing-gate6-0129-1021013633-19275`
failed before physical execution with a shell parsing error; it produced no
render, PNG, frame/audio comparison, or parity result. The separate 0221
preflight also stopped during fixture setup and did not launch a browser or
render. Do not relabel either as a physical positive unless a later actual
result is recorded.

The normal export attempt remains a separate unqualified integration fact. It
used the captured Agent `d0a5072b` source lane and stopped before admission at
the existing `/tmp` disk guard with 10,538,319,872 bytes free, below the
required 10,737,418,240 bytes. No MP4, frame/audio parity, or export
certification follows, and this task does not rerun it.

Physical frame/audio parity, macOS playback, owner-film viewing, a 0.0.14
archive, and the whole-project ZIP remain unclaimed. The next authorized
steps are the single fresh public13 Gate 6 run after the App ancestry guard
passes, then delivery packaging and owner-film viewing. No unchanged
delivery, full suite, census, build, browser, or physical run is part of this
publication.

The deletion ledger is manager-owned and is not edited here. This page records
the architecture, exact source evidence, and remaining owner boundaries only.
