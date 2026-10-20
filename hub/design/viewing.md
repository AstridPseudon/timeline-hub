# Viewing architecture and M4 build contract

Status: M0 complete, M1 recorded, M3 active, M4 delivery incomplete. This is
the concise Viewing handoff; PLAN.md remains the project authority. M5 has not
started. Gate 6 (actual frame and audio parity) and Gate 7 (delivery and owner
film viewing) remain open.

## Architecture

The current public Composition package is `@banodoco/timeline-composition`
0.0.13, an immutable 77-file archive. Its root exports the Timeline
Composition, theme, registry, modifier, duration, scene-preparation, scene
query, and transition helpers; its public `./evaluation` entry point also
exports the audio-envelope compile/apply/WAV and `encodedEnvelopeSource`
helpers. Agent and App remain hosts: they supply the selected timeline and
pinned linked closure, authorized assets, canvas and rational fps, resolved
theme, registries, readiness, and the identity being displayed. Composition
does not fetch Runtime data, save, accept history, certify source authority,
or reconcile application state.

Agent owns the one authored-timing compiler. Composition evaluates the
compiled scene/audio inputs and supplies the existing scene/transition
helpers; it is not a second authored-timeline compiler. This is one public
evaluator seam, not proof that every viewer/private caller has already been
unified: D09 private callers and private ROI/crop/statistics machinery remain
active pending their managed Scene proof and equivalent caller coverage.

The existing named theme-file input/carrier remains the normal theme seam,
but the normal producer that supplies it is still missing. Do not infer
authority from a theme slug or caller-only value, and do not add a resolver,
DTO, or copied theme.

The evaluator is not the frame/audio parity proof. Gate 6 is an independent
App Player/final-export comparison on the same delivered closure, with
picture-only and audio-only negative controls. Existing private pixel checks,
timing checks, and renderer readiness do not close that gate. Unknown font
metrics, media alpha, custom-element internals, and RenderClockTail stay
unknown rather than guessed.

Saving is renderer-free: commit, reload, retry, rebase, undo, and history
acceptance must work with Composition, Node, and the renderer stopped. Preview
failure reports unavailable input honestly; it never blocks or rewrites the
save path. Runtime owns admission and the immutable accepted closure. No
second certification, source factory, universal renderer DTO, or snapshot
rewrite is introduced here.

## Identity and fallback rules

Native inspection and managed render labels are different facts:

- Native inspection uses the factual `inspection.revision_id`. A newly observed
  `head_revision_id`, receipt, or save status never relabels old frames.
- Managed rendering uses the admitted `snapshot_label` for the delivered
  immutable config and linked closure. It is not a native revision claim.
- A failed fresh target keeps the last cached config, closure, and label as a
  cached fallback while reporting the target unavailable. A fresh label is
  allowed only after the source-qualified config and closure are delivered;
  an acknowledgement or old loaded config alone is insufficient.

App's initial canonical read must pair the accepted basis with the factual
local `editProjection` through the existing callback, generation, and race
guards. This accepted-basis/local-projection pairing is a local preview
config fact, not authored or wire data. Only the matching delivered
config/closure may receive its local or accepted label; a local suffix remains
local until that matching accepted basis is installed.

The capture callback remains a narrow, synchronous, read-only observer after
the final scene props JSON is written. It observes resolved assets/theme and
staged parameters inside the existing asset-server lifetime. It is not source
certification or consumer activation. The Agent final-props callback and
`CaptureSceneLabels` prerequisites are owner-merged (`56409ab2`, `f7584fad`)
but inactive until the current source join is qualified.

## Composition 0.0.13

Current immutable source is `5a4e9b72`; the approved archive is:

```text
banodoco-timeline-composition-0.0.13.tgz
SHA-256 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
58,477 bytes, 77 regular files
```

The current integrated Composition tree is
`e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332`. Its qualified full suite
`composition-full-1020230739-25938` passed: **78 passed, 0 failed, 0 skipped**.
The package's default theme remains the existing Agent navy/Arial/cyan
default; explicit film themes remain explicit.

Run the qualified suite from the real Composition root:

```sh
cd /home/user/work/composition
npm test
```

Do not rebuild, repack, or relabel the immutable 0.0.13 archive in a consumer.

## Current delivery boundary

- Gate 6 physical frame/audio comparison remains open and is pending the
  final two home merges (the qualified controller and continuous-PCM caller),
  followed by one fresh frozen central run. No physical parity result is
  claimed.
- D10's vendored Composition and App static/theme implementation copies are
  deleted; this does not retire D09 private callers or claim universal viewer
  or private-ROI unification. The managed Scene proof for D09 is held.
- App preview and normal Agent export consume the same public continuous-PCM
  contract: App's `AudioTrack` playback path and Agent's CPU/export source
  path. This is consumer coverage, not physical Player/export parity.
- The existing named theme-file carrier is approved, but the normal producer
  path is still missing. Active private callers and private ROI/crop/statistics
  machinery remain in place pending the exact Scene/caller proof.
- Exact scanner1.0.8 archive18116B/e87e8870 is approved by the independent gate and Agent's assigned policy reviewer (124shipped/84negative/102codec tests,130independent variants). Ready for delivery selection, no owner-data or macOS claim;1.0.7/1.0.6 remain rejected. See viewing-scanner108-delivery-selection.json.
- Scene source carry de62 is owner-integrated atc456:229PASS/9oldxfail, privatepublic12compat79+125+7PASS; actual host certification/pixels remain unqualified. Root12/presenter and inactive PCM kernel are integrated. Original extent5d is integrated at86405964; actual normal caller b6 is owner-approved and current port remains pending. Real HTTP/WAV central22PASS does not qualify an encoder,MP4,Runtime admission or Player/export parity.
- MAIN5/4/fade source and actual capture-attempt replay prove hold4. First central attempt1020113140-6461 failed before frames due a missing historical theme dependency; source/fullgraph/sixpeer postflight passed. Corrected dependency staging produced central1020115023-5447 PASS/3PNGs/38s, independentRGBmeasurementPASS; actualMAINf105opacity0.5 is now the selectedgolden. Owner11:59 selected golden0.5/currentclamp and WITHDREW renderConfig as unnecessary; proposal closed unapplied.
- Exact source proofs are required for activation. Shared scene graph106added self-links and App graph6added links await lead's local repair confirmation; neither polluted graph qualifies captures. The independent f816 SSR physical graph is clean and reserved for the original MAIN reference.

The deletion ledger is manager-owned and is not edited here. Obsolete rejected
theme proposals and superseded handoff diary entries are pruned rather than
appended. This page records the architecture, exact package evidence, and
remaining owner boundaries only.
