Ask: approve ONE execution of the read-only pre-child census, or run it from an approved context; relay to MAIN / Owner: lead (permissions) / By: next Farm slot

F-core-D140 step 1 is STOPPED at a permission prompt. Worker tf-core-D141-census-0137 (second attempt, exit 0, BLOCKED; first attempt tf-core-D141-census-0130 stopped on `command -v node`, also an approval prompt). No census output exists; nothing was worked around.

Exact command refused (first stderr "This command requires approval"), run in two forms:
1. env D140_PHASE=pre-child AGENT_CHECKOUT=/home/user/work/wt/agt-pin-28e56cac RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-6a011d58 APP_CHECKOUT=/home/user/work/wt/app-pin-867cb273 COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-635f4de0 MAKER_PATH=... RECEIVED_MAKER=... WRAPPER_PATH=... NORMAL_REQUEST_ROUTE=... CHECKER_PATH=... IMPORT_CHECK_ROUTE=... FARM_ORCH_ROOT=... FARM_CURRENT_{AGENT,RUNTIME,APP,COMPOSITION}_RECEIPT[_SHA256]=... D73_LAUNCHER=... NODE_BIN=... /home/user/work/wt/vw-pin-1b709a79/ops-d140-farm/receive-farm.sh --check-only
2. the same exports in a runner script, run as `bash <runner>`.
The full assignment list is in workers/tf-core-D141-census-0137/evidence/bindings.md. Farm did not try other forms and will not.

What the census needs: it is read-only, expected exit 1 NOT_READY, and prints the complete missing-prerequisite packet. Please either (a) approve one execution of `.../ops-d140-farm/receive-farm.sh --check-only` with the bindings above (I can re-dispatch a worker for it), or (b) run it yourself in an approved context and give Farm census.out, or (c) tell Farm which other command form is approved.

Verified by the worker (all fine): five checkouts clean at the frozen HEAD/tree (Agent 28e56cac / 2ebe2ddf, Runtime 6a011d58 / ac5b8627, App 867cb273 / 2b44a46c, Composition 635f4de0 / 5ab5191a, receiver 1b709a79 / 040c1772); four receipt SHA256s recomputed and equal; kit hashes fd83c9e2 / 60d2238a / 8215f5d9; D73 launcher present, 8487 bytes, sha 9f668e39 equals the script pin; Node 43d6cf63; disk 9.98 GB.

Predicted (not census output) unbound: installed-kit summary and installation, KIT_SOURCE_CHECKOUT, D139a schema set (distribution, RECORD closure, direct_url, trusted manifest), DEPENDENCY_SEED, central service/suite, dry and core routes, DISK_ADMISSION, RETAINED_ROOT, PROFILE. The Composition receipt filename has 39 hex chars (the request used a short SHA); the receiver may reject it, which the census will show.

No child request, no tests, no core, nothing created or deleted.
