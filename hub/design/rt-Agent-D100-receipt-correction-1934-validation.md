# D100 corrected evidence validation

Result: `PASS_CORRECTED_DERIVATIVE_ONLY`; behavior remains `FAIL_BEHAVIOR_PENDING`.

This packet is an evidence-only derivative. The author1914 receipt and the independent author1919 review remain byte-exact at their original paths. No Agent source, test, product, pin, generated file, Runtime input, or receipt outside this derivative was edited.

## Git-resolved identity

All values below were resolved from the read-only Agent repository `/home/user/work/agent`, not copied from the task brief:

- `git rev-parse 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1^{commit}` → `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1`.
- `git rev-parse 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1^{tree}` → `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`.
- `git rev-parse 9486cbb06e2ab53402086772e6c2bc18bc4849fc^{tree}` → `0919e511bd28b3d3af76bb18155efda12c3e94f6`.
- `git diff --name-status 9486cbb06e2ab53402086772e6c2bc18bc4849fc 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1` → only `M tests/sdk/test_d100_item_birth_boundary.py`.
- Recursive `git ls-tree` comparison → 3,568 base entries, 3,568 final entries, one changed entry, and no outside changed entries.

Protected product identity:

- Path: `astrid/sdk/timeline/_command_state.py`.
- Final Git blob: `09cbeeddefdc6375ba7d026406c95fb35bafda40`.
- Final SHA-256: `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a` (64 hexadecimal characters).
- Base Git blob and SHA-256 are identical to final; product unchanged.

Changed-test identity:

- Path: `tests/sdk/test_d100_item_birth_boundary.py`.
- Git blob: `39ed571d5f3e49d2545fc31e1f868ee7c58dbc8a`.
- SHA-256: `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37` (64 hexadecimal characters).

The seven read-only Agent source/test files in the derivative `source_hashes` section were each read with `git show 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1:path`; every SHA-256 matches the author1914 manifest and every Git blob is recorded. The retained Runtime reference resolves to commit `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.

## Correction and immutability checks

The original author1914 source manifest is preserved unchanged:

- Path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-test-return-1914/evidence/source-manifest.json`.
- Size/hash: 2,503 bytes; SHA-256 `f9e42e82588912099b2117fce5251a873b441c16f73cdd68c78852baef512fd3`.
- Its two recorded protected-product values are intentionally retained as historical evidence: both are 63 characters and end in `...fa808a`.

The corrected derivative is separate:

- Path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-receipt-correction-1934/evidence/source-manifest.json`.
- Size/hash: 6,655 bytes; SHA-256 `500b81c1be929f655d220ed8be39dde68f2e513c67530c0634b57816d9f1fe91`.
- Both corrected protected-product fields equal the Git-resolved 64-character SHA-256 ending in `...fa808a3`.
- Final commit/tree replace both author1914 `PENDING_HARNESS_COMMIT` values.

The preserved author1919 independent review remains at its original path with SHA-256 `bc680c958f1cb8c268ce6ff13cfdaad1a8b96ac81a0d774ec348cc3c8291992a`. Its substantive purpose/static checks remain input evidence; its overall FAIL was only the two historical truncated hash strings. This derivative does not convert the unrun behavior check into a PASS.

JSON parsing, SHA-256/SHA-1/ref length checks, source-manifest byte counts, and the complete-tree arithmetic above passed. No pytest, lint, typecheck, provider/body, App, Runtime, live, security, or full suite was rerun, as required by the brief.

## Receiving disposition

The corrected packet requires one later independent receipt-only check against the actual Agent Git data. After the admitted 5,000,000,000-byte floor and the corrected Agent queue, the bounded Agent behavior test may run; App remains the sole behavior receiver afterward. No product acceptance is made here. D130 remains held.
