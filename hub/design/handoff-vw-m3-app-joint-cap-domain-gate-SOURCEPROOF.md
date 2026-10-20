# Source proof — actual App joint stored-cap candidate

## Candidate identity

```text
4720a864c81dc7002a9e95dbacf10cec8df5da81
  parent b1ef4b9b910ba72375c34cf319692f90d22edc25
  fix(timeline): preserve stored occurrence caps at preview boundaries

1fe351b9847d35db66ab294a6edf631447fa78ce
  parent 4720a864c81dc7002a9e95dbacf10cec8df5da81
  fix(timeline): use ES2020-safe own-property check
```

`4720a864…` is an ancestor of `1fe351b98…`.

## Relevant exact source

At `1fe351b98`, the producer has:

```text
src/tools/travel-between-images/components/shotTimelineDataProvider.ts:146
if (rawApp && Object.hasOwn(rawApp, key))
```

At the same commit, the serializer has the corrected form:

```text
src/tools/video-editor/lib/serialize.ts:43
if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key))
```

At the exact candidate `tsconfig.app.json`:

```text
target: ES2020
lib: ["ES2020", "DOM", "DOM.Iterable"]
```

Therefore the producer remains outside the declared language library and exact typecheck reports TS2550. This finding is independent of runtime Node support.

## Contract observations

The actual source places the derived scalar only in the existing projected `app.canonicalTiming` object. The raw counterpart is selected through the existing projection identity map; serializer exits remove only `storedOccurrenceDurationMs` and restore raw same-name values. The exact cap diff did not introduce a public DTO, wire/store field, `renderConfig`, new timing compiler, or pin change. These observations do not cure the ES2020 compile failure.

## Composition package identity

The exact App candidate lockfile declares Composition `0.0.12` from its tracked vendor tarball. Its SHA256 is:

```text
0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
```

The current Composition integration package is `0.0.13`; the read-only published artifact used for comparison has SHA256:

```text
9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
```

Both exact package bytes passed the same capped scene-boundary probe. No package version was assumed or changed.

## Verdict

**REJECT exact joint candidate pending a new compatible App descendant.** The necessary correction is confined to the App producer source; this worker intentionally did not apply it.
