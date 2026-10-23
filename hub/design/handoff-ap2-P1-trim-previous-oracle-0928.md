# P1 trim previous-value oracle — handoff

Status: PASS, scoped test-only correction ready for independent review.

Base `94b19e363047c1446608ff42ee11b0f34c906c69`; original spec reference
SHA-256 `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`.
Changed path only:
`tests/e2e/local/three-products.p1-chain.spec.ts`.
Corrected spec SHA-256:
`06104227304e7bab77e8f3f2de131ef26a949db437d02c2b2d7e20a25c057518`.

The old `trimChange` guard expected `before.value: SPLIT_AT` (`2`). The seed
authors `from: 0`, and the unchanged split assertions preserve the new right
clip via `...originalClip`, so the accepted raw source start is `0`. The single
expression now explicitly expects `before.value: 0`. This makes the guard
truthful without changing the split, trim value, IDs, reads, requests/replies,
merged/refused paths, restart/rollback behavior, or any other assertion.

Checks passed:

- Playwright `--list`: exactly 2 original P1 tests in 1 file.
- Scoped ESLint: pass.
- Root, App (180-second allowance), and Node TypeScript checks: pass.
- `git diff --check`: pass; diff is exactly 1 file, 1 insertion and 1 deletion.
- Composition artifact SHA-256:
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Normal Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc` and Agent
  `f894c3c9dda25ab03527eeb7f52da5da31d627c1` were read-only and clean.

No original chain execution or behavioral pass is claimed. No browser, HTTP,
socket, service, build, full suite, product/helper/fixture/schema/pin/lock/
package/ops/shared-install change was made. Independent no-weakening review is
required before acceptance of this current test-only port.
