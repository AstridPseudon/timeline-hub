# App A4 after-anchor mounted persistence

The actual production caller is now covered at the mounted boundary: `useTimelineCommandsService.addClip({ preparedAsset, afterClipId })` builds the prepared-media preview, the real `useTimelineSave`/`applyEdit` path authors the canonical local document, and `localSaveSession` persists the original v2 request through the outbox to `commitTimeline`.

Old behavior → kept production property:

- raw after-anchor source-window clone → editor preview preserves `from`, `to`, `speed`, transitions, params, app opacity/null/opaque values, and absence of `hold`;
- normal duplicate placement → stable editor allocation, exact clip order, V1 ripple only, and unchanged V2 sibling;
- local optimistic save → full v2 `doc.patch` request with created ID, step patch, atomic merge mode, and idempotency key;
- accepted reply → canonical document adoption;
- genuine Runtime conflict → rollback to revalidated canonical head, retained rejected outbox intent, and conflict message.

The old raw capture/executor tests remain intact; they are not presented as proof of mounted production equivalence. Malformed-409/unknown-retry coverage, live HTTP behavior, browser journeys, and full-suite evidence remain outside this A4 test and were not run.
