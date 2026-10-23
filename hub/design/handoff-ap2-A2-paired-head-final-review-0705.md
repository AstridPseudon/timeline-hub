# A2/P1 paired-head independent final review — 2026-10-23

PASS on return `05f39fcd8d7df5492744a9461b8f842002518124` / tree `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`, reviewed against base `9dd59025d6aba6b37112c498b479e3f36c7b4bbb` and failed candidate `76a4bc64773ed9bbfeec393e4b0888594029f7d0`.

The return correctly makes cached immutable-basis/version reuse require the same verified revision/publication pair. The real adapter regression proves `(R,P1) -> (R,P2)` on normal load then poll, equal bytes, P2 returned, version 2, and two immutable reads. Cached `null` remains the settled unverified legacy compatibility case. Public GET/strict identity, exact inspection pairing, bounded retry/refusal, legacy null, captured old-pair CAS, and the full v2 candidate behavior remain intact; no shortcut waiver or guessed latest pair was introduced.

Evidence: targeted Vitest 153/153; focused regression PASS; app `tsc --noEmit` PASS; scoped ESLint PASS; diff checks PASS; exact private graph PASS (80 files, Composition `0.0.14`, archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`); three-file allowlist and source bindings PASS. `runtime.lock.json` remains bound to normal Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`; Agent/Runtime pin commits and trees are clean. Requested-base original P1 spec is unchanged with SHA `cae24b8e5481557f4812e47f06828aed3cf2176c6da92b4ca265095dbefd8175`.

Limits: no browser, HTTP/body, live service, socket, build, or full suite; no product/test edits. Manager can run the existing P1 service row, then the original two cases. Full exact commands, hashes, blobs, and limits are in the worker report.
