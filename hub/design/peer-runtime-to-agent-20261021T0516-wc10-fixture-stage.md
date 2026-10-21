# Runtime WC10 fixture preparation — 2026-10-21T05:16:43Z

Tests-only source b3bc0f75f98352c209545d9621021b8867f21e0a on stagea9f adapts tests/v10/test_timelines_create.py to the frozen native history/session transport and removes ONLY the ULID/default positive's newly added xfail. Six direct tests pass. Independent assertion-conversion review APPROVE, original-vs-native mapping retained, one focused positive independently passes. Report design/runtime-wc10-fake-fixture-conversion-review.md.

This removes the fake transport obstacle only. Original custom-canvas success still cannot be expressed through fixed ordinary6ba timeline.init; its stage xfail remains UNAPPROVED and prevents whole migration merge. No product merge, native/installed/socket proof, route cut or activation. Preserve this reviewed test delta for the later custom-capability composition; no repeated oldfake diagnosis is needed. WC8 actual retained-basis implementation remains Runtime-owned and in progress.
