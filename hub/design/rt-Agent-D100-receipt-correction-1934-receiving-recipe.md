# D100 corrected evidence receiving recipe

Carrier: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-receipt-correction-1934`

Corrected derivative source manifest: `evidence/source-manifest.json`  
Derivative SHA-256: `500b81c1be929f655d220ed8be39dde68f2e513c67530c0634b57816d9f1fe91`  
Derivative bytes: `6655`  
Original author1914 source manifest (preserved, not replaced): `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-test-return-1914/evidence/source-manifest.json`  
Original SHA-256: `f9e42e82588912099b2117fce5251a873b441c16f73cdd68c78852baef512fd3`

The derivative records the actual Agent final commit `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1` and tree `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`. The protected product is `astrid/sdk/timeline/_command_state.py`, Git blob `09cbeeddefdc6375ba7d026406c95fb35bafda40`, SHA-256 `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`. The sole changed test is `tests/sdk/test_d100_item_birth_boundary.py`, SHA-256 `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`.

## Required order

1. Have one independent receipt-only checker consume this derivative and compare its final commit/tree, product/test identities, changed-path scope, and seven source hashes against `/home/user/work/agent` using Git. Do not rewrite the original author1914 or author1919 artifacts.
2. When ordinary free space is at least 5,000,000,000 bytes, run the bounded targeted Agent test against the exact corrected Agent source and pinned Runtime input:

   `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d100_item_birth_boundary.py`

3. Accept only a faithful result in which the two direct custody cases and the direct shared-owner case pass while all existing refusal/no-write assertions remain active. If it fails, report the first boundary; do not weaken equality or change product semantics.
4. After the corrected 27-node Agent result is GREEN, App owns the meaningful whole-path receiver proof and the exact `f53b` original-9 run. App remains the sole behavior receiver.

## Current disposition and holds

- This packet is evidence-only and makes no product acceptance claim.
- Source/static review and the prior independent purpose review are retained; no new protected body review is authorized.
- No pytest/provider/body/Runtime/App/live/full/security run was performed here.
- No source merge, release, pin, fixture, generated-file, credentials, permissions, hub, Git-ref, or LiveKit write is authorized by this handoff.
- D130 remains held.

## Contract/call-path reminder

The production comparator remains Runtime `commitTimeline` → registered Agent provider → `commands.execute` → `doc.patch` → `State`. The direct shared-owner test is a custody guard with admitted default source offset; it does not certify non-default trim support.
