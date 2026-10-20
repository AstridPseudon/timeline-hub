# Native independent duplicate: exact App identity contract

M2 only, candidate strict-xfail remains. Review design/app-duplicate-identity-review.md source/135passingtests/twoactualpureprobes. No product changes.

Reserve occurrence_id/shot_id once; rederive ONLY root stable_deep_link and output_identity using existing shared App/Agent factories. output_identity is an occurrence lookup key, NOT an immutable task/output/object identity. Preserve historical output/task/association records, namespaced/nested data and unknown fields byte-for-byte.

Exact current factories: stable_output_identity(P,T,O)=project/{P}/document/{T}/occurrence/{O}/output/final-video; stable_occurrence_deep_link(P,T,S,R,O) includes actual compiled DESTINATION shot revision R. encodeURIComponent-compatible helpers already exist Agent shot_composition.py353-373. App must not duplicate compiler hashing or supply source revision/random oldgraph revision.

Recommendation to Agent: declare exactly these two root paths as derived duplicate identity fields, reuse normal factories against actual deterministic compiled destination, preserve native args/reservation boundary where possible. No broad suffixremapper or arbitrary replacement strings. Current candidate carries source strings through compiler and should stay strict-xfail until fixed in BOTH raw row and immutable compiled closure.

Important readback trap: App dataProvider recomputes both strings on read; reload UI can hide a wrong stored raw occurrence. Acceptance test must inspect exact raw immutable parent +closure, then actual browser routing/new managed-output association isolation/reload/undo/retry/0legacy.

App old duplicate writer remains until matched official Runtime schema/client and actual qualification. Linked duplicate has no UIcaller, existingpositive test preserved. Agent owns exact contract/change; no App wirefields invented.
