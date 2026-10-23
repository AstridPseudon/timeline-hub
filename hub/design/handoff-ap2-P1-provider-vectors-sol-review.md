# AP2 P1 provider-vector correction independent review

Result: **PASS for packet correctness; NOT MERGEABLE.** Candidate:
`d8e1578bd9f717eb975addb50c2654de70815475`.

The corrected packet is limited to its request corpus and provider/request
tests. It authors all five trim effects with exact guards, uses legal
`internal-revision:ir` plus `clips/id:c/...` paths for the four child vectors,
constructs a complete verified closure with one shared physical `sr`/`ir`
child, preserves raw fixture values/ownership, and asserts exact absent/null/
remove/disjoint results, opaque siblings, and JSON reload. All original source
fixture hashes match; no canonical source fixture changed. Original
same-field `value_conflict` and membership/order `selection_changed`
expectations remain, with no skip/xfail or substitute behavior.

Required evidence: **1 failed, 41 passed, exit 1**. The sole failure is the
known stale membership-removal case, where current R1 returns
`value_conflict` instead of required `selection_changed`. Agent R1 must check
collection membership/order dependencies before the item-value guard, while
keeping same-field stale edits as `value_conflict`. Until then this packet is
NOT MERGEABLE. Review PASS does not grant merge or H3 GO.

The disjoint service observation is a new local acceptance after a competing
`y` commit, not a historical-key replay. It reports legacy `rebased` because
the detached/old Runtime fixture has not adopted required v2 `merged`; this is
an explicitly weakened status assertion and proves neither new v2 merged
acceptance nor Runtime HTTP/App H3. H3 remains unverified/NO-GO.

Evidence commands and complete logs are in the harness report at
`workers/ap2-P1-provider-vectors-sol-review/report.md`.
