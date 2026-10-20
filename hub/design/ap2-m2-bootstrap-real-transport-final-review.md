# AP2-M2 bootstrap real-transport final review

Verdict: **REQUEST CHANGES**

## Source decision

**REQUEST CHANGES.** The prior production callback bypass is fixed: `createCanonicalTimeline` and `ensureProjectHasTimeline` have no bootstrap callback parameter, and production wiring goes through `AstridRuntimeClient.createTimeline` plus the existing `RuntimeDataProvider.commitTimeline` path. The generated `WorkspaceClient.createTimeline` wrapper is the existing `/v1/projects/{project}/timelines` POST with JSON content type and idempotency key; the client wrapper uses the guarded `withMutation` path.

The durable outbox design is materially corrected and verified in the focused tests:

- `reserveCreate` persists the exact create method/path/body/key before transmission.
- The create ACK persists the creation checkpoint and receipt in the existing outbox record.
- Initialization is captured only from a verified sole pristine bootstrap publication, then reserved with the exact base revision/publication, command payload, route, and generated request key.
- `initializationRequest` revalidates the original request and commands before every replay; the accepted initialization keeps its historical request/result link and immutable closure proof.
- The real transport test observes one create and two byte-equivalent init commit requests after a lost init response, with the same idempotency key.
- Names, first/additional IDs, alias resolution and metadata CAS, headed/nonempty refusal, and constrained same-ID repair remain represented.

The remaining blocker is the replacement `createDefaultTimeline.test.ts` real transport test. Compared one-to-one with the original test, it does not retain all original guard assertions. Its handler accepts any path matching `startsWith('/v1/projects/${project}/timelines/') && endsWith('/commit')` rather than the exact target timeline path, and it echoes any commit body rather than validating the complete request. The test only checks a partial command/base payload and does not assert the original content-type/header guards, exact native commit route/body, or the complete identity/handshake request contract. The old test's no-legacy-route assertion is also no longer explicit. The native sequence may change, but these guard assertions must survive in adapted form.

Minimal correction: make the native transport reject/record an exact project+timeline commit route and assert the complete create/init request bodies, content-type and idempotency headers, expected identity handshake values, and explicit absence of the legacy timeline-document/publication path. Keep the existing exact-retry assertions.

## Required verification

Applied only to private copy `/tmp/ap2-m2-bootstrap-final-review.4AqGQj` from base `05b6b488d1834650c459c5c565f2530d9bea20e9`.

```text
sha256sum handoff-ap2-m2-bootstrap-real-transport-consumer.patch
9c6e05abd9cb330edce41e7d717aad43189ce81bc87c3fb4da02ba291867c59

git apply --check <patch>       PASS

vitest ... bootstrapInitialization.test.ts bootstrapCapture.test.ts \
  commitOutbox.test.ts createDefaultTimeline.test.ts
4 files, 127 tests passed

vitest ... client.test.ts clientSharedSession.test.ts
2 files, 31 tests passed
```

The clean worktree remained unchanged. No full, browser, localhost/socket, Runtime Door, normal014, or opaque-inverse tests were run.

## Separate holds

- normal014: **HOLD** — separate compatibility gate; not run here.
- opaque inverse4fail: **HOLD** — separate Agent gate remains unresolved; not changed or run here.
- real Runtime Door/browser: **HOLD** — explicitly out of scope for this review.
