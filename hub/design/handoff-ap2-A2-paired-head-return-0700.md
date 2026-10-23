# A2/P1 paired-head return — 2026-10-23

The bounded review finding is corrected. `readTimelineInOrder` now refreshes the immutable parent basis and increments the local version when a verified cached pair changes publication identity at the same revision. A cached `null` publication remains unverified and does not create a false mismatch against the established whole-document save/readback path. Public identity validation, inspected/public revision pairing, bounded retry/refusal, true legacy-null preservation, captured old-pair CAS, and outbox acknowledgement behavior remain intact.

The new regression uses the real `RuntimeDataProvider` and Runtime fixture: normal load observes `(parent-r1, publication-p1)`, poll observes `(parent-r1, publication-p2)` with equal bytes, and the provider performs two immutable reads, returns P2, and reports version 2. The old candidate was run as a negative control and failed with version 1/one immutable read.

Evidence: exact four-file targeted Vitest passes 153/153; TypeScript, scoped ESLint, `git diff --check`, exact private 819acf graph/archive checks, and the three-file outside-blob allowlist pass. No browser, HTTP/body, service, build, socket, or full-suite run was performed.

Changed in this return: `src/integrations/runtime/dataProvider.ts` and `src/integrations/runtime/dataProvider.test.ts` only. Candidate parity changes remain present but untouched.
