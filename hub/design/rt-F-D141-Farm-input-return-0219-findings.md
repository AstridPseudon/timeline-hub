# D141 Farm input-producer findings

## Result

The complete 01:50Z packet is addressed in one source pass. The frozen
Agent/Runtime/App/Composition source objects are present and their current
checkouts are clean. The actual census recorded Agent, Runtime, and App
checkout receipts as `PASS`; only the Composition receipt was mismatched
because the earlier filename used 39 hex characters. Farm already requested
the normal checkout again with the full 40-hex Composition commit. The venue
remains `NOT_READY`: there is no D141 installation summary, physical D139a
schema carrier/RECORD/direct_url/trusted manifest, Farm-bound 2149 census,
original dependency wheelhouse, or current control-plane routes/profile.

The 22 rows are intentionally split into two categories:

- Supplied producer artifacts: installation summary, schema dist-info files,
  canonical census, dependency wheelhouse, and source/child/D73 receipts.
  These must be produced by the existing reviewed maker, D139a carrier, D139
  census owner, or normal receipt route.
- Farm manager control-plane observations: central service/suite, D73 dry and
  core route executables, profile, disk witness, and retained root. These are
  venue bindings/observations, not producer artifacts and not things this
  source-only packet may invent.

## Decisions preserved

- The qualified route is the ordinary D139a installed-schema route. The
  existing requester/maker guard refuses installed schema plus Farm schema
  authority; no source adapter or guard change is needed.
- CAS2309/installed2314 is historical kit provenance. Its maker hash is
  genuine (`fd83c9e2…`, 111171 bytes, 0755), but that does not prove that the
  physical schema bytes are installed on Farm.
- The 2149 census is the only canonical input packet. The 2216 work is a
  finite review/reconciliation of that packet, not a retargeted current
  census. Historical evidence is not rewritten.
- D124 core and D134 positive/poison recipes remain the existing commands;
  no body, service, import, or core action was run.
- C0 request/reply shapes were read and preserved; no product, schema, client,
  pin, test, receipt protocol, or guard was changed.

## Review finding closure

The independent 0208 review found one stale documentation claim: Runtime/App
receipt closure was incorrectly described as absent. That claim is removed in
this derivative. The 22-row map remains the original census-check list; it
does not grow to 24 rows for the three receipts already marked `PASS`. The
remaining receipt item is only the Composition full-40-hex recheck.

## Genuine absent prerequisites

The exact owner and next command for every row are in `input-map.json` and
`commands.md`. The only prepared portable artifact awaiting admission is the
corrected Composition receipt. Agent/Runtime/App receipt closure is already
PASS in the actual census and must not be requested again. No guessed Farm
paths are presented as inputs.
