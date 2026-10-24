## A3 popup ADD diagnosis

- **Run:** P2 `...13583`, terminal `3 failed / 5 NOTRUN`, 405s.
- **Trace:** [trace.zip](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-readiness-D45-final-caller-sol-0446-full-e2e-three-products-1024045333-13583/playwright-output/three-products.p2-popup-P2-ae6fa-currence-fork-and-A2-commit/trace.zip), SHA256 `b6bcddfa13da1660743bc72e25f69841c6c9d57d161d417302d150c16c36de1c`.
- Source custody: App `c0fe88994405…`, tree `8e3ef15ee5…`; Agent `079580ca46af…`; Runtime `37eb6c7bdb79…`.

### Causal result

The mounted UI selected occurrence `f2-occurrence-copy`, raw child `f2-agent-clip`, then used the existing A2 outbox. The request contained:

- `occurrence.fork`, followed by `occurrence.add-media`;
- one step covering command ordinals `[0, 1]`;
- authenticated media import/selection;
- ADD row `clip-0`, `at: 0`, `clipType: hold`, `hold: 5`, `opacity: 1`, **`track: V3`**.

The authoritative child closure contained only visual tracks `plate` and **`V2`**. No `V3` existed. Runtime/Agent therefore correctly returned HTTP 422:

- `code`: `validation_error`
- `details.code/reason`: `invalid_edit_command`
- `details.path`: `["commands"]`
- message: `media edit requires an active raw visual child track`

No accepted canonical response or authoritative post-execution records exist because validation stopped before execution.

Verdict: **product emitter defect, high certainty.** The generic prepared-media planner moved the ADD from occupied `V2` to a newly-created `V3`; occurrence-scoped ADD requires an existing active raw visual child track. The bounded A3 repair is to preserve the captured raw visual track for popup ADD and disable nearest-free/new-track fallback, with local refusal if no valid raw track exists.

The extra `created` entries are separate: they are C0-authorized and explicitly emitted by A3’s creation-claim fix. The original P2 assertion at [line 464](/home/user/work/wt/app-P2-D45-popup-shape-0505/tests/e2e/local/three-products.p2-popup.spec.ts:464) omits them, so Proof would need an independent no-weakening oracle decision. I did not alter it.

### Verification

- `git diff --check` — PASS
- `git status --porcelain=v1 --untracked-files=all` — clean
- `unzip -t trace.zip` — PASS
- No tests, browser, backend, service, or full suite run per task instructions.
- No source or test files changed. Commit message and `DONE` marker written.