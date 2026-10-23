# Handoff: A3 popup caller independent review

## Verdict

**FAIL** on current commit `8b5085cdc34671e9f6fef53827f6b084e89338d4`.

The mounted popup control is reachable and the current receiver’s 25-test suite passes, but production SWAP is not wired to a successful current `addClip` call. `ShotTimelineMediaControls.tsx:118-122` omits `time` when it sends `replaceClipId`; `useTimelineCommandsService.ts:455-469` rejects any prepared-asset call without numeric `time` before applying the edit. The caller test’s `addClip` mock hides this defect. Production ADD supplies time and reaches the intended A2 path, but the requested ADD/SWAP result cannot pass with SWAP refused locally.

The caller also does not revalidate the selected clip after async import when the mounted data reference remains the same; it retains the originally captured `replaceClipId`.

## Evidence

- Caller: `ShotTimelineMediaControls.test.tsx` — **3/3 PASS**.
- Current receiver: `shotTimelineDataProvider.a3.test.ts` — **25/25 PASS**, including Runtime selection custody, owner/revision binding, shared fork/sibling isolation, v2 envelope, accepted/merged/refused/recovery behavior.
- Preview: **25/26 PASS**; the sole raw opaque `__proto__` failure is unchanged from exact base `1117c15f7` (same assertion reproduced from a private base archive).
- Private exact `819acf` Composition graph: **PASS** (`0.0.14`, 80 files, archive SHA `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`). Root and Node TypeScript pass; App TypeScript fails only at the new nullable `runtime.project.projectId` assignment on line 81. Base App typecheck passes.
- Scoped ESLint, Runtime lock check against `34eac004`, and diff checks pass.
- Strict-islands remains blocked by the existing missing generated/virtual Composition modules.

No product files, tests, pins, locks, generated files, shared installs, or branches were changed by this review.

## Limits

No browser, HTTP/body, live service/socket, build, full suite, or central test-service run. The receiver’s full v2 fields remain covered by the unchanged current receiver tests, but no production caller PASS should be claimed until SWAP uses the supported current receiver contract and the nullable project identity and post-import selected-clip guard are resolved.
