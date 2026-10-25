# D108/D69 residual EVEN handoff

Status: `SOURCE_ONLY_RESIDUAL_EVEN` (not whole-audit PASS).

Membership: 129 functions; removed 113; added 287. Immutable EVEN assignment: 65 functions. Six assigned functions are excluded because they are exactly covered by core/stage/writers maps (15 total across maps).

Residual after exact approved-row exclusion: **66 assertion units** across **25 functions**, plus **31 zero-delta functions** retained in arithmetic. Approved excluded units: 34.

## Source identity

- original-membership SHA256: `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0` (expected `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`)
- recovered handoff SHA256: `af04bc82117976029346a9a6646b956ab16390627a9d764be6a30ef668ee0411` (expected `af04bc82117976029346a9a6646b956ab16390627a9d764be6a30ef668ee0411`)
- old upstream: `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, tree `2694ae8d2709526b40fa037bda8b159cf412769d`
- captured new: `d6294843286c18e57af3c1874cf1996be42212d2`, tree `6aeae30f0892a424104a4348bca6fd74ba1315d6`
- current normal: `d0ecf1d69a7b37f86034bc52004f73f6c6231603`, tree `e9845f8cf5a6ba80210336d0e2452f80a0918762`
- parser SHA256: `f8a000977ee880cefb4e1d8313157049acc667549a88351d3547b03b5e4c8c96`; manifest SHA256: `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`

## Verdict and constraints

Every residual fingerprint record has old/new/current blob and line data, partition approval status, current applicability, and verdict `UNRESOLVED`. No residual row is cleared by syntax or operator counts. Current-source mismatches are explicit. ODD ownership is disjoint by immutable original index.

Prior XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-F-D69-23762-d69-restored47.xml` SHA256 `005ea787fce46efbba6e5637a6e92ab8e9fb5f83f62e3d48649f0522bf06e2a5`; 49 tests / 39 failures; not executed by this worker. Tests/typecheck/lint are N/A by the source-only brief. No product/test/ledger/registry/generated/foreign output edits.

See `handoff-agt-F-D69-residual-even-0945.json` for complete per-function/per-fingerprint records and `evidence/source-checks.json` for source/hash checks.
