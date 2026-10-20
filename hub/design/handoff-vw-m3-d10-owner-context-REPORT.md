# D10 owner packet publication and current-App context

Published the existing D10 donor packet without changing its contents:

- `design/handoff-vw-m3-d10-owner-packet.patch`
- `design/handoff-vw-m3-d10-owner-packet-REPORT.md`
- `design/handoff-vw-m3-d10-owner-packet-COMMAND`

The patch is the original `UNAPPLIED.patch` (SHA-256
`f5dbc5cbbf5c2fa62246c761a4401c12fc530eda90134d156b191432a9f08bb5`) and
contains one Home migration plus exactly nine vendored implementation-file
deletions. The original report and command were copied unchanged.

## Exact public13 seam

The Home migration consumes
`src/tools/video-editor/runtime/publicCompositionElementRegistry.ts` from
the bridge commit `27ee90ac1`. Its
`PUBLIC_COMPOSITION_ELEMENT_COMPONENTS` map is assembled from the installed
Composition 0.0.13 `ANIMATION_REGISTRY`, `EFFECT_REGISTRY`, and
`TRANSITION_REGISTRY`, keyed as `animation:<id>`, `effect:<id>`, and
`transition:<id>`. This is the precise implementation seam for the nine
Composition-owned defaults:

- animations: `fade`, `fade-up`, `scale-in`, `slide-left`, `slide-up`,
  `type-on`;
- effect: `text-card`;
- transitions: `cross-fade`, `fade`.

The bridge supplies implementations only. The Astrid public catalog at
`vendor/astrid-browser/astrid/packs/rendering/elements/public-catalog.ts`
remains authoritative for Home descriptors, schema, `packId`, revision,
renderability, `componentPath` identity, and diagnostics/public-host API.
The patch therefore preserves the catalog import and the host's existing
registration, lookup, capability, and unknown-element behavior.

## Home, standalone Vite, and custom checkout preservation

The patch leaves these `@astrid-public` consumers in Home unchanged:

- `audio-reactive-colour`;
- local `end-spanning-layer` and `frame-overlay` components;
- their card/frame asset URLs and the existing preview asset wrapper.

Normal Vite keeps the explicit `ASTRID_PUBLIC_CHECKOUT` path through
`config/vite/vite.config.ts` (`resolveAstridSource(...,
'ASTRID_PUBLIC_CHECKOUT')` and the `@astrid-public` alias). The standalone
public-host Vite config keeps its absolute-checkout requirement, realpaths
`<checkout>/astrid`, and the same `@astrid-public` alias in
`scripts/astrid-landing/public-host-browser/vite.config.ts`. The patch does
not change either resolver, the custom checkout contract, the standalone
root, the Composition 0.0.13 artifact/lock, or any package export.

## Nine remaining source paths

These are the only implementation files deleted by the packet:

```text
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/fade/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/fade-up/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/scale-in/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/slide-left/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/slide-up/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/animations/type-on/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/effects/text-card/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/transitions/cross-fade/component.tsx
vendor/astrid-browser/astrid/packs/rendering/rendering/elements/transitions/fade/component.tsx
```

The catalog's descriptor `componentPath` strings and the immutable
`vendor/astrid-build-inputs` public source closure are data/provenance
inputs, not additional runtime callers, and remain untouched by the packet.

## Current App context verification

On current worker HEAD `b0efbffae569a8af11b2ebf1998dc5174c184b9b`:

```text
git apply --check .../UNAPPLIED.patch       PASS
```

The check confirms the ten patch paths and their textual contexts (six
insertions, 301 deletions), but it does not prove the imported bridge is
present. The current HEAD has no
`src/tools/video-editor/runtime/publicCompositionElementRegistry.ts`, and
`27ee90ac1` is not an ancestor of this HEAD. This is bounded context drift:
the owner must first land the bridge commit (or an equivalent approved
bridge) before applying this unchanged packet. No product edit or test was
made here, and the donor patch was not rewritten to hide the prerequisite.

## Sequencing and ledger

The source-provenance blocker remains: the owner needs an actual Astrid
source commit that omits these nine files, then must run the normal vendor
refresh and verifier so `vendor/astrid-browser/provenance.json` and declared
vendor-source inputs are regenerated from that source. No invented hashes,
manual provenance claim, or vendor deletion approval is implied. D10 remains
HELD until the owner lands the last consumer and completes that provenance
sequence.

Inherited donor evidence is preserved in the copied report; its targeted
tests and probes were not rerun for this publication-only task. No browser,
full suite, install, network, live socket, or build was run here.
