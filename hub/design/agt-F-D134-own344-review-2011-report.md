## F/D134 review — FAIL

- Independently validated the raw 18455 log: 370 unique bad IDs; 190 failed, 180 errors; hash matched `65def166…ae8e`.
- Confirmed author’s 344 IDs are an exact subset of the retained 370; all source blobs and tuple commit/tree hashes match; all 58 files are absent at named upstream.
- Downgraded exactly nine D100-dependent projection cases to `UNKNOWN`.

Final equation:

`132 TEST_SETUP_OR_EXPECTATION_PROVED + 0 PRODUCT_FAULT_PROVED + 212 UNKNOWN = 344`

Author packet remains unchanged. REG14 remains `UNVERIFIED_CURRENT_REG` (14), prior UNKNOWN 12, retirement 0.

Evidence:

- [review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-own344-review-2011/evidence/review.json)
- [findings.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-own344-review-2011/evidence/findings.md)
- [classification-bounds.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-own344-review-2011/evidence/classification-bounds.json)

Validation passed: JSON parsing, finite-count checks, raw membership comparison, source/tree checks. No tests, reruns, collection, or product changes performed. Raw XML and accepted-record/caller traces remain unavailable, so product-fault and custody claims stay unproven.

Commit message written and `DONE` marker created.