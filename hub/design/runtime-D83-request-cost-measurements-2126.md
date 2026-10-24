# Bounded D83 request-cost result

Final product delta: NONE. The metadata parent 1fa23066f6f07ac6523cc8d39123ae02f1c2bfc4 remains byte-for-byte intact. The dependency independent review passed and normal integration receipt is bc04caa23f4b503fc55e49769ead20677904702a, tree fa696b342468ae191735409822fa3c7c66f8a590.

## One new genuine daemon control

Central service snapshot 2cf9cde0b6b4c14d9dafbec2ba25dbade96a3bc1 contains the metadata parent plus a temporary central entry point. The entry point launched the exact pytest command in its source, with -q -o addopts= -p no:cacheprovider --timeout=45 and absolute XML. Parent runtime source was used. Normal Astrid provider, generated WorkspaceClient, real HTTP browser door, empty public bootstrap, then track-only requests with one, two and three commands. This is disjoint from the other worker's native initialize/occurrence lock control. No lock instrumentation or lock-cause claim. Requests and generated credentials stay in the service's private throwaway realm. No raw request/auth/locals exported.

N counts previously accepted timeline.commit entries (excluding bootstrap). Counts include the newly accepted request's own final verification. Request ordinal is 1-based; command ordinal is 0-based.

| Request | N before | Commands | _verify_accepted | _historical_sequential | validate_sequential_capture | _capture_records | _capture_document_images | auth.validate | schema validation total | profiled wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 2 | .284362 |
| 2 | 1 | 2 | 11 | 1 | 2 | 4 | 16 | 14 | 24 | .304641 |
| 3 | 2 | 3 | 21 | 16 | 17 | 34 | 144 | 39 | 212 | 1.849418 |

Request 2 verifies its one-command ancestor 10 times and its new two-command acceptance once. Request 3 verifies its two-command ancestor 15 times, its one-command ancestor five times and its new three-command acceptance once. Its 16 historical sequential verifications are 15 ancestor revalidations plus one post-acceptance verification. One additional fresh acceptance capture makes 17 sequential validations.

For request 3, original/landing capture-document calls by ordinal are respectively [34,34,4] / [34,34,4]. Each ordinal contributes input/output (two calls per side) for every sequential validation containing it. Request 2 has [4,4] / [4,4]. Physical-owner/materialization alias cases can add more calls; this parent-only control does not model those cases. N and command count covary in this small control, so it does not identify an independent scaling law for either dimension.

Request 3 top overlapping cumulative costs: schema validation 1.437335s, history_entry 1.414690s, _verify_accepted 1.413907s, _historical_sequential 1.386656s, port _ancestor .850910s, validate_sequential_capture .849508s, _capture_records .697029s. First-request cold imports dominate part of its cost. Timings include cProfile and counting wrappers, and cannot predict unprofiled original wall times. Counts and call structure are the useful causal evidence.

## Source interpretation

Runtime port _ancestor (timeline_commit_port.py:224) independently walks observed/base roots through store.history_entry; port.history also authenticates its through edge, and store.history/_history_page authenticate bounds and returned ancestors. history_entry (store:442) calls _verify_accepted (store:202). The verification is an accepted-edge operation, not a direct once-per-current-command loop. _verify_accepted invokes _historical_sequential once for each retained execution (store:321). That authenticates CommitContext/PreparedCommit and the sequential capture. validate_sequential_capture (auth:2468) validates both original/landing Recorders, then each command input/output with _capture_document_images. Thus repeated ancestor retrieval repeats the complete retained ordinal traversal. Additional binding-image/owner callers also validate the entire document afresh. This explains multiplicity without assuming a sampled leaf is the cause or eliminating any check.

## Authentic existing evidence

All 54 authentic14690 per-handler profiles were read in place; hashes and safe count/cost extracts are retained. Aggregate _verify_accepted=64, _historical_sequential=36, validate_sequential_capture=37, schema validations=1609. Handler 54 alone has _verify_accepted=48 (32.554171s cumulative), _historical_sequential=31 (28.894387s), validate_sequential_capture=31 (20.926662s), _capture_records=62 (10.700567s), _capture_document_images=1220 (5.655752s), schema validations=1345 (23.726052s), auth.validate=60. These overlap; do not add them. These profiles predate the already merged preparation corrections and have uncalibrated observer overhead.

Current1960 remains unprofiled: three failures, four passes; the ten-note and False2 cases time out at 45s, True2 candidate-only cases finish around 42s. There is no current per-handler attribution in that run. Actual22971 ordinal3's historical Recorder validation at 50590ms and its ~4.6s UI pending window is consistent with expensive fresh history validation but does not establish terminal cause, permanent deadlock, accept/receipt/response, or a common lock cause. PopupADD26387's no-response window is likewise not an established common cause. No new collector or original/browser rerun was requested or performed.

## Rejected correction

Tried removing generic keyword-dictionary dispatch from the existing immutable schema-validator setup hit path. No new cache and no fresh check removed. Exact rejected blob 989b6522f161c251a2b08a0e2eb9f95b290fbc74 and reconstructable patch retained. An initial retained-capture helper comparison showed 6.70% lower median CPU (.338900 -> .316188 per three verifications), 40 predicate/count frames equal. More relevant accepted-history replay comparison showed .433276 -> .434615 CPU per three calls: 0.31% worse, 44 count frames equal. Eight alternating paired rounds, warmed validators, profiling counts collected separately from timings. Samples vary substantially; no strict accepted-history gain is demonstrated. Restored source/test files exactly. Independent source security review passed the candidate's forwarding/cache-identity semantics; source safety does not establish performance merit.

## Limitation and needed decision

There is no demonstrated additional product gain in this assignment. Metadata's prior finite 8.34% gain, the rejected probe, and sampled timeout leaves do not prove original 45s/30s/120s/UI5s budgets. D47 forbids the obvious reuse of accepted-edge/history/request verification results; preserving fresh predicates leaves the observed ancestor-by-complete-capture work. This evidence does not prove every allowed immutable-preparation optimization is exhausted. It does show that this specific safe correction fails the gain requirement, and there is no measured basis to promise the budgets from it. Orchestrator must decide the next bounded preparation investigation or explicitly reconsider the relevant constraint/design; no unilateral memoization or budget/contract changes are justified. Existing submitters own any next original gate after the normal review/release path.
