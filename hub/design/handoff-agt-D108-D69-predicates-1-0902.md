# F-D108/D69 original predicate preservation map — partition 1

Status: **SOURCE_ONLY_EXACT_PARTITION_MAPPED**.

Odd-index partition of the recovered Agent `affected_function_records`, sorted by `(record["path"], record["function"])`: **64/129 functions**, **67 removed** and **178 added** assertion multiplicity units across **34 functions with deltas**. The sibling partition is disjoint and is not included.

Authoritative source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-original-membership-next/evidence/original-membership.json`; SHA-256 `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`. Agent refs: upstream `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, captured `d6294843286c18e57af3c1874cf1996be42212d2`. JSON/TSV retain every assigned function key/path, old/new blob and lines/body hashes, assertion fingerprint, and multiplicity.

| Decision | Removed unique / multiplicity | Added unique / multiplicity |
|---|---:|---:|
| preservation | 0 / 0 | 0 / 0 |
| approvedreplacement | 1 / 1 | 1 / 1 |
| approvedretirement | 0 / 0 | 0 / 0 |
| UNCLEARED | 66 / 66 | 177 / 177 |

Exact prior receipts used: D72 `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-D72-frame-review-1722.md` plus `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-rt-D72-frame-window-1717-qualified-final.xml` (exact null-window predicate replacement). The D69 voice terminal receipt was not applied because its predicate is unchanged between the authoritative 08e6 upstream and d629 capture, so it is outside this removed/added delta map. No `approvedretirement` was issued. All rows other than the exact D72 pair are explicitly `UNCLEARED`, including related old-writer/v2 changes where a report was source-classification only or named a different selector/body.

## Limits

No blanket clearance was inferred from operator counts, lexical similarity, body hashes, or passing tests. Current `d0ecf1d69a7b37f86034bc52004f73f6c6231603` exact Git blob reads match captured new blobs for every assigned function file; separate later D69 suffixed functions are not paired with these original functions. D07/b943, Windows/d0ec, D107/2e3331ee, and D18 retain existing owners. Remaining gaps are per-predicate semantic equivalence, explicit retirement authority for old legacy-writer assertions, and behavior qualification after source decisions.

Full row-level source and approval receipts are in the JSON and TSV. Product tests/typecheck/lint are N/A for this read-only source task.
