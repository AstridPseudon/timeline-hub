# F-D86 new-source handback

This is a source-only handback. It binds exactly 21 newly affected IDs to the
three independently reviewed Agent source candidates. It does not claim a
behavior result or authorize a registry/body/collection change.

## Membership

- `parentmedia`: 18 IDs from the historical `editing` fixture in actual19214.
  The retained family ledger has 20 IDs, but its two fresh-film cases use the
  `custody` fixture (`historical=False`), were already PASS, and do not reach
  the f261c9 historical delta. They are therefore preserved but excluded here.
- `sheetCLI`: the exact `[cli]` and `[sheet-cli]` entries of the changed
  semantic-batch parametrization. The unchanged lost-ack test remains a
  separate exact-tuple row.
- `graph`: the graph-roots selector in the changed source file. The second
  graph original is in an unchanged historical-redo file and is not rebound.

`selectors.txt` is the canonical membership source. The actual19214 route
retains the old dispositions: parentmedia 18 FAIL, sheetCLI one FAIL and one
PASS, graph one FAIL. Missing traceback frames remain UNKNOWN; none are
reconstructed here.

## Source bindings and call trace

The exact candidate blob, SHA-256, source commit/tree, normal receipt, and
independent review identity are in `source-hashes.tsv` and `manifest.json`.

- `f261c9...`: the historical-only `media_realm` setup adds the occurrence
  lane and changes the occurrence track placement. Original values, commands,
  assertions, refusal/retry, inverse, ABA, and no-write guards are conserved.
- `b68d6b...`: the semantic-batch setup binds `head['publication_id']` in the
  `before` bundle read. The original commands, opaque values, assertions,
  refusal/retry, inverse, ABA, and no-write guards are conserved.
- `e5f5...`: the graph realm registers the existing `chapter-1` scope in
  addition to `film`. Parent film, topology, opaque values, assertions,
  refusal, inverse/redo, ABA, and no-write guards are conserved.

All routes remain `test source -> RuntimeService -> registered
load_timeline_commit_provider('astrid') -> commit_timeline`. Existing MAIN
Runtime receiver dependencies are named and hashed in `source-hashes.tsv`; no
Agent worker author/body/controller duplication is introduced.

## Boundaries

Runtime-owned `new13`, original550, D95 NEW two, held D100 projection, and M1
legacy rows remain separate historical dispositions. This packet does not edit
the D106 ledger, wait for a union, change policy/authority, or claim behavior
qualification. C0 v2 request/reply semantics and historical rebased retries
remain unchanged.

## Verification scope

Static-only checks are recorded in the worker evidence. No pytest, collection,
fixture/helper/function execution, service, browser, render, install, or full
suite was run for this source handback.
