# D141cc custody findings

Verdict: `FAIL_CUSTODY`.

## F-001 — required first-tool sampler was not started by the first tool

The admitted worker's first sampler command failed before writing any trace:

- worker log lines 2017–2021: `mkdir -p .../tmpdir` exited 1 because `tmpdir` was a regular file;
- the sampler command that actually wrote `evidence/disk-trace.txt` appears only in the second attempt at worker log lines 2031–2032.

This is an intrinsic custody miss. The later trace is genuine and starts before source inspection/request creation, but it cannot historically backfill the mandated first-tool coverage. No rerun, source fix, or review loop is authorized.

## Non-findings verified

- Sol1047 dispatch index 1, selector `p2-parent-move@original`, was retained. The parent worker moved only private operational paths (`D66_OUTPUT_DIR`, `D66_SUBMIT_PLAN_PATH`, native stdout/stderr, and its artifact/output directory); the production builder, argv, twelve source-pin environment bindings, registered command/row bytes, and native predicates match the accepted recipe.
- The prepared-only `app-P-D141cc-parent-controller-next` terminal-0 run created no request/body/artifact and is excluded.
- The one native session (59630) produced the authentic preflight and normal IDs; the same normal ID was waited (51172) to terminal pass. No second submit, direct request creation, alternate selector, or retry was found.
- Independent parsing verified the 72-sample author trace, no 4 GB crossing, and the retained sampler's stop signal/result. This does not cure F-001.
