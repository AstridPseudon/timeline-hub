# U4a-v2 corrected producer review — FAIL

Independent review of Agent `7d356202826ce60ff676d6e46151187aad9f4a70` against `fc515591b`, with corrected Runtime producer `780da6d605033ca71dbe2ad48c10ec2870ea4865` / tree `a2850bcaf0b37bd04613b02f071457b66f0987e3`.

The exact four-file adoption is correct: all 15 lock mappings, producer manifest, generator check, unchanged schema digest `35c2…`, artifact file `56a32978…`, producer `b0a15d84…`, and protected source blobs pass. The bounded Agent suite passes `46 passed, 39 deselected`; official Runtime commit-contract controls pass `8 passed, 30 deselected`; normal Ruff and private mypy ratchets remain `2151/2151` and `1915/1915`.

The complete official fixture probe passes accepted, merged, preview/accepted, and preview/merged envelopes with v2 request metadata intact. The required negative probe fails: the normal generated client accepts a merged envelope with only `receipt: {receipt_id: ...}`, and accepts a preview envelope missing `would_status`. The gap is the producer-owned generated guard at `generated.py:940-950` / `python_client_template.py:940-950`, which checks only outer envelope/status shape. Historical `21482` merged-status decoder defect is absent. This is FAIL until producer validation is corrected and regenerated; no Agent fallback or hand edit is appropriate.

See the detailed [worker report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U4a-v2-corrected-review-0258/report.md>).
