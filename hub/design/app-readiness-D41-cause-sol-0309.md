**P3 fails at bootstrap outbox readiness; P2 passes that boundary. The underlying cause remains partly UNKNOWN.** No product changes were made.

- **P3 `3362`: FAIL, exit 2, 147s.** Bootstrap navigation, connection and selection completed. The 5000ms outbox poll failed; the outer assertion expected `initialOutboxRead.status === 'verified'` and received `'unknown'`. Original Gate 5 was NOTRUN.
- **P2 `12221`: FAIL, exit 1, 501s.** Its mounted-readiness leaf **passed** in 17.4s; failures occurred later in the original gesture body. Producer0307 owns case counts and safe-file export.

P3’s retained lifecycle records owner alias 1, generation 0 `basis-read` at 4041.2ms; cancellation at 8116.6ms with `sessionPresent=false`, `closed=false`; then generation 1 `basis-read` at 8121.2ms. No identity-read, session-created, basis-ready or rejection event appears. The seven-record snapshot reports no losses, overflow or rejected records.

The bounded network observations are:

| Run | GET `/…/timelines/:timeline/commits` |
|---|---|
| New P3 `3362` | First completed: HTTP 200, 3555.827ms, two items, no next cursor. Second unfinished in retained trace. |
| Old P2 `10973` | Two unfinished reads. |
| Old P3 `14249` | One unfinished read. |

“Unfinished” means trace status/duration `-1` with no retained response; it does **not** prove the server never completed.

The completed new P3 history head equals both captured mounted revision/publication pairs. Those mounted pairs also remain equal across the restart. **There is no observed head mismatch.** Config/registry comparison operands remain UNKNOWN.

The production await chain is [useTimelineSave.ts](/home/user/work/wt/app-readiness-D41-cause-sol-0309/src/tools/video-editor/hooks/useTimelineSave.ts:186) → original-basis loader → [loadTimelineCommandBasis](/home/user/work/wt/app-readiness-D41-cause-sol-0309/src/integrations/runtime/dataProvider.ts:885), which reads history before immutable parent/shot/internal sources. An internal-revision read was also unfinished. Missing request-to-generation aliases prevent identifying the exact unresolved await for each generation. The changed effect dependency causing cancellation is likewise unrecorded.

Passing P1 `18792` used a different retained App tree, explicit timeline selection and a 90s initial-owner wait. Its loader/support/spec match App804, while the save hook and handoff differ. It establishes a working flow, but cannot establish this native bootstrap’s cause.

Source custody checked: App804/tree8437, qualified Agent079/Runtime37eb, child0256 and Remotion0258. Installed `service.py` and `timeline_commit_store.py` bytes exactly match Runtime37eb. Retained metadata observes the child interpreter and `runtime_protocol.cli`; actual daemon imports/source commit and provider attachment remain explicitly UNKNOWN. Runtime0302 certifies **145 passed/60.12s on Agent4151**; the 59.37s run has UNKNOWN Agent provenance. Agent079’s baseline transcript failure is not evidence of this cause.

**Verification:** no new tests, services or journeys launched. Read the SAMEID terminal results for the registered `full-e2e-three-products` and `ap2-P3-gate5-h6-0348` commands above. `git diff --check` passed; five inspected production/support files match App804 exactly; worktree remains clean.

**Next action:** independent reviewer0309 classifies this report. App A2 should then add narrowly scoped diagnostics for changed effect-dependency booleans and generation-correlated history/immutable-read start/end phases. No supported product defect yet warrants a fix or OLDRED/newGREEN control. Originals were preserved; commit message and `DONE` were written.