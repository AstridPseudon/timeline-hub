# Corrected stored-cap consumer final gate

Decision: **APPROVE the corrected consumer proposal for App joint-port review; consumer-only approval, not App producer or merge approval.**

## Review scope

Reviewed the complete unapplied `consumer.patch` and `tests.patch` from
`handoff-vw-m3-stored-cap-consumer-preserve-boundaries-*` against the exact
clean App base `b1ef4b9b910ba72375c34cf319692f90d22edc25`.

The prior rejection findings are corrected:

- `TimelineFramePreview` now receives the existing compiled transition vector,
  bounded duration, selected private config, and projection fact through the
  existing private invocation seam. `PanelFrameAnchor` is unchanged.
- Stored-cap selection is validated per clip. Missing, negative, nonnumeric,
  `NaN`, and infinite values use the old effective occurrence duration. A
  valid zero retains the existing zero-length filtering semantics.
- The source editor/read config is not mutated. A valid stored cap creates only
  a private invocation copy, including the selected effective duration needed
  by the public evaluator. No second store, `WeakMap`, DTO, serialized field,
  public API, or alternate compiler was added.
- A config with no valid stored scalar stays on the old effective-bound path;
  one valid scalar does not bypass per-clip fallback for the rest.

The existing Player/client-render delivery, editor/read, mailbox, and
late-ACK/provenance coverage remains in the handoff. The 4000/4500 lifecycle
case keeps the source config unchanged and verifies render ends 120/135 with
opacity 0.5/1 respectively.

## Independent evidence

Exact clean-base patch checks:

```text
git -C review/app apply --check consumer.patch
git -C review/app apply --check tests.patch
```

Result: both patches applied cleanly to the exact clean `b1ef` archive.

Focused correction regression, run with an owned Vite cache and the shared
`node_modules` tree read-only:

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config review/app/candidate.vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  --testNamePattern='uses only the private stored occurrence cap|uses the effective cap for missing and invalid stored metadata|does not clamp malformed stored metadata|delivers the paired vector and bounded extent|bounds only the private stored-cap render copy' \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts \
  src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
```

Result: **3 files passed; 9 tests passed, 24 filtered; exit 0.**

The donor's reported 115-test/6-file Vitest run, scoped ESLint, scoped
TypeScript check, and clean-base patch checks were inspected but not repeated;
this gate was intentionally limited to the still-vector and mixed-invalid
regression group.

## Unverified and next step

App producer recomputation from graph/local/recovery/accepted sources and
raw-context/authored/wire/storage stripping remain **UNVERIFIED**, as required
by scope. No App producer/session/type/pin or product-source edit was made.
No full suite, browser, render, socket, network, install, or git mutation was
performed.

Next step: App may apply this consumer proposal only as part of its exact joint
producer candidate, then run the producer serialization/readback tests and the
full mounted consumer neighbor lane on that shared candidate before merge.
