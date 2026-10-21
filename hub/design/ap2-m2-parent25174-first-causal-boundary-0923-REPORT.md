# AP2-M2 parent25174 first causal boundary

## Verdict

The retained run is an actual failure, not a preflight or fixture failure.

- Original run ID: `ap2-m2-parent-corrected-custody-one-original-0915-ap2-m2-parent-corrected-custody-one-original-0915-integration-actual-1021091413-25174`
- Case source: `8eb4d08e60f434b938ea885c8cadca4bd87151b3`, tree `ea317333400d1a342f2520556eef8ce9399666c1`
- Public pins: Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- Result: exit 1 at `tests/e2e/local/three-products.spec.ts:1557`; `wire.attempts` stayed `0` for the 90s ceiling.

The first causal boundary is App's external-drop producer route, before native command submission. The input path asks for time 20, but `dropFileOnTimeline` sends the x-coordinate for the left edge at 20 (`tests/e2e/local/support/app.ts:231-233`). `computeDropPosition` supplies the default 5-second clip duration and subtracts half that width (`src/tools/video-editor/lib/drop-position.ts:128-131`), so the planner receives 17.5s. The rendered hit is the V1 transition clip: the packet's parent payload has V1 occupied at 15–18s, with the other visual track S1 free. `planClipDrag` therefore resolves the requested V1 row to the nearest free visual row S1 (`src/tools/video-editor/lib/clip-drag-planner.ts:484-510`). This is collision rerouting from the recorded geometry, not the prior reordered-row regression: the pointer is on the rendered V1 clip, while the planner's selected target becomes S1.

The route is then:

1. `handleFileDrop` passes the selected S1 track to the prepared video path (`src/tools/video-editor/lib/external-drop-utils.ts:352-356, 512-526`).
2. App performs the positive Runtime media import and exact five-field verified read successfully.
3. `addClip` builds a native row on S1 and calls `port.capture`, awaits the verified read, then calls `port.finish` (`src/tools/video-editor/hooks/useTimelineCommandsService.ts:494-549`).
4. Agent-side local capture rejects the row at `parentClipAddCapture.ts:379-383` because S1 is the occurrence-owned shot lane. `port.submit` is after that throw (`src/tools/video-editor/hooks/useTimelineCommandsService.ts:545-546`), so no Runtime commit POST, native Agent command submission, ACK, recovery, reload, undo, or original body assertions are reached.

The observed failure is therefore App-owned producer/geometry selection, not Runtime refusal, lost ACK, or oracle failure. The existing native occurrence fence remains strict and correctly catches the wrong S1 ownership.

## Exact retained Runtime evidence

The negative verification correctly returned 404 for the deliberately mutated object ID. The positive path returned 201 for media import, 200 for selection, and 200 for verified selection. Positive values were:

- object/asset: `sha256:826d8afe1c80dc66e571931663d6375a7cbeb59d164850a0156b470fd37a7ef6`
- generation: `generation-task-231543af4457485393a4549af8d294f5`
- variant: `initial-b4d0c87e51f637863357c566e45054ccaf42b7e7c7b8cb7bdb9b012b1cdc61e1`
- catalog: `sha256:0d401b7b43dfc2a8983dc9d2655bf622c86c32e000badd9cfb9a50b4bd346616`
- verified media: `video/webm`, size `160935`, duration `12.0`

No guessed wire is used. The positive verified selection is the exact selection returned by Runtime; no Runtime commit command was sent.

## Packet hashes

Authoritative packet root:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/evidence-final95-parent-8eb4d08e/run`

```text
bounded-browser-evidence.json b0325b1a90dc0c8ff36861b8f68cec5ed68a7410e2e0de5b35803bb389ddc151
error-context.md              293c424c3149a83655f5f838e2acf8ae8edff75a987614cdf1f20dd07aee705c
evidence-presence.json        0ab19165d6ac03ac502930a7e33b5f6cfda679e7b450e33b0f75b477b689374b
playwright-trace.zip          386071fb3b9bf92226f0e41c2c7ba8da9548b10622702b11fdbd1d966ccbbe1d
result.txt                    6afccb5b43a157a7f5bc8cdb2dce50e3f6c196db3420f6082169f13ce1775ae9
runner-tail.log               824dcec49533a7ddd20d0dbe2d96f90f7022e4dd0f3121d6191bc2601e0626a6
source-identity.txt           b5b29bdf8671a36a2622dab70fa7abb11c68660a3a6fefaff98e9cd5e5ac46f4
```

There is no packet/source identity mismatch: `source-identity.txt` matches the exact case source and tree above, and the worktree has no source changes. The first behavioral source mismatch is the 20s left-edge input versus the producer's implicit centered 5s interpretation, which changes the selected route to S1.

## Smallest next action

App2 should make the real external-file-drop coordinate path pass an explicit zero x-offset (left-edge semantics) into the drop coordinator, while leaving clip-drag pointer offsets unchanged. The regression recipe is the existing mounted journey: drop `manual-drop.webm` at nominal 20s on `f2-transition-clip`, assert the first native row is `track: V1`, `at: 20`, `clipType: media`, then exercise the existing fault-first ACK/recovery and undo assertions. Do not alter the native occurrence fence or Runtime/Agent wire.

No source, fixture, assertion, helper, pin, authority, or budget edits were made; no retry or test rerun was performed.
