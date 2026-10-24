# Report: agt-F-count-giant-review-0827

PASS — cumulative read-only review of all five artifacts.

- Verified 267 IDs/phases/tags, all ours: **263 closed / 4 open**.
- Exactly one giant original closure; 266 node records and 122 prior mappings byte-identical.
- Verified 123 mappings, 50 prior proof records plus one scoped proof, owner/family totals, CSV/JSON parity, XML, source blobs, and 38-member rationale with 37 unchanged.
- Full `CONTRACTINVENTORY` and historical Farm/RED/restart limits preserved.
- Census SHA-256: `e13d65bad98c46f90ab9dd037ae9b20d2c99a650c3db6827b65d4d542a1b24a0`
- Package SHA-256: `8171638af8e1ec3f1fb00f52c70da21989f50c0c0b9214fe457524ad9a91da9e`
- No source, test, product, network, HTTP, full-suite, or candidate retry actions performed.

Checks:

- Standalone stdlib validator: PASS.
- Raw byte-preservation validator: PASS.
- `python3 -m json.tool`: PASS.
- `git diff --check`: PASS.
- Retained NumPy wheel finite check: PASS — 926 RECORD rows, zero hash/size mismatches, no duplicate/unsafe paths or `.data` relocation.
- NumPy installed Store entry is absent; exact installed triggering rows remain unavailable. No cause inferred.

Manager may publish the exact five authored bytes as the official 263/4 census. No blockers for this review.