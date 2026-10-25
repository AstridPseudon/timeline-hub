# D114 isolated registerAsset terminal

- Service: `app-pin-04beedcd-p2-d114-asset-0855-1025085739-15712`; target `app-pin-04beedcd`; terminal FAIL, exit 1, 236s.
- Source preflight: PASS (exit 0, 3s).
- Readiness: PASS 1/1; original: FAIL 1/1, 0 errors, 0 skipped.
- First unmet predicate: `tests/e2e/local/three-products.p2-elements-assets.spec.ts:655` — expect(envelope.data).toEqual(expected.data); called from `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1179:18` during guarded native Undo.
- XML: readiness c470c6e49c69056bf14533d7f0c04807b7c1024b06f428a5745b079848a90a2b; original 52b6e9ce6befb3a0c0c4c3648d94c5f7995b3fab080ca45309c73ebd4408108f. Manifest SHA: 6e33b356616420d606dca46f3797535cd91e2d2c1b431c13971c35e2c7ae483f.
- Manifest confirms exact four heads/trees, Node v20.19.4, schema digest, source hashes unchanged before/after, readiness exit 0 and original exit 1.
- Retained runtime-private files searched are listed in `terminal.json`; phase 1 was complete (57 events, no drops), repeated-start phase 2 retained 4 summaries with a bounded rolling buffer (346 seen, 218 dropped, 128 retained).
- No bounded D102/reason/correlation marker was found in the searched stderr/stdout/stack files. Backend outcome remains UNKNOWN; no cause is inferred.
- No retry, duplicate, retarget, collector, alternate route, or output cleanup was used; all run outputs remain preserved.
