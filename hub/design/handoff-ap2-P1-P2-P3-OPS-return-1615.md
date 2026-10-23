# Handoff — ap2-P1-P2-P3-OPS-return-1615

Static shell qualification is ready for the three authorized App suite rows.

- App selected source/tree: `0b3cef4d21610031049b2c8809089a730d0abfbe` / `2652d85a0ab40bcf0e88443f721dc4b868eeb743`
- Agent selected source/tree: `98ef2f9c95fd43d88cca2909d8d1518302e3050c` / `ed007d6efc06135b5978d8a11a71609b0f476f14`
- Runtime selected source/tree: `2593942dfbbbe1d70bb6e776f811285deb2ab18b` / `3bd06dc517f347976541ae4dde3caf3d29d03419`

P2’s nested `bash -c` payload is losslessly shell-quoted and round-trips to the prior current payload; P1/P3 payloads also round-trip. All three outer commands and extracted inner payloads pass `bash -n`. Assignment/eval fail-fast controls prove inner nonzero and parse failure do not reach the success marker. P2’s original eight-journey tail is restored; P1’s original tail and P3’s Gate 5 grep tail are preserved byte-for-byte after selected App identity substitution.

Native seed is NOTRUN. The prior service result 1366’s summary pass is rejected because its log has the nested unexpected-EOF and no seed. Do not credit actual journeys until the existing service-owned bounded preflight produces a real seed GREEN.

One protected source gate remains visible: current clean App tree P1 body is `38ada64bb2596254472e93974a44893987a87db1` / `5b3bcc0bf55f55236d0bb738bc66d69c4c8a963698952ff5c0f65f73829d014c`, while the unchanged P1 guard expects `daa50e…` / `098d631e…`. This is owner-receipt/merged-tree pending, not a reason to weaken the guard.
