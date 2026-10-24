Ask: permit one exact required created claim in the protected P3 command expectation / Owner: Orchestrator scope decision; Proof source and review / By: 2026-10-24T07:45Z

Independent read-only wholepath0705 raised this; exact assessment0728 confirms a concrete source incompatibility in the explicitly byte-protected reset/downstream tail. Current P39310 did NOT reach it. No code or test has been changed. Full worker final is design/handoff-ap2-P3-protected-tail-assessment-0728.md.

At exact App66354161950d1e747965c095ea97b881d2592708, three-products.spec.ts1640 strict requestB.commands equality expects a doc.patch command without created. Production documentPatchIntent.ts131,216-223 and localSaveSession.ts167-185 submit required created:[] for this no-allocation command. This is an exact expected-key omission, separate from the setup clip.move predicate fixed by the existing author. Existing all other original request/response/history/undo fields are source-consistent.

Concrete proposed ONE change, not applied:
```diff
   expect(requestB.commands).toEqual([{ schema_version: 1, op: 'doc.patch', version: '1', select: null,
-    args: { changes: mountedB.changes } }]);
+    args: { changes: mountedB.changes }, created: [] }]);
```

Decision needed because the current explicit instruction requires this reset and downstream tail to stay byte-identical. Permit only this required exact no-allocation claim, with independent no-weakening review, no arbitraryextras/union or predicate loss? Every original real0to5/POST200/reset200/lostACK/exactretrykey/restart/receipt/head/canonical/history/undo/owner/zeroLegacy assertion remains. No originalrun/newpin/bench/sourceguard/timeouts authorized by this question. Old tail SHA256f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67; worker's virtual corrected hash4b267cb513d863b46931cb793e995dbbe7169be2a56b46f15112655a945458ec is source-only, not an executed body hash. Manager will require actual worker hashes if permitted.
