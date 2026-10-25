## PASS — A3/P2 core cumulative review

Applied only the exact two reviewed blobs to clean `5337b439b9`.

- Mounted native-none path: old product RED (9 passed, bulk outbox intent missing).
- Fixed product: mounted test GREEN, 10 passed.
- Adjacent suites: 113 passed.
- `tsc --noEmit --incremental false`: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected six paths unchanged.
- Exact candidate blob hashes verified:
  - test `9b5d08cceed77b7a655bb000a631872f77ab18d1`
  - hook `b3bac8a440bf2152dc85143cb745757c78696c06`

The test covers the real mounted flow: canonical projection → clip selection → Effects/Transition/None → `useTimelineCommit` materialization → persisted outbox → held `commitTimeline`. It asserts full v2 request fields, reads, removals, labels/intents, source, idempotency persistence, opaque fields, sibling clip, tracks, registry, markers, occurrence, and ACK adoption. Existing stale/wrong-editor controls remain green.

The repair preserves only authored top-level extension keys outside `TIMELINE_CLIP_FIELDS`; known fields remain authoritative, so explicit transition deletion is not resurrected.

Fixture limitation: the retained harness source was matched field-for-field for the available values and shape, including `crossfade/.5`, native-none metadata, markers, tracks, registry structure, and occurrence ownership. Actual 21061 canonical browser bytes and original media identities remain unavailable. `source_mapping` is Agent-bundle-derived and is not present in this App canonical fixture/seam; no live Runtime receipt/history claim is made.

No full/browser/service/build/install suite was run. `commit-msg` and `DONE` were created.