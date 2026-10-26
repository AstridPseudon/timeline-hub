# Handoff

Use `withMountedD141jVisibilityCollector(page, testInfo, expectedOccurrenceId, run)` as the private candidate opt-in around the existing mounted popup journey. It imports `/src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts` in the browser devserver context, retains `d141j-visibility.json` before the existing page fixture closes, and then uninstalls the collector.

The retained artifact is suitable for the unchanged checker when genuine mounted events are present. A real failing popup may retain empty groups or no events; report those observations and the original checker/gesture result honestly. Do not run the checker as a way to convert an absent native chain into PASS.

Future native admission remains gated: one ordinary run, TEST_KEEP inherited, one 5-second native trace, 180-minute bound, same-session polling, no relocation/resubmit, and a 4 GB stop floor only after the one-time free-space threshold is met. Current free space was 4,699,103,232 bytes, below the 5.2 GB future threshold; no future run was attempted.
