# vw-m4-duration-input-contract-review-0738

## Result

**APPROVE.** The exact two-file delta at reviewed commit `b3443897bededee1b3a08a8d8adabffa63161bd5`, parent `7bb54bbd64107e5090643ecca1e4d33164173e85`, is the smallest accurate Composition source correction for this boundary. Reviewed tree: `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`.

The delta is limited to:

- `typescript/src/lib/duration.ts`: `getTimelineDurationInFrames` changes from `TimelineConfig` to inferred `T extends Pick<TimelineConfig, 'clips'>`.
- `typescript/tests/duration.test.ts`: focused clip-only, resolved-shaped, and full-config literal smoke.

No App source, package version, pin, release artifact, runtime implementation, public13/frozen gate6 tuple, or graph change is present.

## Contract review

The inferred generic is correct for the stated contract:

- An App `ResolvedTimelineConfig` with optional `theme` and resolved-only siblings is accepted because only its `clips` member is constrained; its `ResolvedTimelineClip[]` remains compatible with `TimelineClip[]`.
- Existing direct full-config literals remain accepted because inference captures the complete literal as `T`; this avoids the excess-property regression that a non-generic `Pick<TimelineConfig, 'clips'>` parameter would cause.
- Clip and FPS type safety remain intact: `T` must provide `TimelineClip[]` through the constraint and `fps` remains `number`. The generic does not weaken the clip element contract.
- The broader sibling acceptance is static only and accurately describes the existing implementation: ignored fields are not read. The function's actual input contract is the `clips` collection, not `theme`, output, tracks, or resolved metadata.

The existing root public export in `typescript/src/index.ts` and the `TimelineConfig`/`TimelineClip` declarations remain unchanged. The producer's declaration build emitted:

```ts
export declare const getTimelineDurationInFrames: <T extends Pick<TimelineConfig, "clips">>(timeline: T, fps: number) => number;
```

## Runtime evidence

The source body from `return Math.max(` through the function end is byte-identical to `7bb54bbd6`; only the parameter declaration changed. The focused smoke returned `30` frames for all three accepted shapes. No runtime arithmetic, rounding, defaults, or clamping changed.

Producer evidence reviewed:

- `./node_modules/typescript/bin/tsc -p typescript/tsconfig.test.json --noEmit` — passed.
- `node scripts/build-typescript.mjs --test` — passed.
- `node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/duration.test.js typescript/test-dist/tests/evaluation.test.js` — passed, 2 files / 0 failures.
- `node scripts/build-typescript.mjs` — passed; emitted the declaration above.
- `git diff --check` — passed.

Independent source-review checks in this review also passed:

- `git diff --name-status 7bb54bbd6..HEAD` — exactly the two files above.
- `git diff --check 7bb54bbd6..HEAD` — passed.
- direct source comparison — runtime body byte-identical; root export and base type declarations unchanged.

## Remaining check

The coordinated downstream check remains: rerun the qualified App seven-site TypeScript program against this corrected public declaration and confirm the seven `TS2345` diagnostics disappear without changing the other 56 diagnostics. The seven sites are `ShotTimelinePreview`, `CompactPreview`, `VideoEditorAssetPanelSurface`, `TimelineEditorShellCore`, `TimelineRenderer`, `useDerivedTimeline`, and `useRenderState`.

That App check, release/adoption/pin work, full suites, browser/live-socket tests, Runtime tests, and package publication were not run or authorized here. This report is source/type-contract agreement only; it is not a release or adoption decision.
