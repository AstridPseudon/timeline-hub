# A4 provider map summary

At Agent 6531622c8f198c3efb509217e303fcad0126c47b and App 4c4c9c77c96fab70c4efef09db9a3bc456b0d803, the registered provider surface is doc.patch and clip.add-media. track.reorder and transcript.associate are absent from the Agent registry, schema, handler, and Python provider fixtures.

The mounted App parent-media commit-session port reaches the registered clip.add-media provider with the expected command envelope and read/created/step metadata. App after-anchor and track-reorder capture modules are dormant at this snapshot; mounted after-anchor/track edits use local row/config mutations represented by generic doc.patch. No mounted transcript-association caller was found.

Existing parent-media tests in tests/editing_conformance/test_recipe_m2_parent_media.py cover the strongest registered fixture: clone/rate-aware timing, ripple/order, null/absent/opaque data, created and previous claims, membership/order guards, refusals, and detached-provider boundaries. Generic tests/editing_conformance/test_doc_patch_v2.py covers generic list/order/merge and claim behavior. Existing transcript provider tests cover exact verified source pins, retained inputs, source overwrite, and atomic malformed-source refusal, but not App nested transcript/caption/review reconciliation.

Evidence collected:
- --collect-only for both candidate suites: 187 tests collected in 1.55s.
- test_doc_patch_v2.py: 102 passed in 11.81s.
- test_recipe_m2_parent_media.py: 71 passed, 14 failed in 26.64s; failures are existing registry-guard and reload/inverse cases, not repaired or hidden.
- Transcript-focused provider selection: 9 passed, 105 deselected in 2.17s.

No source or test changes were made. No new test should be authored until the orchestrator/App worker confirms whether desired retirement is generic doc.patch coverage or preservation of dormant capture claims; the latter has no current provider entrypoint and cannot be honestly certified by a Python witness alone.

