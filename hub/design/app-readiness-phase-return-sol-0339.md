Corrected `dataProvider.ts` diagnostics and focused tests only.

- History `end` follows existing head validation.
- Parent/shot/internal `end` follows canonical validation and graph projection. Failures refuse open phases and preserve the primary error.
- Coalescing, hook/handoff blobs, awaits, guards, and diagnostic schema preserved.

Validation used `/opt/node20/bin/node`:

- `node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest-bundled.mjs" --configLoader runner --no-cache src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/lib/timeline-diagnostics.save.test.ts` — **109 passed**.
- Same runner with private donor config and `-t 'does not complete unvalidated reads|defers immutable completion'` — old source: **17 failed, 2 passed**; all 19 controls pass after repair.
- `--import tsx tests/e2e/local/p1-diagnostic-safety.test.ts` — **22 passed**.
- `--import tsx tests/e2e/local/mounted-readiness-safety.test.ts` — **12 passed**.
- Flocked `tsc --noEmit --incremental false -p` for `tsconfig.json`, `tsconfig.app.json`, and `tsconfig.node.json` — passed.
- Scoped `eslint --max-warnings 0`, `git diff --check`, scope and donor-identity checks — passed.

Boundary limit: immutable completion establishes existing closure validation/projection success, not cryptographic digest recomputation or authoring/mounted readiness. The authoring-bundle await remains unchanged in prohibited handoff code.

No full/browser/backend/service runs. Commit message and `DONE` written. Recommend independent cumulative review before merge.