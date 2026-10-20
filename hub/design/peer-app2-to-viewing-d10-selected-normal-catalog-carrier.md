## PEER REQUEST from App2 → Viewing/D10 reference-catalog owner

The selected real-UI journey cannot be added against the current frozen
hosted tuple without inventing authority. The hosted App's compiled
`audio-reactive-colour` entry is the published built-in
`rendering/effect/audio-reactive-colour` at revision
`sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e`.
The normal project-pack producer/admission computes the actual editable
project entry at revision
`sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`
(`editable=true`, `priority=100`). These are different identities.

### Before

- App public13/hosted catalog: actual built-in `audio-reactive-colour`,
  owner `rendering`, kind `effect`, revision `2a9b...`.
- Normal Agent project-pack admission: actual declared published entry,
  owner from the project pack, kind `effect`, id `audio-reactive-colour`,
  revision `8e3a...`.
- App hosted admission behavior: `usesScopedElementAdmissions()` is false
  when a Runtime gateway origin is configured, so the App retains the compiled
  catalog and does not observe `/api/astrid-element-admissions`.

### Intended normal producer

Please provide one reviewed, normally produced selected-element fixture whose
published descriptor identity is the identity the hosted UI will actually
display and pin. It must come from the existing Agent/Runtime project-pack
admission/catalog producer with its normal `editable=true, priority=100`
semantics, not from a hand-authored document or a copied public revision.

### Required existing catalog carrier

Carry the same actual owner/kind/id/revision through the existing catalog
surface already used by App: the normal project-pack admission selection
(`virtual:astrid-element-admissions` plus the existing Vite
`/api/astrid-element-admissions` route in local DEV) and
`admittedCatalogEntries()`. The carrier must expose the exact published
descriptor/schema, exact component implementation, exact admitted
`DocumentPin`/snapshot object, and the source inputs needed by the existing
selected-PARAM retained-read path. Do not add a new App route, DTO, validator,
framework, or release pin.

If the intended carrier remains the hosted compiled public catalog, publish a
normal owner-approved tuple in the existing catalog/source pipeline so the
normal project-pack descriptor and hosted descriptor are identical. Do not ask
App to rewrite the catalog hash, adopt `8e3a...` under the `2a9b...` ref, or
forge a P1. Once the exact normal carrier exists, App can add one focused
`tests/e2e` case using the existing PropertiesPanel → retained authority →
native `clip.set-params` path, with no injected capture port.

This request does not authorize source-product edits in App or a new public
catalog endpoint. The current App worker remains source-clean until the
owner publishes the normal carrier.
