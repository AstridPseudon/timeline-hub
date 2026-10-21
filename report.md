## Report

- Diagnosed the initial `config.app` order: Runtime authoritative storage and
  receipt/reload use sorted-key canonical JSON, so the old `before, target,
  after` fixture could not read back in that order. This is not normal API
  data loss.
- Applied the permitted setup-only correction in
  `tests/test_timeline_owned_reference_integration.py`: target remains
  `com.example.compiler-canary`; siblings map `before -> a-before` and
  `after -> z-after`, with all corresponding exact map/order and
  `insertion_order` assertions updated. Null/opaque values and all semantic
  remove/retry/receipt/no-duplicate/restart/inverse/redo assertions remain.
- Complete preflight passed: Runtime42a producer bytes/all 15 lock entries,
  all 76 artifacts, schema 65/37 and exact digests, 0.2.17/import/profile,
  shared dependency read-only checks, temp/disk, syntax/diff checks, 1-test
  collection, and complete fixture setup closure.
- Exact preflight collection command: `env
  ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad
  PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad"
  PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q
  -p no:cacheprovider --collect-only -m integration
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo`
  → `1 test collected`.
- Earlier unchanged-tree setup failures were ordered `27437` and RT03
  `11493`; corrected fixture-registration run `30759` reached the old order
  assertion and established the canonical-readback witness used here.
- One authorized central ordered run only:
  `rt-m2-private017-initial-order-diagnosis-1015-private017-agent6c-integration-1021101825-7616`
  (snapshot tree `02d77ba52097cba031b16aa2f183236b52472cf0`)
  → `1 failed in 1.51s`, first failure at line 284 because the normal Agent
  recorder enriches the accepted command with capture fields and the test
  compares it to the raw command. No auto-retry and no RT03 run.
- Remove, restart/exact retry, inverse, and redo behavior remains unverified;
  no qualification/adoption claim is made. No product source or immutable42a
  artifact/pin was changed.

See [the detailed diagnosis](design/runtime-private017-initial-order-diagnosis-1015.md)
for the source trace, literal key mapping, preflight identities, and exact
central result.
