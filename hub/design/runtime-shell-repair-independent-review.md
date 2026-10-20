# Runtime shell repair independent review

**REJECT — one reproducible hidden-content/corruption refusal gap.** Reviewed final commit `0e49e0228f5977b5a8b2b17b7f017a91b40eaf2d`, tree `d97b20693d801f6b7889867620f2b51856521147`, after source-worker DONE. This is the exact tree qualified centrally. No moving WIP was approved.

Same-ID repair accepts a retained same-project `timeline:main` document containing `{"clips":[{"id":"keep"}],"clips":[]}`. The existing `timeline_scope_is_empty` calls ordinary `json.loads`, which drops the first authored clips value; the new absent/null-head branch then treats the document as empty and bootstraps it. A final-source private probe expected refusal and failed. A diagnostic confirmed **one new parent revision, one history edge and one repair receipt**, while the original corrupt document bytes remained stored. This violates the requested hidden-authored-byte and corruption-fail-closed boundary; it is not a claim that the raw document was deleted.

The permissive parser predates this patch, but this change newly admits no-parent resources through it. Relevant source: [emptiness parser, line 60](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-shell-repair-independent-review/notes/final-source/runtime_protocol/timeline_commit_store.py:60), [new repair gate, line 927](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-shell-repair-independent-review/notes/final-source/runtime_protocol/timeline_commit_store.py:927). Reuse existing strict JSON rejection behavior (the baseline verifier already refuses duplicate keys), refuse before bootstrap, and extend an existing hidden-document case with the raw corrupt input. No normalization, new writer or architectural change is needed. The owner-authorized repair decision is sound and is not being reopened.

Other reviewed boundaries pass: existing bootstrap/writer reuse; same lock/transaction; absence/null versus verified unpublished revision versus published/tracked state; wrong project/archive/retained content refusal; exact original-create and repair-key retry after init/edit/undo/restart; changed payload refusal; strict initial empty admission; and unrelated catalog rows remaining outside timeline content. No new API/table/DTO, authored-default application, compatibility writer or mutex framework was added.

Evidence:

- Independent final-source neighbors: **105 passed**.
- Independent private adversarial probes: **4 passed / 1 failed** (duplicate-key case above). Unrelated catalog shot/document/media rows stayed unchanged and outside the canonical closure; hidden false/zero/empty-string values refused with unchanged DB/CAS and zero SQLite changes.
- Inspected source-worker evidence: **157 passed / 1 deselected** bounded neighbors; **94 passed / 1 deselected** private init/schema tests; central **32 passed**, including all nine commit cases and the unchanged missing-positive with `--runxfail`. The prior qualification's **14 passed / 1 strict missing positive** is therefore closed for the intended normal repair/init flow. The strict test was not rewritten.
- Independently verified final product bytes equal the central private archive; original init test is byte-equal to the prior archive; private schema is exactly full S2 (48 definitions/22 operations) plus approved init (49/23).

Next: repair the corruption refusal in the existing path, preserve the original positive, rerun the bounded failure and affected gates, then request review of the new final commit. No full/broad suite, App adoption, public pin or release is approved by this report.

[Detailed report, exact commands and evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-shell-repair-independent-review/DetailedReport.md).
