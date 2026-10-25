Resolved the contradiction at base `913686448cafbb63dfba5d8053cb725e1140bb07`. All repository product/test files remain unchanged.

The earlier GREEN geometry control asserted **requested** V2, without checking the resolved target. The existing mounted A2 control mocked the coordinator as V2/4.5s, bypassing the failure.

Retained DOM confirms correct helper geometry:

| Input | Retained value |
|---|---:|
| V2 anchor/reference left | 240px / 336px |
| Anchor/reference time | 3s / 6s |
| Scale | 32px/s |
| Label offset / row height | 144px / 36px |
| Normalized pointer | X368 / Y54 |

The helper correctly requests 4.5s. The five-second preview overlaps V2’s clips at 3–6s and 6–9s. Generic snapping allows only `8/32 = 0.25s`, so the coordinator requests a new track, producing **V3/4.5s**. The strict oracle independently uses existing asset-placement snapping, which resolves **V2/9s**. The retained request confirms V3/4.5s and HTTP **422**.

Absolute bounding-box results were not retained. The witness uses stable relative DOM geometry across three snapshots; translation/zoom/scroll controls confirm the mapping without inventing absolute coordinates.

The review-only proposal carries the valid managed row hit through `DropPosition.pointerTrackId`. Single managed image imports then settle through the existing asset planner on that row. Generic drag snapping remains unchanged.

- [Product patch](/tmp/w-3b214318e2/proposal.patch): `drop-position.ts`, `external-drop-utils.ts`.
- [Combined application/review patch](/tmp/w-3b214318e2/review.patch): product proposal plus the existing mounted suite using the real coordinator.
- [Geometry witness](/tmp/w-3b214318e2/geometry-witness.json).

Exact verification commands:

```bash
python "$TMPDIR/extract-witness.py"
python "$TMPDIR/prepare-controls.py"

PROPOSAL=old TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx node_modules/vitest/vitest.mjs run --config "$TMPDIR/controls.config.ts" --configLoader runner --no-cache --maxWorkers 1
PROPOSAL=new TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx node_modules/vitest/vitest.mjs run --config "$TMPDIR/controls.config.ts" --configLoader runner --no-cache --maxWorkers 1

/opt/node20/bin/node --max-old-space-size=4096 "$TMPDIR/typecheck.cjs"

/opt/node20/bin/node node_modules/eslint/bin/eslint.js --stdin --stdin-filename src/tools/video-editor/lib/drop-position.ts --max-warnings 0 < "$TMPDIR/drop-position.ts"
/opt/node20/bin/node node_modules/eslint/bin/eslint.js --stdin --stdin-filename src/tools/video-editor/lib/external-drop-utils.ts --max-warnings 0 < "$TMPDIR/external-drop-utils.ts"

git apply --check "$TMPDIR/review.patch"
git diff --check
git diff --exit-code -- src tests
```

Results: **old RED: 5 failed, 93 passed; proposal GREEN: 98/98 passed**. App/Node typechecks with private source overlays, both lint checks, patch applicability, and unchanged-source checks passed. Controls cover stale occurrence/row refusal, explicit new-row boundaries, and wrong/missing/ambiguous measurement references and siblings. Measurement guards do not establish general stale-sibling protection.

Protected spec SHA-256 remains:

`67976926ae233805e3ed8d7e220eaa1bf92d30fb807fd14595f5d0daaee43a2a`

No browser, service, build, full suite, or installation ran. No acceptance, canonical-result, reload, or Undo credit is claimed. Generic hover-preview consistency remains unverified.

Nothing blocks this source investigation. Recommend unified application/review through existing owner **0064**, with App A3 ownership assigned for the two product files. `commit-msg` and empty `DONE` are written.