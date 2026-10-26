# D141l findings

Verdict: source review PASS; actual test results FAIL; custody PASS; bounded no-regression only for the current full failure-ID set.

1. Current full 8638 is FAIL (19745 pass, 32 fail, 4 files, separate collection error); chained Node NOTRUN.
2. Pristine full 17524 is FAIL (17866 pass, 18 fail, 3 files); chained Node NOTRUN. All 18 pristine IDs are preserved.
3. Five current IDs are in files absent from d822; 27 are in frozen useTimelineSave but exact titles/parameterized predicates are absent. No renamed equivalent was found. All 32 are N/A/OWN, not UNKNOWN and never pristine PASS. This is bounded no-regression, not global REG0/GO.
4. genericPatch is a separate module-level schema-digest collection failure; absent upstream; not a test ID.
5. The two Node failures match exact files, blobs, callsites and ssh-keygen ENOENT in the same normal-service environment kind. They are NONREG_PROVED; this does not qualify unrelated full Vitest differences.
6. Raw hashes, source/tree/parent bindings, receipt validators and traces qualify custody. Five-second gaps and bracket-only semantics remain disclosed; pristine Node DATA is derived, not original stdout.
7. Prior 0705 reported one absent worker KEEP; final read finds it present and D74 records 161/161 decoded, 111/111 gzip, 38/38 KEEP. Retain only as historical metadata.
8. D141w 493/tree6a6e49 is the reviewed exact 21-path upstream delta over 4de; current 82e matches the tree. 255 targeted tests and both TS configs passed; three pre-existing AgentSetupCard lint errors remain.

Author 0710 claims qualifying: genuine pristine full/Node outcomes, exact custody, Node nonREG, separate collection error, no global REG0, C0 field preservation. Corrected: all 32 OWN/UNKNOWN become exact N/A/OWN; script sizes are not package sizes; full qualification is direct. Remaining UNKNOWN: none for the finite reviewed IDs.
