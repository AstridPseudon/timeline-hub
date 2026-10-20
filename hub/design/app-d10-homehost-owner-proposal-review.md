# App D10 Home/Vite/root owner review

Review time: 2026-10-20 17:35 UTC, with one bounded 10-second wait after the
peer request.

## Result

The Viewing D10 donor proposal was not published. The 16:40 App inbox entry
only announces an unapplied worker proposal; no D10 patch, file list, or
report exists under `ORCH/design/` after the wait. I sent one direct peer
request at:

`design/peer-app-to-viewing-20261020T1735-d10-homehost-proposal.md`

No Home/root/vendor implementation was made, and this review does not approve
vendor deletion.

## Current source and exact consumers

The reviewed source is current App13 at `tl/integration` `c57dcc261` (whose
refresh parent is Main `bebadd0e1`, integrated by `969941059`). The only App
runtime file that imports public Astrid rendering components is:

`src/pages/Home/astrid-public-host.tsx`

Its 12 registered component entries split exactly as follows:

| Host entry | Current source | D10 classification |
| --- | --- | --- |
| `animation:fade` | `@astrid-public/.../animations/fade` | Composition builtin; migrate to `ANIMATION_REGISTRY.fade` |
| `animation:fade-up` | `@astrid-public/.../animations/fade-up` | Composition builtin; migrate to package registry |
| `animation:scale-in` | `@astrid-public/.../animations/scale-in` | Composition builtin; migrate to package registry |
| `animation:slide-left` | `@astrid-public/.../animations/slide-left` | Composition builtin; migrate to package registry |
| `animation:slide-up` | `@astrid-public/.../animations/slide-up` | Composition builtin; migrate to package registry |
| `animation:type-on` | `@astrid-public/.../animations/type-on` | Composition builtin; migrate to package registry |
| `effect:text-card` | `@astrid-public/.../effects/text-card` | Composition builtin; migrate to `EFFECT_REGISTRY.text-card` |
| `transition:cross-fade` | `@astrid-public/.../transitions/cross-fade` | Composition builtin; migrate to `TRANSITION_REGISTRY.cross-fade` |
| `transition:fade` | `@astrid-public/.../transitions/fade` | Composition builtin; migrate to `TRANSITION_REGISTRY.fade` |
| `effect:audio-reactive-colour` | `@astrid-public/.../effects/audio-reactive-colour` | Custom Astrid pack; keep host loading |
| `effect:end-spanning-layer` | `@astrid-public/.../local/.../end-spanning-layer` | Custom/local pack; keep host loading and asset wrapper |
| `effect:frame-overlay` | `@astrid-public/.../local/.../frame-overlay` | Custom/local pack; keep host loading and asset wrapper |

The six `end-spanning-layer` card URLs and `frame-overlay` URL are also
custom-pack assets and must remain on the Astrid public-source alias. There are
no other runtime imports of those nine package-owned builtin component paths
in `src`, `scripts`, `examples`, `config`, or `tests`.

The four 2rp theme effects (`art-card`, `cta-card`, `resource-card`,
`section-hook`) are already consumed through
`src/tools/video-editor/sequences/registry.ts` and
`@banodoco/timeline-composition/registry.generated`; they are not remaining
D10 Home consumers. The package’s existing registry test covers all 13
Composition defaults.

Other `vendor/astrid-browser` imports are not these builtin components:
`boundary.ts`/`seam-intent.ts` are custom seam contracts,
`remotion/src/fonts.ts` and vendored font assets serve font loading, and
`config/vite/astridSource.ts` plus the tool-catalog verifier validate the
bundled Astrid source. `vendor/astrid-build-inputs/{primary,public}` is a
source-closure/provenance tree, not a discovered runtime consumer. None of
those may be removed as part of the nine-component D10 migration.

## Seam verdict

The public package seam is viable, but only with a two-authority split:

1. `@banodoco/timeline-composition` registries own the nine component
   implementations listed above.
2. `@astrid-public/packs/rendering/elements/public-catalog.ts` remains the
   authority for Home descriptors, schema, `packId`, revision, source,
   renderability, and diagnostics/public-host API. The Composition package
   registries do not expose the complete Astrid public descriptor contract and
   must not replace it.
3. `@astrid-public` remains the loader for `audio-reactive-colour`, the two
   local effects, and their assets. `ASTRID_PUBLIC_CHECKOUT` must continue to
   override the bundled checkout in both the normal Vite config and the
   standalone `scripts/astrid-landing/public-host-browser/vite.config.ts`.

The Home host’s existing `resolveComponent(elementId, kind, packId)` lookup,
descriptor list, 12-entry registration check, sequence registry, dynamic
custom sequence behavior, and `describeClipCapability` behavior must remain
unchanged apart from where the nine implementation values come from. A custom
checkout must be able to change the custom pack implementation/catalog without
changing the package-owned builtins, and a missing package builtin must fail
visibly rather than fall back to a vendored duplicate.

## Minimal patch scope once the donor is published

App-owned changes should be limited to:

- `src/pages/Home/astrid-public-host.tsx`: replace only the nine builtin
  component imports with the Composition public registry values; keep the
  catalog import, custom imports, asset wrapper, registration checks, and host
  capability methods.
- The narrow adjacent Home/host tests needed to prove the split described
  below.
- `config/vite/vite.config.ts`, the standalone public-host Vite config, or
  `package.json`/lock only if the donor demonstrates a real resolver/root
  change. Current App13 already pins the immutable
  `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, so the older
  Mainbebadd assumption of `vendor/banodoco-*` directories is stale and must
  not be reintroduced.
- `scripts/build/verify-astrid-vendor-sources.mjs` only if its import checker
  is changed by the donor. It should continue to verify the remaining custom
  `@astrid-public` imports and vendored provenance; it must not require the
  nine Composition builtins to be present in `vendor/astrid-browser`.

No Composition, Agent, Runtime, Home product, or vendor deletion approval is
implied here. Viewing/Composition must supply and approve the package export
and artifact seam; App owns the eventual root/lock and vendor cleanup after
the last consumer is qualified; the orchestrator owns ledger/stop-point
acceptance.

## Retirement evidence required after migration

Before deleting any D10 copy, run the following against the correct installed
0.0.13 package (not the shared 0.0.10 dependency currently present on this
machine):

- `node config/vite/timelineCompositionPackage.test.mjs` — root/lock/artifact
  identity, all six Vite/Vitest/public-host configs resolving the public
  package exports, shared React/Remotion peers, and Node SSR subpaths.
- Targeted Home/host tests covering `PublicAstridEditorProvider.test.tsx`,
  `EditorRuntimeProvider.test.tsx`, and
  `TimelineRenderer.public-host.qualification.test.tsx`: all 12 catalog
  descriptors register; each of the nine package components resolves by
  kind/id/pack; custom checkout loading still resolves the three custom
  components and assets; diagnostics/capability responses and public API
  shape are unchanged.
- A focused custom-checkout test must prove the package-owned nine do not
  silently resolve from the checkout, while `audio-reactive-colour`,
  `end-spanning-layer`, `frame-overlay`, and their asset URLs do.
- `node scripts/build/verify-astrid-vendor-sources.mjs` (or its replacement
  verifier) must pass with only the custom Astrid imports remaining in the
  Home host.
- A final static guard should find no Home/runtime import of the nine
  package-owned component paths through `@astrid-public`; it should still find
  the catalog, three custom component imports, and custom asset imports. The
  guard must not count `vendor/astrid-build-inputs` or custom seam/font
  contracts as D10 consumers.

Only after those tests pass, the package artifact/lock identity is qualified,
and no other App consumer is found, may App remove the nine obsolete source
copies and update the deletion ledger. The custom Astrid source closure and
its non-D10 consumers remain.

## Evidence and limits

Read-only source inspection used `rg`, `git show`, tar listing/stream reads of
the committed 0.0.13 artifact, and the current App13 tree. No full suite,
TypeScript check, build, install, browser, or vendor/root edit was run.

The focused command:

`node config/vite/timelineCompositionPackage.test.mjs`

had 1 passing subtest and 8 failures because the read-only shared install at
`/home/user/work/app/node_modules/@banodoco/timeline-composition` resolves
version `0.0.10`, while App’s tracked package/lock/artifact require `0.0.13`.
The package/lock identity subtest passed; no dependency was changed to make
the other assertions green. This is environment evidence, not qualification
of the proposed D10 seam.
