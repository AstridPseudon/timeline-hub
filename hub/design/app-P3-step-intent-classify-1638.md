## Result

- No product or protected test files changed.
- Classified the failure as an outdated protected setup oracle, not an App regression.
- Source intentionally emits `Move f2-app-clip on V1` at [timelineLocalSaveHandoff.ts:572](/home/user/work/wt/app-P3-step-intent-classify-1638/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:572).
- Passing P2 and local handoff controls independently confirm this intent provenance.

Minimal setup proposal:

```ts
expect(second.step).toMatchObject({ label: second.label, intent: `Move ${seed.appClipId} on V1`, tags: [] });
```

Hashes, old → proposed:

- Full spec: `95d9a3e7…dd296c` → `a6468188…1e99a`
- Setup helper region: `28f7f84e…fb962` → `77c10439…eb6f4`
- Original Gate5 body: unchanged `d47d5526…9fb20`
- Canonical tail: unchanged `5ede6f37…80912`
- Reset block: unchanged `980b4cbe…2fe62`

## Tests

- `node --test tests/e2e/local/support/p2-parent-oracle.test.mjs` — 6/6 passed.
- `vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts` — 70/70 passed.
- Retained D66 P1 control — 2/2 passed.
- Retained D66 P3 run — readiness passed; primary failed only at `three-products.spec.ts:1347` on the stale generic-intent expectation. Separate afterAll tuple drift was Agent/Runtime during-run source movement.
- `git diff --check` — passed; worktree clean.

C0 alignment: `contract/commit-v2.md` §§1, 4, 7 require requested step intent, authoritative reply steps, and persisted authoritative history. `DONE` and the P3 commit message were created; no source commit was needed.