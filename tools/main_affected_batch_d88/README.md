# D88 incremental MAIN affected-node preparation

This is a source-only overlay on the exact committed D86 251-row route. The D86 route and its 299-record remainder remain preserved under `tools/main_affected_batch_d86/`.

The proposed selector set is a lossless union of the 227 non-retired original rows and four reviewed source additions: current sheet 17, M2 placement 20, M2 pool 6, and inverse-stage 7. The 24 D87-retired native-batch rows plus its separately mapped checkout case are recorded in `retired-d87.tsv`, excluded from READY and not moved into the visible 299-record remainder. Held/failed families are listed in `held-not-ready.tsv`.

This overlay is not runnable yet. The exact incremental membership response, fresh four-repository D73 checkout receipts, path-sensitive source hashes, normal qualified profile, and parsed-command preflight are pending. The recipe retains `-n 3`, `--timeout=45`, and `-m integration`, but manager release is required before any body. No pytest collection, service, install, build, or submit was performed.

D88 remains `UNKNOWN_NEEDS_LIVE_ACTIVATION`: `d88-capture-plan.json` records the existing Runtime helper, the 5-second watchdog/30-second follow-up and two-capture cap, the actual caller/bootstrap trace requirement, and the fields that stay UNKNOWN until one authentic producer is captured.
