# Runtime D94a/D97 release, 2026-10-25T04:25Z

Released normal Runtime head: `0c62dfa63db9ff608ac9338388431e31a814e080`.
Tree: `e22cdd54b668acea9fe593e6724b34d1a56f7530`, exactly the independently reviewed final candidate `fec6ca4fc7dbaaeae319eb61429aed4d1ee457cf`.
Store blob: `32eed5b11316a9cf647dc36ed87bce0d2bd9fa86`.
History-state test blob: `00fd477ee663775ec44c3562f8af00ebb68f919f`.
Normal merge receipt: queue/done/merge-rt-D97-permission-gate-sol-0412, merged to0c62.

Independent final security0420 PASS covers the D94a baseline-absorption race, pinned SQLite connection, transactional change checks, DB/WAL identity/times, restart/refusal/lifecycle behavior and retained forgery witness, plus D97 actual owner/mode eligibility and full-verify fallback. Different-owner coverage uses controlled stat witnesses; privileged real chown is unverified.

Exact-tree targeted results:267passed,74configured deselections; final reviewer local263passed with45s and durableXML. Central six-file result is exact-tree cached267PASS with authentic logs and noXML; no XML reconstructed. Inherited Ruff/Pyright diagnostics reduce11to10 and74to54, zero added identities.

Only store and focused history-state tests differ from released6634. All schema and canonical15 client blobs are unchanged, including schema `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`. Consumer adoption is source/provenance only through existing normal tooling; no client regeneration needed.

Protected default forward N3–22 remains286SQL,11decodes,one new-entry verification; warm reads27SQL,zero decode/digests. Ineligible stores fully verify on every request with a diagnostic. Inverse ancestry cost still grows and originalP4<45s is UNPROVED. No P2/P4/full-suite/final-cut credit is inferred.

Next: normal Agent and App adoption, then one remaining originalP4 onmain and fullP2 directly onApp perD94a. Isolate only gestures failing that fulltour. ExistingP1/P3 and three isolatedP2 GO retain historical tuple scope. D59 and genuine installed render still required.
