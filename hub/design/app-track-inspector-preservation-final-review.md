# APPROVE — App TrackInspector preservation gate

Decision: APPROVE candidate `d821e5587e4d428e9e3e3dfbe5b7195e192bd00e` on top of integration `590c19795111fd1891bbd50a5f8d48bef3505a26`.

Tree: candidate `aedee085ec20135e896a6d258dc1845cc352f423`; base `1955b25d2bad77ae8c36e1918a2a6f69dd795bd3`. The candidate is test-only: exactly these three paths differ from `590c19795`:

- `src/tools/video-editor/components/PropertiesPanel/TrackInspector.test.tsx` (new, 159 lines)
- `src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`

No product files changed. `git diff --check` is clean. No skip/only/fails markers were added.

Old → new coverage mapping, verified against `9d518546d`:

- `TrackLabel.command.test.tsx:61-85`, the production rename positive across desktop/phone/tablet, maps to the real `TrackInspector.test.tsx:65-92` command-path positive. It renders the actual `TrackInspector` and actual `useTimelineTrackManagement`; capture/finish use the real capture helpers. The command, original `Original` guard, preview, unchanged remote display state, opaque-field preservation, one submit, and absence of `onChange`/legacy `applyEdit` are asserted.
- `TrackLabel.command.test.tsx:104-120` plus the phone/tablet sheet-close refusal at `:153-177` maps to `TrackInspector.test.tsx:94-118`. Unmount/remount models close/tab switch, refusal is visible, the dirty draft survives reopen and a remote update, the original capture is not refreshed, and retry submits the identical command payload.
- `TrackLabel.command.test.tsx:122-138` maps to `TrackInspector.test.tsx:120-137`: capture refusal keeps typed input and visible error, with neither finish, submit, `onChange`, nor legacy `applyEdit` called.
- `TrackLabel.command.test.tsx:87-102` and clean-close recovery at `:179-197` map to `TrackInspector.test.tsx:139-158`: unmount releases a clean edit, remote state is visible on reopen, and the next edit captures the new remote head.
- `TimelineCanvas.test.tsx:2505-2528` touch selection maps to `TimelineCanvas.test.tsx:2505-2510`, explicitly parameterized for both `phone` and `tablet`, with exactly one `onSelectTrack` call. Desktop inline editing remains separately asserted at `:2512-2527`.
- `TrackListRenderer.test.tsx` comment at `:698-700` now points to the actual `PropertiesPanel/TrackInspector.test.tsx`; touch rows are asserted to select the Inspector target rather than a removed sheet. Existing PropertiesPanel tests retain add/delete Inspector controls.

The port is not mock-only absence testing: the Inspector and command-management hook are real, command capture/finish are real, and positive command/preview/guard expectations are present. The shared Inspector has no device prop; phone/tablet scope is covered at the actual Canvas selection boundary by the explicit two-device case, while the shared Inspector behavior is tested once on its real surface. No second touch UI or product feature was introduced.

Evidence:

- PASS — `/home/user/work/app/node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/PropertiesPanel/TrackInspector.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx` — 3 files, 120 tests passed.
- Not evidence / startup failure — same command with `--configLoader=runner`; this repo config references `__dirname`, so collection stopped with `ReferenceError: __dirname is not defined`. The bundled-config command above passed.
- Not run by instruction: full suite, browser/e2e, build, and TypeScript compiler.

The owner’s 15:46 inbox ruling was read verbatim: integration was frozen at `590c19795` until this fix-forward port, before the one full. This candidate satisfies that gate; the one full remains the next orchestrator action.
