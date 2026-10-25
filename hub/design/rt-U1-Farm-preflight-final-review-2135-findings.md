# U1/D135 final review

Verdict: **FAIL**.

## D135-FINAL-1 (P1): six test-module hashes are recorded but not enforced

`source-manifest.json` records a SHA-256 for each of the six authorized test
modules (`actual_modules`, lines 66-170) and the exact six-file pytest argv.
However, `_manifest_checks()` at `preflight.py:431-458` only parses each file
and compares its top-level import manifest. It never compares the file bytes
to `item["sha256"]`. `_source_checks()` hashes only the separate
`source_files` list, which omits those six test modules. Therefore a Farm
checkout can change a test body while preserving its imports and still pass
the preflight, so the required unchanged-six-test-hashes gate is not enforced.

The frozen object audit independently verified the recorded values: all 21
listed source hashes and all 7 actual-module AST/import manifests pass against
Runtime `0bb3bc45/tree73d925` and Agent `32dde0c0/tree81ad`. This finding is
about the executable check, not the manifest contents.

Required correction: include the seven `actual_modules` paths in the hash
failure aggregation (or make `_manifest_checks()` compare and report their
SHA-256 values) before allowing readiness `PASS`; retain the exact argv and
existing AST/import checks.

No other executable defect was found in this bounded review. Runtime/Agent
source, tests, pins, generated files, live configuration, and Farm kit were
not modified. Actual Farm preflight and the six-file body remain **NOTRUN**.
