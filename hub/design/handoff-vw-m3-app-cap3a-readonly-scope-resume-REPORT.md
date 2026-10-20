# REJECT — App exact3a stored-cap review

Decision: **REJECT exact commit `3a4350f9d9a578f817568d5fe348c5d750595129`** for the requested joint App cap gate.

## Scope and source identity

- Exact source: `3a4350f9d9a578f817568d5fe348c5d750595129` (`3599fc49ad76dfdd7847ab4c813fc9317a0304eb` parent).
- Subject: `fix(app): port stored occurrence cap onto integration root`.
- `git diff --check 3a4350f9d^ 3a4350f9d`: exit 0.
- No product files were changed in this review.

## Passing evidence

The exact source was archived into this worker's private scratch tree and run
with only the clean private12 leaf-link overlay:

- public12 `@banodoco/timeline-composition`: exactly 77 files;
- 47 real scope directories and 531 individual leaf links;
- no leaf link targets `/home/user/work/app/node_modules`;
- no shared dependency/cache/venv mutation was used.

Targeted Vitest lanes passed:

- `serialize`, draft-config, persistence, command-projection, and popup tests:
  **5 files, 180 passed, exit 0**;
- stored-cap surface, preview surface, lifecycle, canonical image-cap, and
  shot-projection tests: **5 files, 60 passed, exit 0**.

The exact App project check also passed:

```text
node <clean-private12>/node_modules/typescript/bin/tsc \
  -p tsconfig.app.json --noEmit --pretty false
exit 0
```

The producer review is otherwise consistent with the requirement: the one
derived `app.canonicalTiming.storedOccurrenceDurationMs` is projected from the
verified occurrence duration, retained through graph/local/recovery/accepted
paths, and removed/restored at serialization exits without a new store, wire
field, DTO, or `renderConfig` carrier. Editor/read geometry remains based on
the effective duration.

## Blocking findings

1. The exact tree does not carry the same compiled transition vector and
   projection fact into the still boundary. `TimelineFramePreview` accepts only
   `config`, `request`, and `bounds` at line 104; its Thumbnail input at line
   131/195 is only `{ config, astridElementHost }`. Its caller at
   `VideoEditorAssetPanelSurface.tsx:106` passes no vector, bounded duration,
   paired config, or fact. This is the still-delivery omission identified by
   the corrected consumer handoff.

2. The exact tree does not carry the same compiled vector into client render.
   `useClientRender.ts:271` passes only `{ config: resolvedConfig,
   astridElementHost }`; `useClientRender` has no vector parameter, and
   `useRenderState` does not compile or pass one. Therefore the required
   vector/extent/fact atomic delivery is not shared across still, Player, and
   client-render consumers.

3. `boundCanonicalRenderConfig` only changes a clip when its stored scalar is
   a finite number below the effective duration. Missing, nonnumeric, NaN,
   infinite, or negative stored metadata returns the clip unchanged rather
   than explicitly selecting the existing effective-duration fallback per
   clip. The corrected consumer donor's per-clip fallback behavior is not
   present in exact3a. The existing projection may mask some cases, but the
   render-bound helper itself does not establish the required invariant for
   all canonical/command-projection inputs.

## Limits and required next step

No browser, network, install, full suite, live socket, render, or pixel/audio
parity run was performed. The 240 passing tests and typecheck do not waive the
consumer omissions above.

Apply the corrected consumer donor's paired config/fact/vector plumbing to the
same exact producer descendant, preserve per-clip effective fallback for all
invalid stored scalars, then rerun the focused producer lane plus the donor's
115-test consumer lane and the ES2020 project check.
