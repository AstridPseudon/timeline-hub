# P2 D141gg single-scope-2 custody review

Verdict: **FAIL_CUSTODY**.

The explicitly authorized new `p2-transition-none-single` / `single-scope-2` body itself passed: preflight `...-9320` PASS, normal `...-24271` PASS exit 0, and same-ID `wait-test` exit 0. The original test XML contains one readiness pass and one exact P2 single-transition test pass, with zero failures/skips/errors. The source test asserts the v2 `doc.patch` remove of `transition`, raw absence after the edit, preservation of opaque parent data and clip order, exact request/reply/history metadata, reload, guarded Undo restoration, and zero legacy writes.

## Findings

1. **CUSTODY-RAW-KEEP (blocking):** the genuine raw test-directory KEEP markers were absent when the IDs were created and when the body ran. The manager added both markers prospectively at `2026-10-26T11:49:29.082850Z`, after the preflight, normal request, and body start. The author’s worker-local KEEP/evidence KEEP is not native raw-test protection. No retroactive first-tool or full-run marker claim is made.
2. **CUSTODY-RECIPE-PATH (non-behavioral deviation):** the author’s private packet and future artifact paths were relocated from the accepted prep packet’s `single-scope-prep-1137` root to the author’s `single-scoped-controller-1145` root, despite the no-relocation instruction. A full JSON diff found no other value change: selector, argv, cwd, environment/unset keys, operational environment, four source pins/checkouts, command hashes, row hashes, and suite/predicate inputs match. The actual native association is genuine, but the relocation is disclosed and not silently blessed or repaired.

Native body disk trace: 54 samples, minimum available `5029826560` bytes, maximum `5477560320`, maximum interval `5.006048s`, and no 4 GB stop. Author controller trace: 158 `/dev/vda` rows, minimum `5029302272`, maximum `5479276544`; it is session-only coverage. The body crossed below the 5.2 GB admission floor after admission but remained above the 4 GB stop line.

No product, source, pin, generated file, registry, queue, kit, hub, or Git metadata was changed. No test, typecheck, lint, browser, service, or body was rerun.
