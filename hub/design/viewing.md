# Viewing architecture and delivery — M4 current handoff

Status: M0 is complete and M1 is recorded. Composition is ready for the
coordinated consumer update. App and Agent 0.0.12 adoption is still pending,
M3 consumer activation is not integrated, Gates 6 and 7 are open, and M5 has
not started. This page is the current build and delivery contract; the PLAN
remains authoritative for project-wide decisions.

## Architecture

There is one public Composition evaluator package:
`@banodoco/timeline-composition`. It supplies pure scene and track answers,
the TimelineComposition renderer, bundled defaults, and the one registration
seam for host-resolved elements, animations, effects, and transitions. The
canonical transition boundary is incoming-authored input converted once to the
serializable compiled vector consumed by scene preparation and rendering.

The evaluator answers what the supplied scene means. It does not prove pixel
or audio parity. It does not fetch Runtime data, save, accept history, certify
source authority, or reconcile application state. App and Agent remain thin
hosts: they supply the already selected timeline and pinned linked closure,
assets and authorized URLs, actual canvas and rational fps, resolved theme,
host registries/dispatch, media and font readiness, and the local or committed
identity for the input being displayed. The host keeps its existing media,
audio, export, and lifecycle behavior; Composition is not a replacement host.

The current public scene transport is a thin input adapter, not an authority
factory. It accepts supplied props and basis and returns public scene rows,
preserving unknown or unavailable answers. Production activation still needs
the Agent source-owner join from the exact post-resolve or historical source,
occurrence mapping, and materialized Root props at the same host lifetime.
Shape, status, receipts, or source-looking metadata cannot certify those
inputs. No new source factory, certificate API, universal renderer DTO, or
Runtime transport is part of this handoff.

The current capture callback is equally narrow: the existing
`on_scene_props(merged_props, actual_capture_frames)` observer runs after the
final props JSON is written, with resolved assets/theme and staged parameters,
inside the existing asset-server lifetime. It is synchronous and read-only;
omitted or `None` preserves the old call shape, and an observer failure uses
the existing cleanup path. Capture still has no delivered profile, so the
profile must come from `_canonical_profile(...)` over the same frozen
materialized inputs, including width, height, and rational fps. This callback
is not source certification or a production consumer activation seam.

Keep the existing `fast_lane` and `sweep` pixel verification, private pixel
checks/statistics, legitimate adapters, and Agent `_timing_evaluators.py`.
Retire duplicate viewer formulas only after named public behavior tests and
the trusted source join cover them. Unknown font metrics, media alpha,
custom-element internals, and RenderClockTail remain unknown rather than
guessed.

## Identity, delivery, and saving

Native inspection and managed render labels are different facts:

- Native inputs use the actual `inspection.revision_id`; `head_revision_id` is
  separate context and never relabels the inspected revision.
- Managed inputs use the admitted `snapshot_label` tied to the delivered
  immutable config and closure.
- A receipt, global save status, or newly observed head does not relabel old
  frames. A failed target leaves the cached config, closure, and label intact
  while reporting the target as unavailable.

App's initial canonical read must pair the accepted basis with the factual
local `editProjection` through the existing callback, generation, and race
guards. That paired fact is local preview state, not authored or wire data.
Only the matching delivered config/closure may receive the corresponding
accepted or local label. An acknowledgement by itself, or an old loaded
config/head, is not proof of what the player displays. A local suffix remains
local until its matching delivered accepted basis is installed.

Saving is renderer-independent. Commit, reload, retry, rebase, undo, and
history acceptance must work with Composition, Node, and the renderer stopped.
Preview failure reports unavailable input honestly and does not block or
silently rewrite the save path. Runtime remains responsible for admission and
the immutable accepted closure; no second certification or snapshot rewrite is
introduced here.

## Composition 0.0.12 artifact and consumer instructions

Use the immutable artifact, not a rebuild or source checkout:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz
sha256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
sha512 490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==
bytes 58444; files 77
```

The package source is the final `5e06f401` lineage. Locked build, repeat-pack,
fresh ESM/SSR, strict NodeNext, and the central 69-test package lane pass;
the built public root/theme API also matches the Agent default-theme object.
The host peer tuple is React and React DOM 18.3.1, Remotion/media/layout-utils
4.0.509, qualified with Node 20.19.4 and npm 10.8.2. Keep package bytes
immutable and do not regenerate package files in a consumer.

Adopt 0.0.12 directly as one App/Agent pair after the official matching
Runtime/client tuple is published. That pair is pending and is not integrated
in this handoff. Consumer owners own their package, lock, bundler, and host
changes; the package remains opaque to them. Explicit themes remain explicit;
the package's final `banodoco-default` is the existing Agent navy/Arial/cyan
default (`bg #050814`, `fg #FAFAFA`, `accent #67E8F9`).

The old 0.0.11 artifact and source remain immutable historical references only:
`dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`.

## Build and test commands

Composition's real-repository checks are:

```sh
cd /home/user/work/composition
npm run build
npm run gen-registry:check
npm run build:test
node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/*.test.js
npm test
```

The central service uses the repository's allow-listed `composition full`
suite (`npm test`), requested once after the last source change:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <worker-name> full)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

After the App/Agent pair and official Runtime tuple land, use the central
consumer suites rather than local browser or socket runs: `agent full`,
`app full`, `app full-e2e-timeline`, and the named
`app e2e-viewing-frame-parity` lane for actual Player/export comparison.
The frame lane must use the same delivered closure and package bytes and must
include its independent picture-only and audio-only negative controls.

## Delivery status and gates

The App helper's 43.8-second qualification proves host launch/readiness/stop
and dependency identity only. It is not a rendered frame, Player audio,
Player/export parity, or Gate 6 result. Snapshot-deletion incident replays are
complete; do not rerun them without a new cause.

Gate 6 remains open until the actual App Player and final export pass picture
and mixed-audio comparison on the pinned closure, with both one-host mismatch
controls. Existing private pixel verification and timing evidence do not close
that gate. Gate 7 remains open until repository gates, the coordinated ZIP,
fresh-main application, and owner-film viewing are complete. No macOS claim is
made.

M4 work is therefore delivery and qualified cleanup around the existing
interfaces, not a new framework or another evaluator. M5 extension work waits
for the PLAN hard stop and has not started.
