# Runtime R2r native-store independent review — PASS

Candidate `a511bd493bbb018c9aa634aea00f06e376f950c2`, parent/base
`1365e4b17b31c4a7093d5943674637067fd2bab4`. **PASS; no blocking product
finding.** The candidate diff is limited to auth, store, and the new inverse
stage test. Worktree clean; no source repair was made.

Exact bounded acceptance:

- inverse/auth/read-basis: **126 passed in 40.02s**;
- inverse/history integration: **10 passed, 68 deselected in 9.69s**;
- D17 preservation lane: **101 passed in 13.20s**.

The new inverse-stage file collects **41 tests**. The corrected REALSTORE
split+note witness passed on the actual candidate: forward acceptance/auth and
inverse acceptance/auth are both `pass`; source history is the exact accepted
forward `history_entry`, source publication is
`txn-ddb90be35ad5469cb51ae943df508e7c`, inverse publication is excluded, and
source step/ordinal/created-ref provenance is recorded. Missing, forged-step,
and future/inverse history refuse. The inverse stage covers native range
`[0,8]` and effect range `[0,3]`; parent clip mirrors, config/root writes,
sequential values, full restoration, readback, exact retry, mirror forgeries,
and no-durable-write/no-history-change controls pass.

The same witness against extracted `21b329935785e4040775ed34b4a01ebf31ec6683`
reproduced the causal RED: `invalid_records: inverse stage write differs from
its sequential input`. Original 0912 remains byte-identical at SHA-256
`47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a`.

Scoped auth/new-test Ruff is clean. Auth/store Ruff has **11 inherited
diagnostics**, identical to parent. Auth/store Pyright has **76 inherited
diagnostics** on both trees; normalized and source-line-mapped identity
comparison reports **0 added / 0 removed**. AST/compile and `git diff --check`
pass. First 367 test lines match held baseline byte-for-byte; expected changed
file set is exactly the two source modules plus the new test.

Both `parent/clip` and `parent/asset` alias normalization paths were checked
against the authenticated physical parent paths, with config/root and absent
item handling. A standalone real-Agent parent/asset inverse journey was not
part of the bounded runs, so no broad Agent qualification is claimed.

Evidence JSON: `/tmp/w-41c28dfd8b/realstore-witness.json`.

Caveat: the supplied witness JSON retains a stale hard-coded
`runtime_commit=21b329935`; its runtime checkout and auth/store origins/hashes
are the actual candidate, and the actual tree SHA is `a511bd493`. This is an
evidence metadata defect only; it should be corrected on the next witness
refresh. No full/Agent-58/native14/crash24/original20/browser/HTTP journey or
daemon was run. Integration merge and central D17 recheck remain manager-owned.
