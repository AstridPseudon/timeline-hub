# F-D86 superseding exact22 safe metadata

This packet supersedes only the 'exact22/' subpacket of the first export at
'../exact22'. The first export is preserved unchanged and remains immutable;
'../actual20/' is also unchanged. This packet is a separate corrected return,
not a silent overwrite.

The producer artifacts are durably present in Runtime commit
'350058edc5b830215c7d915e09024e2362a0b429' on
'tl/rt-D86-ready22-body-0333'. The venue was the producer worker's direct
existing D73 launcher. The actual run ID is
'fd86-exact22-body-20261025-034159'; no centrally numbered request record was
found, so no central service ID is claimed.

The A20 packet remains the existing service
'd91-first20-immutable20-0313-1025031717-18575' (service 18575), with its
real per-ID records, safe first-exception fields, helper identity, and source
identities unchanged. The current Agent peer 033346 remains requested; this
packet does not claim that request as fulfilled.

The producer XML contains exactly 22 selected testcases: 4 PASS, 18 ERROR,
0 FAIL, and 0 SKIP. Every per-ID status in this packet is taken from an
authentic XML testcase record. The four PASS rows are not inferred from
missing records or from the ERROR complement. The aggregate 4/18 result is
retained from the producer summary. Error rows retain only safe class,
message, and source-location metadata; private XML, body log, command text,
credentials, keys, URLs, and stacks are not exported.

Execution limits retained from the producer record: 22 unique selectors,
worker parallelism 3, cache disabled, 45-second timeout, and no marker filter.
Preflight exited 0 and the body exited 1. This is a source-only metadata
correction; it adds no functional closure or behavior credit.

All 22 prior captured identity fields (ordinal, canonical node, family,
source file, source commit, and source hash) are preserved byte-for-byte in
the corrected membership and outcome projections. Producer artifact and
input hashes are listed without exporting their contents.

Exact flat file list:

- 'README.md'
- 'accounting.json'
- 'artifact-sha256.tsv'
- 'exact-membership.tsv'
- 'family-owners.tsv'
- 'firstexception-clusters.tsv'
- 'per-id-outcomes.json'
- 'per-id-outcomes.tsv'
- 'run-identity.json'
- 'source-dependency-delta.tsv'
- 'source-hashes.tsv'
