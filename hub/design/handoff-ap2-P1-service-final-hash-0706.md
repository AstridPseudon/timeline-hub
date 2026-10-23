# Handoff: ap2-P1-service-final-hash-0706

Status: **operational qualification complete; product remains pending independent0705**

Changed only the existing `ap2-P1-chain-h6` row in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`

Exact one-field correction:

- old `src/integrations/runtime/dataProvider.ts` expected SHA: `3527e7d9f39e72e573a3eb753c7d542d1fb4ed1d5ed3856aa6aec46353471c13`
- new actual SHA from App HEAD `05f39fcd8d7df5492744a9461b8f842002518124`: `46fbdca6ecc32292273e87b9f62abf5e8c35a3b39904f1fa8b1165ae69a9894f`

Proof:

- row contains new hash exactly once and old hash zero times.
- `bash -n` of the complete `ap2-P1-chain-h6` command: PASS.
- Atomic replacement path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`, byte offset `20176`, `64` bytes.
- exact outside-byte comparison: `True`.
- current file SHA256: `0e10a9bf8c3a75c42cdc59b73005a10043bd2b9200aa89cd4c5a07a39f527523`.
- reconstructed preimage SHA256: `7bbe71551488f2fd8eec0e7a84a49e453fd1e1bab1219ff32dc06a1f33f474f8`.
- App worktree status remains clean.

No tests, service body, HTTP/socket/browser/build/full-suite run or central request was made. No product/test/schema/generated/pin/fixture/launcher/other-row edits were made. Production caller and full-v2 request/reply are unchanged. Independent Luna row review remains required before the original service body; no product PASS is claimed.

