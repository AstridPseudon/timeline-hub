# Handoff: ap2-P1-corrected-spec-current-port-0939

Source-only P1 port is complete on base `35a7382a45762d9f2f320146e29959e6ec895d4c`.

The sole worktree change is the exact donor file
`tests/e2e/local/three-products.p1-chain.spec.ts` from
`ad94e470389e4fc05b7c827200085c8b03fe356c`. Its final Git blob is
`6d428522d630fb30115707d6f364b9bd28d23e51`, and its SHA256 is
`06104227304e7bab77e8f3f2de131ef26a949db437d02c2b2d7e20a25c057518`.
The donor and final file compare byte-for-byte. The reviewed `from: 2` → `from: 0`
oracle correction, final reply diagnostics, and `fields` merge expectation are present;
the original accepted/merged/refused, new-ID, raw/opaque/absence/order, lost-ACK,
restart, rollback, and canonical assertions remain in the exact donor.

Evidence: P1 Playwright list found exactly 2 tests; scoped ESLint, normal root and
Node TypeScript, diff check, frozen Runtime/Agent identity, normal Runtime lock, and
the exact Composition archive identity passed. The isolated private-graph App check
reproduces the known held TS2322 at `shotTimelineDataProvider.ts:771`; it was not
weakened or hidden. No browser/body/HTTP/socket/service/build/full/request run was made.

Harness commit and final post-commit tree are pending. Keep remote adoption held until
the actual parent is merged and the branch contains only this one test commit.
