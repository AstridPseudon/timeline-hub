# Runtime strict shell repair final review

**APPROVE** final harness commit `ff9d5c17bc75fb12b3293690a8d9acd8eded0db2`, tree `6c380bb36bb7e398613c238bb1a442502de67c78`, against rejected `0e49e0228f5977b5a8b2b17b7f017a91b40eaf2d`. No blocking findings remain. Approval applies to this immutable tree and the bounded shell repair only.

The hidden-content finding is closed. `timeline_scope_is_empty` now calls the existing baseline `_json` parser, rejecting decoded duplicate keys at every nesting level, escaped equivalents, and duplicate-empty values. Malformed/non-finite JSON also refuses. This happens before bootstrap, revision persistence, history installation or repair receipt recording; original bytes remain stored unchanged. There is no new parser, normalization, writer, endpoint or authored-default application.

Independent final-tree evidence:

- **5 passed**: the original reviewer file ran unchanged, including the previously failing `{"clips":[{"id":"keep"}],"clips":[]}` negative. It asserts identical SQLite/CAS state and zero SQLite changes.
- **27 passed**: additional probes across absent, null and verified unpublished heads. Corrupt inputs refuse twice with guarded bootstrap/persistence/history/receipt methods never called. Distinct opaque keys, including distinct Unicode spellings, and canonical empty legacy documents succeed without rewriting document bytes or CAS, preserve the existing unpublished revision identity, and replay exactly.
- Source review confirms the entire repair still uses existing create admission, lock/transaction and bootstrap; retained parents/publications, foreign/archive/name mismatches, F2 content/dependencies and nonempty snapshots refuse. F1 destination guards remain unchanged. Exact original-create and repair receipts replay before resource-state checks; bootstrap applies only the canonical empty document, and init remains explicit.

Inspected worker evidence: **117 passed / 4 deselected** bounded local tests, **5 passed** unchanged reviewer probes, and central request `rt-m2-shell-strict-json-fix-targeted-1020123728-6927`: outer **1 passed**, native child **32 passed**, no xfails. The central snapshot tree equals the final harness tree. Independent collection confirms that the child includes **all nine commit integration cases**, the original missing-head positive under `--runxfail`, real generated-client Door/restart, absent/null repair and init/edit/inverse/restart durability, and actual-provider F1 restore coverage. The required nine cases are present; the outer one-test count is not substituted for them.

Verified 404 non-overlay tracked files in the retained native candidate equal the final tree. Its 18 approved private artifact/schema overlay files and original init test equal the prior archive; full S2 48 definitions/22 operations is preserved with only approved init added (49/23). Original native positive assertions were not weakened. No full or broad suite was run or requested, and no service/socket test was run directly by this reviewer.

No product edits, pins, merge or publication occurred. App adoption and full repository/release qualification remain outside this approval. The orchestrator can accept this exact repair tree and qualify downstream adoption separately.

[Detailed report with exact commands, source checks and logs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-shell-strict-final-review/DetailedReport.md).
