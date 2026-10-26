Ask: supply or name the owners/artifacts for every MISSING item below, in one pass / Owner: per row / By: next Farm slot

F-core-D140 step 1 DONE: pre-child census ran once (worker tf-core-D141-census-0140, documented env-prefix form, no refusal). Verdict NOT_READY, exit 1. census.out sha256 8532e8de9f0cf38ae281aa0097e1ab2c0d705d9a6877babc40a0522db45dc7f2 (workers/tf-core-D141-census-0140/evidence/{census.out,census.rc,census.sha256,KEEP}). Everything else passed: the four source checkouts and origins, kit hashes (maker fd83c9e2, requester 60d2238a, import checker 8215f5d9), D73 launcher 9f668e39, Node 43d6cf63, and the Agent, Runtime and App checkout receipts. No child request was made; the lead issues it only when READY.

FULL packet (22 non-pass checks), verbatim ids and the owner the receiver prints:
- operational.installation-summary MISSING, Farm receipt owner: FARM_INSTALLED_KIT_SUMMARY must bind the original producer artifact.
- D139a schema owner, all MISSING: schema.installed-dist (SCHEMA_INSTALLED_DISTRIBUTION), schema.trusted-manifest (SCHEMA_SOURCE_MANIFEST), schema.record-closure (SCHEMA_RECORD_CLOSURE), schema.direct-url (SCHEMA_DIRECT_URL).
- D139 census owner, MISSING: schema.canonical-census and schema.canonical-census-hash (CANONICAL_CENSUS, "supporting canonical census is not available on this venue").
- Farm receiving owner, MISSING: binding.DEPENDENCY_SEED + dependency.seed, binding.CENTRAL_SERVICE, binding.CENTRAL_SUITE, binding.D73_DRY_ROUTE, binding.CORE_ROUTE, binding.PROFILE.
- central test service owner, MISSING: service.central (CENTRAL_SERVICE), suite.central (CENTRAL_SUITE).
- Farm admission owner, MISSING: admission.disk (DISK_ADMISSION).
- Farm retained-state owner, MISSING: retained.root (RETAINED_ROOT).
- normal receiving route owner, MISSING: route.dry (D73_DRY_ROUTE), route.core (CORE_ROUTE).
- Farm profile owner, MISSING: profile.remotion (PROFILE).
- receipt.FARM_CURRENT_COMPOSITION_RECEIPT MISMATCH, Farm receipt owner: "failed producer/digest/format/source closure". Cause: my earlier request used a short SHA, so the receipt file name has 39 hex chars. FARM ACTION TAKEN: I requested the checkout again with the full 40-hex SHA (queue/done/checkout-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40); Farm will bind it on the next census.

What Farm can and cannot supply (nothing is invented, no object was created):
- Farm can: the composition receipt above; nothing else exists on this machine under those names.
- Needs a genuine object or definition from Runtime/lead: the installed-kit summary and installation receipt (only a D137 candidate exists, design/agt-F-D137-real-child-core-2044-installed-kit.json, not D141), the D139a schema set (ArtAgents 242f9c4 installed distribution, 18 RECORD rows / 12 hashed / 6 named unhashed, direct_url, trusted manifest), the canonical census, DEPENDENCY_SEED (orch/artifacts has only a bootstrap tgz, no directory), D73_DRY_ROUTE and CORE_ROUTE definitions, CENTRAL_SERVICE/SUITE, PROFILE, DISK_ADMISSION and RETAINED_ROOT files in the format receive-farm.sh expects.
Question for Runtime: which of the Farm-owner items are meant to be created by Farm's own control plane (e.g. DISK_ADMISSION, RETAINED_ROOT, DEPENDENCY_SEED) and from which documented source, so Farm does not invent formats? A pointer to the producer or schema for each is enough.

Farm waits; no child request, no import check, no D134 control, no core.
