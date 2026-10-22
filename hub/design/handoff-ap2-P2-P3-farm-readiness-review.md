# Flat review: App P2/P3 farm handoff — FAIL

Verdict: **FAIL; no P2/P3 acceptance credit.** The handoff is a useful v1/native inventory, but it is not a v2 farm-ready review. The two blocking issues are:

1. It recommends strict expected-to-fail markers for the original snapshot tests (handoff line 32). That violates the current hard rule: preserve successful behavior through migration; do not add skips/xfails or rewrite tests to expect refusal. Those journeys must be migrated as passing tests.
2. It does not identify the v2 status/schema break. The current App DTO/helper/tests still use `rebased` and omit v2 `steps`, `merge`, and `reads`; the approved contract requires new v2 disjoint-head success `merged`, complete step metadata, and authoritative history fields. Current helper existence and current v1 native cases are not v2 execution evidence.

Additional required corrections:

- Require exact history assertions for `label`, `steps`/patches/ordinals, requested/effective merge mode, reads, authoritative publisher, `records.commands`, `records.steps`, and inverse `undo_steps`/`undo_of`, in addition to `intent`, `records`, and `receipt.command_kind`.
- Keep the two-source proof linked by publication IDs: network `COMMITS` POST interval plus Runtime `/commits` history interval. Use the pinned/cursor-safe history result.
- State that Gate 5’s initial reset is fixture normalization; the adversarial sequence begins with A and remains App A → Agent C → lost ACK → dependent B → reload → Runtime restart → exact A retry → B recovery → guarded undo.
- Treat the listed operation/selector rows as v1/native baseline until A2/A3/R2/Runtime integration supplies v2 command metadata and the missing popup `clip.swap-media` journey. The current `e2e-m1-gesture` selector lists only three tests and is not P2-only; no named P2/P3 suite exists in `tests/suites.conf`.

Evidence: static review only. `npx playwright ... --list` listed 14 tests in 2 files; `--grep 'M1 real' --list` listed 3. No browser, socket, Runtime, Agent, farm, full, or acceptance suite was run. Typecheck/lint were not applicable to this zero-source-delta review.
