# D141w validation

## Result

The exact tuple, detached/clean state, reviewed builder blob and actual manager admission were rechecked. The placement selector passed its preflight and normal body. Popup ADD was halted as a controller custody failure after two normal request IDs appeared across a lost artifact window; both IDs were stopped with the existing request-stop-test route and waited to terminal `cancelled`. No popup result was credited. Remaining selectors were not dispatched because the shared submit-custody boundary failed.

## Commands and evidence

- `sed -n '1,240p' .../PLAN.md` — PASS; controlling plan read first.
- Exact `git rev-parse HEAD`, `HEAD^{tree}`, detached-symbolic-ref and porcelain checks for all four pin checkouts — PASS.
- `sha256sum /home/user/work/app/scripts/testing/d66-plain-stack.mjs` and blob lookup — PASS; reviewed 49,914-byte builder, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`.
- Genuine Node v20.19.4 with `--import tsx`, all twelve D66 pin fields, target, unique absolute output/plan paths and `--submit` — used for the two dispatched selectors.
- Placement `request-test`/`wait-test` was owned by `--submit`; actual normal ID `...1639-9168` terminal status `pass`.
- Popup preflight terminal status `pass`; first normal ID `...2149-13234` was observed in the controller trace and remained running when the artifact had no normal field. On resume, the same submit artifact created/recorded `...2155-20413`; both existing IDs were stopped via `request-stop-test` and consumed with `wait-test`, terminal `cancelled`.
- Controller traces recorded five-second availability samples; minima stayed above 5.2 GB and the 4-GB stop was never reached.
- `git status --short --branch` in the assigned worktree — clean; no source or test edit.

## Not run

No remaining selector, full suite, retry, alternate route, collector, product repair, registry/queue manual write, or speculative popup diagnostic was run. Popup D141j PASS wording is not applicable because no popup body PASS exists.
