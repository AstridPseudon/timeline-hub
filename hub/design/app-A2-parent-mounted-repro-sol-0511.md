**A2/P2 outcome: RED reproduction; precise pre-outbox refusal identified.** Only [A2-parent-mounted-repro.test.tsx](/home/user/work/wt/app-A2-parent-mounted-repro-sol-0511/A2-parent-mounted-repro.test.tsx) was added. Existing source remains unchanged.

Using retained D45/13583 fixtures and production provider loading, mounted drag callbacks, save subscription, owner initialization and capture:

- Pointer movement 181→341 produces the original **0→5s** display change.
- Rows materialization also drops the selected clip’s `opaqueClip`.
- `timelineLocalSaveHandoff.ts:324–326` rejects the authentic move capture: **“parent gesture changes more than its selected fields.”**
- Interaction-end rescheduling at `useTimelinePersistence.ts:1334` loses the gesture basis; its second capture rejects as `child-ownership-unavailable`.
- Ready and delayed-identity cases each leave **one owner, zero intents, no reservation and zero dispatches**.
- Delaying the original verified read instead produces `owner-original-read-invalidated`, a distinct boundary.

Final commands:

```bash
A2_FIXTURE="$TMPDIR/a2-source-fixture.json" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/a2-vitest.config.mts" --configLoader runner --no-cache
```

**2 failed, 1 passed; 5.92s.** Required save assertions remain RED.

```bash
/opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/a2-controls.config.mts" --configLoader runner --no-cache --testNamePattern 'passes the original ordinary move inputs'
```

**2 passed; 18 unselected; 3.53s.** `git diff --check` passed.

The reproduction uses genuine provider loading to preserve production defaults. Capture observation is call-through; no basis was injected and no Runtime acceptance was fabricated. Full-v2 transmission, reply handling and adoption remain unverified because append is never reached.

Artifact SHA-256: `ace36aafc5102c24d4c94dbb455bec16183b690ad109596615759b672260c744`.

Next bounded owner: **App A2 / sol0505**, coordinating rows materialization with the handoff’s selected-field check and separately examining deferred gesture-basis retention. This establishes the offline mechanism; original13583’s internal ordering remains unobserved. No product fix or original rerun performed. Commit message and `DONE` created.