# App A4 after-anchor first-return cumulative independent review — PASS

PASS for the bounded mounted prepared-media after-anchor persistence contract on
`tl/app-A4-after-mounted-final-review-1958` at `a99b08ff64`, against `6e04a9a9a7`.
This is not whole-A4 or P1GO completion; branch remains HOLD.

Actual production trace:

`useTimelineCommandsService.addClip({ preparedAsset, afterClipId })` →
`applyPreparedMediaCommand` → real `save.applyEdit` → `useTimelineSave` →
`useTimelinePersistence` → `createLocalSaveSession`/IndexedDB outbox →
`RuntimeDataProvider.commitTimeline` → `AstridRuntimeClient` → generated
`WorkspaceClient` transport. The test uses a controlled final transport only;
provider/client/generated request and response parsing are real.

Accepted coverage verifies paired canonical base, source asset, track, stable
created ID, exact doc.patch guarded changes, source window, opaque/null values,
absent hold, order, V1-only ripple, full request serialization/route/body/key,
accepted data+receipt, authoritative steps, merge mode, canonical digests,
`receipt.result === data`, and canonical adoption/outbox clearing.

409 coverage uses `details.current` (not invented `details.head`) with status,
base, current, conflicts, code, path, hint, and suggested command. It proves
rejected rollback/revalidation, retained durable intent, and message; it is not
classified as unknown/retry.

The old 356-line/37-assertion raw after-anchor test and the retained media
normalization cases remain unchanged. Their `clip.add-media` reads/selections/
bindings/records are not claimed as mounted parity: the actual mounted path
emits generic atomic `doc.patch` with a registry set, clip list insert, and
ripple set. Raw missing/null/subminimum/transition/at_ms/ambiguity and current
preview/unavailable differences remain bounded or uncovered as stated. No
production, old-test, schema, generated, lock, pin, or environment change was
made.

Evidence: targeted Vitest 3 files/29 tests passed; App, Node, and root TypeScript
passed under `flock -w 600 /home/user/work/.app-tsc.lock` with 4096 MB; scoped
ESLint passed with zero warnings; `git diff --check` passed; cumulative diff is
only the new persistence test. No full/browser/live/service/P1/P2/P3/benchmark
suite was run.
