# F/D134 partition findings

The exact finite partition is:

`TEST_SETUP_OR_EXPECTATION_PROVED (141) + PRODUCT_FAULT_PROVED (0) + UNKNOWN (203) = 344`.

`per-id.tsv` is the complete membership record. It preserves the actual status, failure type, first safe failure file/line, current source blob, test-file provenance, cluster, causal category, and safe source evidence for every retained nodeid.

The 141 proved setup/expectation records are bounded to concrete source seams: 102 managed-edge fixture writes rejected by the Agent managed-closure guard; 11 stale source/hash or runtime-pin expectations; 2 fixture calls missing required arguments; 9 projection fixtures with no item; 4 detached-fixture preflight failures; 1 fixture with no client; 1 retired save-route expectation; 3 `rebased` versus current v2 `merged` label expectations; 7 invalid one-sided clip-mirror fixtures rejected by the mirror guard; and 1 legacy archive shape expectation.

No product fault is proved. The remaining 203 records include provider/inverse mismatches, missing or ambiguous identity/anchor state, selected-parameter authority unavailable, native/graph/timing/input failures, and other first-boundary failures where private accepted records or a legitimate caller trace are unavailable. A guard refusing an invalid fixture is setup, not a product fault; a test-file absence upstream is provenance, not causality.

All 344 selected IDs are in 58 current test files, and all 58 files are absent at named upstream `08e6b905...`. This is recorded separately and does not imply 344 test bugs. Active owner scope is limited to D100 for source/setup custody, producer/inverse for managed-edge and commit/inverse seams, and wordsource for mirror/word-shape seams; unresolved records are routed by source file without dispatching authors.

The 14 prior REG records are preserved separately as unverified current REG after the independently observed prelaunch `PYTHONNOUSITE` rejection; the 12 prior UNKNOWN records remain UNKNOWN. Retirement remains 0.
