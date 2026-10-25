# D127c findings

## D127c-F001 — resolved in source; independently revalidated

The final App source contains an explicit `REVIEWED_PROFILER_HELPER_SHA256` branch for the exact Runtime helper digest `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`. That branch requires the canonical basename `p2_commit_phase_capture.py`. The normal, reviewed, and reviewed-new arms remain strict; the fallback still asserts the reviewed-new digest, so arbitrary hashes are refused.

`readCapture()` uses the same four-hash allowlist and maps the final digest to `reviewed-profiler`. `p2CommitPhaseCaptureConfig()` obtains the hash from the selected source bytes, or checks supplied path+SHA environment values against the bytes. The mounted live assertion calls the same `assertSourcePinnedHelper()` function used by the positive/negative sourceguard test.

The actual final Runtime helper bytes were independently read from Git commit `368f53f4454d5908c86de53d174f0bedcf23781c`; SHA-256 is the exact `095c…` value above. No Runtime checkout was changed.

## D127c-F002 — blocker — required Node20 proof did not execute intended nodes

The required supported Node20.19.4 command completed with only the file-wrapper event (`tests 1`, no named child tests). A custom event reporter confirmed no `D127c source guard` or `D127c reviewed-profiler validator` node was enqueued. Per the task rule, zero-selected is NOTPASS. This is an execution-environment limitation, not a discovered source-logic mismatch.

Node22 with `--experimental-test-isolation=none` executed and passed the intended sourceguard, reviewed-profiler, and reviewed-new nodes individually. Node22 is supplemental and cannot replace the required Node20 evidence.

No live bootstrap, socket, browser, original-element, native, full, tour, acquisition, or product body ran.
