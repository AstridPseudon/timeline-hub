# D141 handoff

Both requested full runs are terminal and raw outputs are retained:

- Normal: `app-full-1026004326-12174`, FAIL exit 1, 5 Vitest files / 33 tests failed; Node NOTRUN.
- Pristine receiver: `app-D141-pristine-receiver-0007-full-1026010029-23581`, FAIL exit 1, 3 Vitest files / 18 tests failed; Node NOTRUN.

The normal run is applicable to the exact final integrated App head/tree. The pristine snapshot has the exact frozen tree and required commit as parent, but the service-created synthetic HEAD is not the required frozen commit; the service removed the snapshot after completion. This is an evidence seam, not a silently accepted exact-source proof.

No normal/pristine failure root matched. Per D141 rules, no REG or nonREG verdict is claimed; all eight actual roots are UNKNOWN. No same-kind rerun was made because no environment-type failure was established and the brief forbids broadening the body. See `reg-diff.json` for root-by-root classification and `normal-result.json` / `pristine-result.json` for exact failure names.

Recommended next step: have the existing pristine receiver preserve or report the exact frozen commit identity at postflight (without changing the suite), then decide whether a comparator rerun is warranted. Do not use the live `banodoco/reigh-app` checkout as a substitute.
