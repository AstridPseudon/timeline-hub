# F-D108 independent first-return rereview

Verdict: **PASS for the finite fallback corrections; full D69 qualification remains NOT QUALIFIED.** The successor `handoff-agt-D108-assertion-return-0758` corrects all four independent 0754 failures and makes no readiness or acceptance claim.

| correction | verdict | independent result |
|---|---|---|
| Actual captured-vs-normal scope | PASS | `d6294843..b943270a` changes six paths; the two D110 paths are `astrid/sdk/timeline/inverse.py` and `tests/sdk/test_inverse_removed_shot_owners_runtime.py`, and their blobs match `ccf831df`. |
| Fallback direction and arithmetic | PASS | `d6294843` old → `08e6b905` current over 146 common modified Python test paths: 4,214 common functions, 189 changed bodies, 310 removed fingerprints, 119 added fingerprints, 646 exact-preserved old rows; residue is `60 / 197 / -168`. |
| Crosswalk hashes | PASS | JSON `e131b68c…1515`; Markdown `135f2e0b…1d5b`; expected `37e559e6…a4504` is separately identified as the SHA-256 of the absent rehearsal manifest, not either crosswalk. |
| Exact finite rows and groups | PASS | 189 body rows, 956 old predicate rows, 310 removed rows, and 119 added rows have exact source line/blob/AST metadata; row IDs have no duplicates. All eight groups are exact disjoint unions with no cross-group overlap. |

The row semantics are exact same path + qualified function + predicate kind/fingerprint multiset. `ast.Assert` and `ast.Raise` (including bare `raise`) are represented; parameters, markers, and `pytest.raises` coverage-limit metadata match the source. Removed rows remain `UNCLEARED`; no removal has approval. The 310 deletions are not treated as upstream predicates removed by our captured change: they are the `d629` → `08e6` fallback’s captured-old-to-current-upstream direction.

The preservation inquiry separately names `08e6b905` as old and `d6294843` / `c456b328` as separate new objects. It contains comparison totals only, not per-predicate upstream-old/source/approval mappings; therefore it is preservation context, not clearance. The authoritative `129 / 113 / 287` membership remains `EXACTMISSING` because the named rehearsal manifest is absent. This is a genuine input limit, not a failure of the finite fallback and not permission to clear omitted rows.

No false readiness/acceptance claim is present: result is `NOTPROMOTED`, authoritative membership is `EXACTMISSING`, and product changes are `none`. The production caller and v2 request/reply boundary remain unchanged.

## Evidence

- JSON parse, exact Git source reads, stdlib AST/multiset recomputation, row metadata checks, in-memory compilation, group arithmetic, six-path/D110 scope, crosswalk hashes, and `git diff --check` passed.
- No product tests, imports, collection, helpers, probes, browsers, services, installs, or body execution were run; they are not applicable to this read-only source review.

Minimal next scope for full D69 qualification: obtain the genuine applied rehearsal manifest/audit and authoritative selector/fingerprint membership, then map those authoritative rows to exact current source lines/blobs and approvals. Until then retain `NOTPROMOTED`.
