# Handoff

Verdict: `FAIL_FINITE_MOUNTED_WIRING`; candidate remains private and unmerged.

The exact future enable route is to call `withMountedD141jVisibilityCollector(page, testInfo, expectedOccurrenceId, run)` from the existing mounted popup diagnostic path, around the unchanged `p2-popup-add` journey. The callback must run while the existing single page is alive. The helper dynamically imports `/src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts`, installs the existing collector, and in `finally` snapshots it, writes `testInfo.outputPath('d141j-visibility.json')` with mode 0600, attaches the JSON, and uninstalls before the existing fixture closes the page. Empty events and original checker failures must remain honest.

The remaining finite gap is concrete: no current mounted spec or fixture calls that helper. A future admission must add only the allowed observational fixture/spec wiring, then re-run source controls and the unchanged checker. It must not alter the popup assertions, emitter/checker semantics, App values/control flow, C0 wire, registration, or production behavior. Native execution remains gated by the 5.2 GB admission threshold, one heavy run, inherited `TEST_KEEP`, five-second trace, 180-minute bound, same-session polling, and 4 GB stop floor.

Independent visibility 1245 remains immutable `PASS_SOURCE_VISIBILITY`; route-review 1256’s packet defects remain separate and do not grant mounted qualification.
