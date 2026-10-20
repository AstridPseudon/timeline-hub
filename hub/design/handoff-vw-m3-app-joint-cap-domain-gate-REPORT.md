# REJECT — actual App joint stored-cap See-domain gate

Decision: **REJECT exact joint candidate `4720a864c81dc7002a9e95dbacf10cec8df5da81` → `1fe351b9847d35db66ab294a6edf631447fa78ce` for the required See-domain gate.**

## Scope and ancestry

- Reviewed the actual published producer/consumer pair, not a running branch or an unapplied proposal.
- `4720a864…` is the producer/raw-context commit, parent `b1ef4b9b…`.
- `1fe351b98…` is the ES2020 descendant, parent `4720a864…`.
- `git merge-base --is-ancestor 4720a864… 1fe351b98…` passed.
- Producer/pins and Composition product source were not edited.

The candidate does satisfy the intended behavioral shape on inspection: one derived `app.canonicalTiming.storedOccurrenceDurationMs` is projected from the retained verified raw occurrence basis; the existing serializer removes only that derived scalar and restores raw `canonical`/`canonicalTiming` collisions; the consumer uses the existing bounded render selection/vector/extent seam. No added wire/store/DTO/renderConfig carrier or second compiler was found in the actual cap diff.

## Blocking finding

The exact final descendant still contains `Object.hasOwn` in the producer:

```text
src/tools/travel-between-images/components/shotTimelineDataProvider.ts:146
  if (rawApp && Object.hasOwn(rawApp, key)) {
```

The candidate `tsconfig.app.json` targets ES2020 and declares `lib: ["ES2020", "DOM", "DOM.Iterable"]`. Exact-candidate typecheck reproduced the owner report’s prior failure:

```text
tsc -p tsconfig.app.json --noEmit --pretty false
exit 2
src/tools/travel-between-images/components/shotTimelineDataProvider.ts(146,30): error TS2550: Property 'hasOwn' does not exist on type 'ObjectConstructor'.
```

`serialize.ts:43` was corrected to `Object.prototype.hasOwnProperty.call`, but the producer-side call was not. This is a concrete root-target compatibility failure, so I cannot approve the exact joint candidate.

## Passing evidence

- Exact `1fe351b98` App source, with its matching pinned Composition `0.0.12` artifact, mounted in an owned temporary dependency overlay: **9 files, 200 tests passed**. This covered serialization, draft/save persistence, command projection, popup publication, stored-cap surface, lifecycle/mailbox, and the captured cap fixture.
- Current Composition source targeted regression after private out-of-tree TypeScript compilation: `scene-evaluation.test.ts`, `transition-spans.test.ts`, and `transition-policy.test.ts`: **3 files passed**.
- Exact published Composition artifacts were read-only extracted and probed with the shared pinned peers: `0.0.12` and `0.0.13` both passed the cap boundary probe (`4000ms → end 120`, `4500ms → end 135`, uncapped → end 150).
- Exact artifact hashes: public12 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; public13 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Candidate App package lock pins `@banodoco/timeline-composition` to `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`; Remotion peers are `4.0.509`. The Composition integration tree/package is `0.0.13`. Both were verified, not assumed.

## Limits and next step

No browser, pixel/audio render, live socket, network, install, full suite, Gate 6, or producer/pin edit was performed. The App behavior tests passing does not waive the typecheck blocker.

App should publish a new exact descendant replacing only the remaining producer `Object.hasOwn` with the ES2020-safe own-property form, rerun the producer/consumer mounted lane and exact typecheck, then request this gate again against that descendant.
