# A3 child-placement handoff

The App placement entry point now accepts an explicit `occurrence:<id>` owner. With that field, it loads the verified canonical closure, emits the existing Agent `occurrence.fork` semantic command through the existing A2 LocalSaveSession/outbox, then reloads the accepted head and performs the existing parent placement mutation. Without it, parent placement is unchanged.

The targeted service test proves the command envelope (`select`, reserved `shot_id`, occurrence ownership intent, and created shot ID), two outbox commits, and shared-source preservation: the selected occurrence points to the forked physical shot/revision while its sibling still points to the original. Invalid/ambiguous owner and destination guards remain covered.

Evidence: 39 targeted Vitest tests passed; App `tsc --noEmit`, scoped ESLint, and `git diff --check` passed; normal Runtime/Agent producer locks and the private exact819acf Composition graph passed. Full/live/browser/body admission remains intentionally unverified.

Changed files: `src/shared/lib/placement/placementService.ts` and `src/shared/lib/placement/__tests__/placementService.test.ts` only. Independent Luna review and App-home merge-forward remain next.
