# A4 provider-map corrected summary

**Verdict: FAIL for complete coverage-map parity; bounded registered-path findings PASS only.**

At Agent `079580ca46af77e0292d49dc34386b25c8391f99` / App `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` (current App mount check `58bf24ce6fc57c7477a7fa45d94b20dfb12c5e92`), the Agent registry has `doc.patch` and `clip.add-media`; it has no `track.reorder` or `transcript.associate` provider/schema/fixture witness.

- Correction: `createTimelineCommandSession`/`commitSession.ts` has no production value caller in the current App inventory; its five production imports are type-only. The actual mounted A2 source boundary is `localSaveSession.ts:152-179` plus `documentPatchIntent.ts` and `timelineLocalSaveHandoff.ts`, with production value callers in `shotTimelineDataProvider`, `useTimelineSave`, and `placementService`. `clip.add-media` remains a registered/detached provider witness, not a claim that the App currently calls that session. After-anchor and track UI behavior currently mutates local rows/config; transcript capture is not production-mounted in the frozen source.
- Parent-media witnesses cover raw/canonical birth, timing/ripple/order, null/absent/opaque input, reads, created/prior values, and refusal boundaries, but the retained targeted suite is **71 passed, 14 failed** (six registry-reload guard failures; eight nested inverse/reload failures).
- Generic `doc.patch` witnesses cover list membership/order, previous values, created IDs, null/absence, opaque JSON, conflicts, and refusal atomicity. They do not certify `track.reorder`.
- Transcript witnesses cover exact verified source pins, retained input closure, overwrite handling, word-anchor source behavior, and malformed-source refusal. They do not cover nested transcript planes, caption/review reconciliation, or `transcript.associate`.
- Prior evidence: 187 collected; `test_doc_patch_v2.py` 102 passed; transcript selection 9 passed/105 deselected. Runtime authority was `/home/user/work/runtime`; per-case module origin was not proven.

Corrected continuation: a test-only generic `doc.patch` witness may proceed within the PLAN after coordination with the App source owner/worker; no orchestrator approval is required. Missing/unregistered old operations are never permission to delete promised App behavior/tests. Preserve all old tests/implementation until faithful mounted coverage is executable. No product/test/provider/schema/pin changes were made here.
