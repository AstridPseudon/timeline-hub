# Findings

## D141J-REVIEW-001 — mounted lifecycle is not wired

The candidate adds `tests/e2e/local/support/d141j-visibility.ts` and its source controls, but the only call sites for `installD141jVisibilityCollector` and `withMountedD141jVisibilityCollector` are the new finite test file. There is no call from `tests/e2e/local/three-products.p2-popup.spec.ts`, `tests/e2e/local/support/app.ts`, `elementApplyDiagnosticPageFixture`, or another real mounted page fixture.

The production chain is real and unchanged: `useAstridShotsHost.ts:210` records accepted reads; `useShotGroups.ts:188,273,336` records active and grouping boundaries; and `TimelineEditorCore.tsx:931` records the pre-overlay boundary. Those observers only write to the module-private collector after `installD141jVisibilityCollector(collector)` runs. Since the candidate never installs it in the mounted process, its passing source controls cannot produce a native four-field artifact.

The helper’s finite behavior is otherwise sound: its browser action dynamically imports the existing module, uses the existing installer and snapshot, retains an empty or failed artifact before page close, attaches the JSON, and attempts uninstall in `finally`. These are source-control results, not mounted readiness.

## Packet distinction

Route-review-1256’s nonexistent `TimelineEditor.test.tsx` coordinate and missing `D66_RUNTIME_CHECKOUT` in its hand-authored normal recipe are defects in that prior operational packet. The author candidate uses the actual `TimelineEditorCore.test.tsx` control and does not alter the D66 builder or route recipe; neither prior packet defect is reclassified as a helper defect here.

No reviewer fix, synthetic passing outcome, test weakening, browser run, service request, body execution, registry action, checkout, or merge was performed.
