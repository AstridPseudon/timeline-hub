# App parent-media swap native-parity review

## Verdict

**Not qualified for native parity.** The App helper produces the correct authored result and core write/dependency set, but its submitted command/record claims are not the Agent-native claims. Passing the App-only tests therefore does not establish SDK parity: sending the App command to the actual Agent handler fails immediately with `CommandError(kind=capture_mismatch, message="submitted resolved does not match authoritative capture")`.

## Compared implementation

- App: `src/tools/video-editor/commands/parentClipSwapCapture.ts` and `parentClipAddCapture.ts` at `7c1343104`.
- Agent: `3c4f6de4` ordinary014 source pair, with the parent `clip.swap-media` handler/schema from the private014/current cut (`6b2309aa`); `native_occurrence_media_commands.py` was inspected directly.
- The `edit-command.schema.json` SHA-256 is identical at `3c4f6de4` and `6b2309aa`: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

Both sides use `schema_version: 1`, `op: clip.swap-media`, `version: "1"`, `select: parent/clip:clip-a`, exact five-field `old_media`/`media`, and `intent.ownership: parent`.

## Fresh pure subprocess evidence

The temporary TS capture wrote one bundle/command to the own worktree; an inline Python subprocess imported the actual Agent tree (`PYTHONPATH=.review-agent`, Agent archive `6b2309aa`) and ran the native capture, `execute`, inverse, replay, and refusal cases. No HTTP, Runtime provider, browser, socket, or full suite was used.

Successful replacement:

- Native writes exactly two records: `parent/asset:reserved-new` absent -> the four-field binding (`media_id`, `type`, `generationId`, `variantId`), and `parent/clip:clip-a::asset` old alias -> new alias.
- Native created IDs exactly: `[{"ref":"parent/asset:reserved-new","kind":"asset","owner":"parent"}]`.
- Native bindings exactly: fixed `media.owner=parent`, fixed `media.track=parent/track:overlay`, and fixed `media.target=parent/clip:clip-a` depending on `media.old`/`media.new`.
- App and native final bundles were byte-for-byte JSON equal: both clip mirrors changed only `asset`; `at`, `hold`, `from`, `to`, `speed`, and opaque clip fields survived; the old registry binding (including opaque data) survived; the new binding was added to both equal direct/nested registry mirrors; placements/shots were unchanged.
- App/native `writes`, `bindings`, `created`, `dependencies`, and `derived_writes` were exactly equal.
- Native inverse returned the original bundle exactly; native replay over an unrelated `clip-b` opaque write succeeded and preserved that peer change.
- Native stale-source refusal: `dependency_changed`, `original authored guard changed`, no mutation.
- Native wrong-selection refusal: `dependency_changed`, `media edit requires exact Runtime-verified media input`, no mutation.

## Exact parity mismatches

The App command/record claims differ from the native command/record:

- `command.resolved`: App `[]`; Agent `['parent/clip:clip-a']`. This is the immediate `capture_mismatch` blocker.
- App records 10 reads; Agent records 7. App has three extra/non-native reads: `parent::config.output.fps`, `parent/source::source_window`, and the empty `collection.occurrences` selection/read. Agent's parent swap reads only the clip collection, target clip, track collection, target track, asset collection, old asset, and new asset, in that order.
- App's old-asset read includes the opaque registry member; Agent's effective-registry read omits that opaque member while the final bundle still preserves it. The guards are not the same.
- App records a `collection.occurrences` selection; Agent records only `collection.clips` and `collection.tracks`.

Minimum fix: make the App parent-swap capture emit the Agent handler's authoritative `resolved`, read set/order/state projection, and selection set before retaining submitted claims. Do not paper over this by treating App self-mirroring as proof; the actual SDK currently rejects the App command.

## Additional guard mismatch

The fresh fixture added an incoming transition while retaining the same valid raw source range. The actual Agent handler accepted the parent raw swap and preserved the transition. The App helper refused it at `parentClipAddCapture.ts:258` (`row.transition != null`). The Agent's raw-parent path intentionally bypasses the transition refusal for `raw_window=True`; the App guard should be scoped equivalently. The App code also requires a positive `hold` even where the Agent raw-window path derives it from `to - from`; recheck that missing/null-hold case before qualification.

## Tests

- `npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts --no-file-parallelism --cache=false` — **2 files, 10 tests passed**.
- Fresh temporary TS capture/guard test plus the actual Agent subprocess bridge — **1 test passed** for App capture, and the subprocess reported the results above; it was removed after the run.
- Actual SDK bridge: `PYTHONPATH="$PWD/.review-agent" /home/user/work/venv-app2-native/bin/python` with inline JSON bridge against Agent archive `6b2309aa` — **exit 0**; native replace/inverse/replay/refusals all completed.

No Runtime full/three-node rerun, HTTP/provider test, schema/API/artifact/pin/dependency change, or source edit was made.

## Blockers and next step

Blocked on App-side claim/guard alignment. App source was intentionally not edited per review scope. The App owner should align the capture claims with `native_occurrence_media_commands.py`, add a direct App-to-actual-SDK conformance test that submits the returned command, and add transition plus missing/null-hold parity cases before re-review.
