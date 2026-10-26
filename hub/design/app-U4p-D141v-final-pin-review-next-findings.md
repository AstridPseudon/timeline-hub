# U4p D141v independent findings

## PASS

The candidate is a genuine metadata-only adoption. The requested full commit/tree and base match Git; qualified Agent and Runtime producer homes are clean and exact; the two changed paths are the expected manifest and Astrid provenance metadata files.

Independent checks found 160/160 vendor payload names and bytes conserved, 14/14 Runtime lock mappings byte-identical to base and hash-valid against the pinned Runtime checkout, no outside-allowlist changes, exact manifest/provenance pins, valid JSON, clean whitespace, and idempotent manifest plans. Required Node 20.19.4 tests and verifier passed.

## Custody finding (not waived)

The author’s first-tool `disk-trace.txt` is bounded to five samples at 14:26:06Z–14:26:10Z. Its `continuous_stop_respected` flag does not establish continuous whole-worker coverage. The original evidence is preserved and no continuous-history or body credit is assigned.

This review’s persistent sampler ran across tool calls from 14:31:58Z–14:32:50Z (52 samples), remained above the 4 GB stop, and was explicitly stopped, waited on, and reaped. Its trace began after an initial harness-pointer/background-launch failure; that bound is reported rather than backfilled.
