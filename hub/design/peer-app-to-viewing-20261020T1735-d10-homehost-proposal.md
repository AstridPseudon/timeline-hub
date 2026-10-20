# PEER REQUEST from App — 2026-10-20 17:35 UTC

The 16:40 inbox entry says the Viewing D10 Home/Vite/root proposal is being
prepared, but no D10 proposal, patch, file list, or report is currently
published under `ORCH/design/`. Please publish the unapplied donor packet for
the bounded App owner review, including the exact package/export and test
seam.

The review will use current App13 (`tl/integration` c57dcc261) and must keep
these boundaries explicit:

- Composition-owned defaults come from the public `@banodoco/timeline-composition`
  registries: animations `fade`, `fade-up`, `scale-in`, `slide-left`,
  `slide-up`, `type-on`; effect `text-card`; transitions `cross-fade`, `fade`.
- The Astrid public catalog remains descriptor/schema/pack/revision/
  renderability authority for Home diagnostics and the public API. The
  package registry supplies component implementations, not a replacement
  catalog.
- Custom host loading remains on `@astrid-public`/`ASTRID_PUBLIC_CHECKOUT`:
  `audio-reactive-colour` plus local `end-spanning-layer` and `frame-overlay`
  (and their assets). Do not route these through Composition or delete the
  bundled Astrid source closure.
- Preserve the public host's registration and capability/diagnostic behavior,
  the explicit custom-checkout override, and the standalone public-host Vite
  alias. Do not assume the old Mainbebadd `vendor/banodoco-*` tree exists;
  current App13 uses the immutable 0.0.13 artifact.

Please include the exact remaining consumer file set and the tests that prove
package-owned builtin imports are gone before any D10 vendor deletion is
approved. App will not edit Home/root/vendor or invent a patch while the donor
packet is unpublished.
