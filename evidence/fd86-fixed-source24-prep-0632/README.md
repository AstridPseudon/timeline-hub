# F-D86 fixed source24 receiving preparation

Private, source-only receiving packet for PLAN3F/G3/R1 and the strict C0
complete-command boundary.  It is based on the existing Runtime packet in
`evidence/fd86-new13-source-prep-0552` (the `tl/rt-D86-new13-main-0552`
route source).  No Agent merge, source lock, registry install, body, or
functional result is claimed here.

The D86 receiving set is exactly the 21 selectors in `inputs/selectors.txt`:
18 parent-media selectors, the two changed semantic-batch sheet selectors,
and one graph-roots selector.  Canonical membership is taken from the
published 19214 per-ID packet; all 18 parent-media rows are historical FAIL,
the sheet pair is historical FAIL/PASS, and the graph row is historical FAIL.
The 17724 NEW13 body has no overlap with this set.  These facts are retained
as prior dispositions only; no PASS from an unchanged case is promoted.

The separate D98a functional-original packet is exactly the three selectors
in `functional3/selectors.txt`, with source/static evidence from
`rt-D98a-functional-prep-0613`.  The old 32278 observer result remains
immutable context (three errors with observer active); it is not reopened,
reclassified, or used as behavior credit.

Every newly normal source prerequisite is receipt-bound: parent lane
`1a97728baafcef69ed3d081b03902ad3d5ac2032`, sheet lane
`b9484befcadb9427ebac65de938dfa10217edb4f`, graph lane
`8c88ea8f06b65f9b79fb7810af04720845c5cc6f`, and D98a capture
`a90bc7f9e1653e94384c094aaa87adf32239f5bc`.  Source commits, trees, blobs,
review identities, and SHA-256 values are in `inputs/source-hashes.tsv` and
`functional3/source-hashes.tsv`.

The existing D73 targeted route remains the only later body route.  Its
launcher/checkout/service artifacts and hashes are recorded under `route/`;
the next command is finite and is written there with the 21-selector file.
The later controller must capture one genuine normal adopted tuple once,
verify exact checkout/import/source/schema/profile receipts, then run the
existing route serially.  `actual550`, `23noXML`, passed13, old13errors,
currentheldID5, word2, D10022/ten, and D107 remain separate boundaries.

The remaining normal-adopter requirement is the D102c adoption receipt for
the consumer/source pair.  No future tuple is captured here, and ambient
`1daca` is not substituted into lock `689`; the later controller must persist
the actual adopted receipt before body submission.

No pytest, collection, import, fixture/provider, CLI, browser, registry, CAS,
or HTTP request was run.  The only checks in this packet are static parsing,
hash/set validation, in-memory AST compilation, shell syntax, and
`git diff --check`.
