# Viewing architecture and M4 build contract

Status: M0 complete, M1 recorded, M3 active, M4 delivery incomplete. This is
the concise Viewing handoff; PLAN.md remains the project authority. M5 has not
started. Gate 6 (actual frame and audio parity) and Gate 7 (delivery and owner
film viewing) remain open.

## Architecture

There is one public Composition evaluator: `@banodoco/timeline-composition`
0.0.12. It answers what the supplied scene means and provides the compiled
scene/track data, renderer components, defaults, and registration seam. Agent
and App remain hosts: they supply the selected timeline and pinned linked
closure, authorized assets, actual canvas and rational fps, resolved theme,
registries, readiness, and the identity being displayed. Composition does not
fetch Runtime data, save, accept history, certify source authority, or reconcile
application state.

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

App’s initial canonical read must pair the accepted basis with the factual
local `editProjection` through the existing callback, generation, and race
guards. This paired config/projection fact is local preview state, not authored
or wire data. Only the matching delivered config/closure may receive its local
or accepted label; a local suffix remains local until that matching accepted
basis is installed.

The capture callback remains a narrow, synchronous, read-only observer after
the final scene props JSON is written. It observes resolved assets/theme and
staged parameters inside the existing asset-server lifetime. It is not source
certification or consumer activation. The Agent final-props callback and
`CaptureSceneLabels` prerequisites are owner-merged (`56409ab2`, `f7584fad`)
but inactive until the current source join is qualified.

## Composition 0.0.12

Current Composition source is `a62e7d266`; the restored Makefile is present and
the package is immutable:

```text
banodoco-timeline-composition-0.0.12.tgz
SHA-256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
58,444 bytes, 77 files
```

The exact package/API smoke `1020085340-3498` passed in a fresh private
consumer (Node 20.19.4; ESM, SSR, scoped-host, strict NodeNext, peer identity,
and immutable-package checks). The Composition full run
`1020091054-4980` passed: **69 PASS, 0 FAIL, 0 SKIP**. The package’s default
theme is the existing Agent navy/Arial/cyan default; explicit film themes stay
explicit.

Run these from the real Composition root; the package argument is deliberate:

```sh
cd /home/user/work/composition
make build
make test
npm run test:package -- \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.12.tgz
```

`test:package` defaults to the current package version (0.0.12). The standard
`npm run build && npm pack --ignore-scripts && npm run test:package` also passed,
rebuilding the exact immutable 77-file archive. The old 0.0.11 archive remains an immutable
historical reference only. Do not rebuild or repack 0.0.12 in a consumer.

## Current delivery boundary

- The native decoder is the approved two-file App delta `4360c759`, ready for
  owner port. The exact capture delta `1ba0800af` still awaits the App helper
  closure `320784f82`. The actual native frame qualification remains **2 PASS,
  2 FAIL**; no parity claim is made.
- Scanner 1.0.7’s independent review passed **40 tests** (the 1.0.6 baseline
  remains 36); its policy decision is owner-pending. The shippable scanner is
  bounded inspection metadata, not owner data. No owner-film or macOS claim is
  made.
- The current scene-source unit has **201 PASS and 9 pre-existing XFAIL**; its
  current-port integration remains in flight. The normal PCM actual-caller,
  window, and layer join also remains in flight. Do not activate from a
  callback shape, package presence, stale source, or readiness smoke alone.
- Exact source proofs are required for every activation. The shared scene graph
  has **106** added self-links and the App graph has **6** added links; both
  repairs are held pending owner approval. Capture and environment
  qualification using either graph remain held.

The deletion ledger is manager-owned and is not edited here. Obsolete rejected
theme proposals and superseded handoff diary entries are pruned rather than
appended. This page records the architecture, exact package evidence, and
remaining owner boundaries only.
