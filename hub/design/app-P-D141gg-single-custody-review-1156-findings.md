# Findings

## CUSTODY-RAW-KEEP — blocking

The manager’s prospective receipt records `preexisting_keep: false` for both genuine result IDs and adds their raw KEEP files at `2026-10-26T11:49:29.082850Z`. The preflight was requested at 11:46:56Z, the normal request at 11:47:26Z, the body began at 11:47:38Z, and the normal body ended at 11:51:50Z. Therefore the raw marker was not present from first durable ID custody or body start. The author-local worker KEEP and evidence KEEP do not protect the native `tests/<ID>` raw result. This is an actual marker gap, not backfilled evidence.

## CUSTODY-RECIPE-PATH — disclosed deviation

The immutable accepted prep packet is `bdf548ac...f194e`. The author packet is `e6b63540...fd85`. An exact sorted JSON comparison found differences only in `D66_OUTPUT_DIR`, `D66_SUBMIT_PLAN_PATH`, and the five `paths` entries (`output`, `plan`, `lock`, `stdout`, `stderr`): each moved from the prep worker root to the author controller root. Selector, attempt suffix, suites, rows, command hashes, row hashes, argv, cwd, operational environment, unset keys, and all four source tuples are equal. The native run is associated with the genuine result IDs and pinned sources, but the explicit no-relocation requirement was not followed.

## PASS-RESULT — not a custody clearance

The authenticated normal result `...-24271` has status `pass`, exit `0`, and same-ID wait exit `0`. Its XML has exactly one readiness test and one original single-transition test, with zero failures/skips/errors. The exact source predicate covers the v2 request, raw property removal, opaque data and order conservation, reload, guarded inverse/Undo, authoritative history, and zero old-route writes. This behavioral PASS does not cure CUSTODY-RAW-KEEP.

## TRACE LIMITS

The native trace has 54 actual samples, min `5029826560`, max `5477560320`, max gap `5.006048s`, and no 4 GB stop. The author controller trace has 158 `/dev/vda` rows, min `5029302272`, max `5479276544`; it is only that sampler session and supplies no inferred historical coverage. The body went below the 5.2 GB admission floor after admission but remained above the 4 GB stop line.
