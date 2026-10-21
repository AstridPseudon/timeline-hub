# Exact 1120 central preflight — 2026-10-21 11:26 UTC

Status: **HOLD / preflight failed; no physical phase.**

The one newly registered composition suite was requested once and reached
terminal exit 1:

`vw-m3-reviewed1120-one-central-preflight-1126-e2e-viewing-reviewed1120-preflight-1126-1021112642-1058`

The exact command was:

`bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-final-stage-metadata-path-correction-1120/packet/run.sh --preflight`

Grant, packet SHA256SUMS (`965c12bb71a1579518e1b1f6a2fb60d0a526ccfa9296df199f2171e0954cc1ec`),
fresh marker absence, canonical paths, central snapshot tree
`71d8e95edb1bb2d187c3193ef3462d4cfde277fa`, budget, fd9 lock, syntax/static
checks, and cleanup passed. The retained stage audit then failed before the
main preflight: actual Runtime graph
`f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a` versus
granted `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`.
No preflight JSON was produced. `token-issued:false`; no marker, grant,
Runtime, helper, browser, physical comparison, or export occurred.

Raw evidence:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-reviewed1120-one-central-preflight-1126-e2e-viewing-reviewed1120-preflight-1126-1021112642-1058/log.txt`

The immutable stage remains leased and unchanged. Preserve the actual inner
cause and existing local audit/direct-tar evidence; do not restage intact
source solely because a metadata/graph path failed. No physical action is
authorized from this result.
