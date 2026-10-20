# AP2 M2 selected current DEV original-P1 gate

## Scope and source reconciliation

Base was `hub/tl/integration`, current head `157eef8cf1151db09310153c10856d45d8590c87`. The committed donor source was `d0c563bc452b2d39b7202df574684ecb7b7f410f` (`test(app): repair selected P1 fixture provenance`), with its parent selected journey source `7db1752cad0ac37fa137f3693fe66269ae53e354`. The selected spec was ported onto the current App harness; its SHA-256 matches the donor exactly.

The fixture uses the required real provenance:

- initial selected clip: same-id/effect/hold carrier, `elementRef.revision: 'draft-1'`, and no `packId`;
- normal Agent `timelines update-element` producer admits the project-owned P1;
- accepted Runtime history is asserted to contain exactly `clip.set-element`, then `clip.set-params`;
- P2 is admitted through the real project-pack path, authored source is removed, and the journey expects retained P1 behavior after reload, refusal, exact lost-ACK retry, and undo.

No fake document, hash, schema, authority bypass, browser alias, or synthetic history was added. The selected source retains the strict public Composition 0.0.13, Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and private graph guards in the repaired absolute driver. Existing integration content represented by selected shared `5a7144b55`, current adapter `7d`, and native trim `0fa` was not changed.

## Current-tree Composition repair

The locked Composition 0.0.13 archive has `dist` exports but no `typescript/src` sources. Current `config/vite/vite.config.ts` already names App fallback paths for the theme API and generated registry, but both fallback files had been deleted by earlier cleanup. The central build therefore failed with:

```text
[vite:load-fallback] Could not load .../src/tools/video-editor/lib/theme-api.fallback.tsx
ENOENT: no such file or directory
```

The candidate restores the small existing fallback implementations at:

- `src/tools/video-editor/lib/theme-api.fallback.tsx`
- `src/tools/video-editor/lib/registry.generated.fallback.ts`

These are Composition compatibility sources only; they do not supply selected-element authority or project document data.

## Static evidence

- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts src/tools/video-editor/lib/registry.generated.fallback.ts src/tools/video-editor/lib/theme-api.fallback.tsx` — passed.
- `npx tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.
- Exact target guard: Playwright collection selected one test from `three-products.selected-param-dev.spec.ts`, titled `local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo`.

## One central gate and result

The only central command run was:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
mkdir -p "$ORCH/scratchpad/orch/tests/cache"
R=$("$ORCH/scratchpad/orch/bin/request-test" ap2-m2-selected-current-dev-original-p1-gate ap2-m2-selected-real-p1-history-fixture-fix --no-cache)
"$ORCH/scratchpad/orch/bin/wait-test" "$R"
```

Result: `ap2-m2-selected-current-dev-original-p1-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020224832-2034`, exit 1 in 27 seconds, on snapshot tree `aa506e4edffcba18f441d4766d13ed0695064bcd`. Collection succeeded and listed exactly one test. The hosted Vite build transformed 3321 modules and then failed before browser launch, DEV server execution, Runtime journey, or qualification because the fallback file was absent in the pre-repair snapshot. The retained evidence is:

- result log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-current-dev-original-p1-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020224832-2034/log.txt`
- retained stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/driver.stderr`

No local driver/browser/socket/full run was performed. No second central gate was submitted. The selected DEV qualification is therefore **not qualified**.

## Next step

The code-only candidate is ready for orchestrator review. If a new central gate is authorized, use the same named suite against this post-fallback source tree:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$ORCH/scratchpad/orch/bin/request-test" ap2-m2-selected-current-dev-original-p1-gate ap2-m2-selected-real-p1-history-fixture-fix --no-cache)
"$ORCH/scratchpad/orch/bin/wait-test" "$R"
```

That command was not run in this worker because the task allowed one central named gate and the first gate already consumed it.
