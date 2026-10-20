# Runtime shell/native init final qualification

## Verdict

QUALIFIED for the bounded Runtime native-init cohort on the composed current
source. The approved same-ID repair for genuinely empty shells with an absent
or null parent head, plus the strict duplicate/invalid legacy JSON refusal,
passes the original real-client/provider create/init/restart/undo/retry cohort.
No positive behavior was rewritten as a denial, and no public release, pin,
publication, ZIP, merge, or full suite was performed.

## Exact sources and private artifacts

- Current integration source: Runtime `129493b2aff614560d9b7ac2577957e799cf30ec`, tree
  `330ea3969cb9cce77271404f31793c21abd5993f`.
- Exact shell repair: `0e49e0228f5977b5a8b2b17b7f017a91b40eaf2d`, tree
  `d97b20693d801f6b7889867620f2b51856521147`.
- Exact strict parser repair: `ff9d5c17bc75fb12b3293690a8d9acd8eded0db2`, final
  tree `6c380bb36bb7e398613c238bb1a442502de67c78`.
- The two `129493b` transport-test files are carried unchanged in behavior:
  `tests/fixtures/operation-handle-live.mjs` is exact, while
  `tests/test_operation_handle_integration.py` has only fixture-registration
  aliases added so the inherited test passes Ruff without changing assertions.
- Approved Agent source: commit `487ca1e0d74edf4aecdd2b4e045294ab089fc273`,
  tree `c7033d9e5a8a859cba1e2bed2393e66af85a6505`, archive SHA-256
  `d8bd76ac1c2fa8feb9b2da87f622b2e23779b7a8beb28167013131bf6dce8807`.
- Approved raw schema:
  `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
  `e29c4542a79e5c2098251ac3ff80a47883d08878b79592aa920f1e3321274159`.
  The private Runtime copy is byte-identical.
- Private contract is version `0.2.14`, schema/contract digest
  `e6c4228e5d4d643b236f0dbdb22a9b34fbd0953dbfcbd86da0aca06c4ab07af7`.
  It retains the full S2 floor (48 definitions / 22 operations) and adds only
  the approved `timeline.init` operation (49 / 23); no new operation was
  invented here.
- Private artifact version:
  `sha256:22e2729bcb626f0f7320bfe7e995b8db90c43b8cce159fe2bb2720734450b8e7`;
  `contract/artifacts.json` raw SHA-256
  `cdb6943f497c83a74e5a1fba0ddb88f3ebc44e00b89139dc6f631bae47e9e0d8`.
- The private artifact/source overlay was built under
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-shell-native-final-qualification/runtime-private`
  from the current snapshot and the prior frozen normal-generated archive;
  shared dependencies remained read-only.

## Central test evidence

The final central snapshot tree was `beed2563247497702dcf46da7146d216d6432647`.

- Exact native/init cohort: request
  `rt-m2-shell-native-final-qualification-targeted-1020125840-9634`;
  wrapper passed and its private child suite reported **23 passed in 18.88s**.
  This includes all 15 original init cases with `--runxfail`, the formerly
  missing genuinely-empty NO-HEAD same-ID success, absent/null-head repair,
  restart, undo, retry, later edit/undo guards, strict hidden/corrupt refusal,
  complete authored App defaults/order/name/slug, the authenticated generated
  client Door case, and the historical-slot provider neighbor.
- Separate nine-case commit lane: request
  `rt-m2-shell-native-final-qualification-commit-integration-1020125919-4513`;
  **9 passed in 12.50s**. These were not duplicated in the native/init launcher.
- Current `129493b` transport neighbor: request
  `rt-m2-shell-native-final-qualification-targeted-1020125806-22068`;
  wrapper passed. Its underlying `test_operation_handle_integration.py`
  contains and ran the three integration cases (two lost-ack wait modes and
  credential/scope refusal).
- The exact 32-node union was collected with exit 0; node IDs are retained in
  `workers/rt-m2-shell-native-final-qualification/test-ids.txt`.

## Local evidence

- Shell/strict-parser neighbors:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_empty_shell_repair.py tests/test_timeline_headless_overwrite_refused.py tests/test_timeline_commit_baseline.py tests/test_timeline_commit_port.py tests/test_timeline_projection_occupancy.py -k 'not actual_provider_historical'`
  -> **169 passed, 1 deselected**.
- Private non-Door native/init cohort with `--runxfail` -> **21 passed, 1
  deselected**.
- Private current-union contract -> **73 passed**.
- Private normal generation `generators/generate.py --check` -> exit 0.
- Private artifact manifest `scripts/artifact_manifest.py --check` -> exit 0.
- Private Ruff checks -> all checks passed; `git diff --check` -> exit 0.

## Setup notes and limits

The first direct central targeted request for the transport file selected no
integration tests under the repository's default marker policy (3 deselected,
exit 5). The explicit launcher then initially found the default missing
`/home/user/work/wt/astrid` checkout. Both were fixed only in test setup: the
launcher selects `-m integration` and points `ASTRID_CHECKOUT` at the retained
approved Agent source. The final wrapper passed; no runtime assertion or
product behavior was weakened.

No full/full-nightly suite, App browser journey, public schema freeze, public
pin, merge, publication, ZIP, or Agent/App edit was run. Those are outside
this qualification brief.
