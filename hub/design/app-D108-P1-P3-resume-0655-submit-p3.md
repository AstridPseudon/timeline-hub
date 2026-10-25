# D108 P3 submit

- Existing D66 API submitted one source-preflight then one original body serially; no prior P3 plan/request existed and no duplicate was made.
- Preflight `app-pin-f7201e02-d108-p3-current-0655-preflight-1025065907-15346`: PASS, exit 0, 3s. It verified the exact four pins, detached clean checkouts, prepared recipes, and a one-parent App service snapshot.
- Original `app-pin-f7201e02-d108-p3-current-0655-1025065937-31792`: queued/running under the same captured tuple; only this ID may be waited/resumed.
- Counts are readiness 1 and original P3 1. Required P3 source SHA is `93c2bf4c72ac…a64b`; readiness source SHA is `2b9723db2629…1593`.
- P3 predicates remain unchanged: both recovery mounts, exact five observed/three forwarded requests, strict request/body/key/origin/order checks, merged-B recorder shape, authenticated history/canonical document, restart, and guarded undo.
