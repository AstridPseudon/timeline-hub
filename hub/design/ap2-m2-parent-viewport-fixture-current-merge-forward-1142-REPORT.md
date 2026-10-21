# App2 parent viewport fixture merge-forward report

## Result

Merged forward only the reviewed parent fixture delta from donor `6707a30f14bf3a5ee19cb9e481b7dbd95b77522a` onto HOME `92c30b570cf8105dc021a64874c258e6c950b841`.

The worktree result is HOME plus one reviewed file:

- `tests/e2e/local/three-products.spec.ts`: 36 insertions, 3 deletions.
- No production source changed.
- No other HOME file changed.
- The fixture blob is exactly donor/source blob `e612c18cac2a651e855e75388498762f034dc63a`.

The applied fixture delta contains only the existing UI `Zoom out timeline` preparation and measured geometry assertions, plus the already-reviewed strict full-404 response body. Existing manual-drop behavior and assertions remain intact: original manual title, V1 target, pointer 22.5, left edge 20, raw/order/ACK handling, retry, restart, undo, opaque data, and zero legacy writes.

## Identity

- merge parent recorded for harness: `92c30b570cf8105dc021a64874c258e6c950b841`
- HOME tree: `c34d65b66481fd0015279451b175c53b7b5e8f4f`
- donor/source commit: `6707a30f14bf3a5ee19cb9e481b7dbd95b77522a`
- donor/source tree: `6ff32d797f0e774b8574274a3494ce8755fa160c`
- donor/source fixture blob: `e612c18cac2a651e855e75388498762f034dc63a`
- common base: `0cc2583aaf07e89190b9344b5ac82849d6279586`
- harness final merge commit/tree: pending harness commit

Custody checks passed:

- donor fixture blob compares byte-for-byte with the worktree fixture;
- HOME comparison outside the fixture reports zero changed files;
- merged diff reports one file only, 36 additions and 3 deletions;
- preserved marker inventory includes strict `not_found` and exact refusal message, V1, 20s, 22.5, retry key/body, inverse undo posts, and `wire.legacy === []`.

## Tests and checks

- `git diff --check` — PASS.
- `./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0` — PASS, exit 0.
- `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/tmp ./node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts:1410 --list` — PASS; exactly 1 test listed with the original manual-drop title.
- No browser execution, build, socket/service run, actual journey, central suite, or full suite was run.

## Remote-merge-ready packet

Ready for source-packet review and the manager's remote merge request. The harness must commit this resolved tree while retaining merge parent `92c30b570cf8105dc021a64874c258e6c950b841`; the resulting commit/tree are intentionally not claimed here. This is fixture readiness only, not ADD proof/cut or a live execution claim.

