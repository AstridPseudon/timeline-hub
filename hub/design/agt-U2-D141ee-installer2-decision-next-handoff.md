# U2 D141ee installer2 handoff

The harness may commit the single-file test change with the supplied commit message. The change retires exactly two owner-approved obsolete npm-schema installer expectations:

1. `tests/test_installer_schema.py::test_staging_installs_the_npm_locked_schema_before_declaring_services`
2. `tests/test_installer_schema.py::test_remotion_lock_pins_the_transitive_schema_package`

Owner quote, verbatim, for each ID: “I approve retiring exactly the two npm-schema installer test IDs listed in escalations/agent-20261026T1158Z-D141ee-final55-owner-scope.md, ledgered with this quote; replacement controls stay.” Date: `2026-10-26`.

The exact current supported caller/control chain is `Backend.stage` → `_verify_local_timeline_schema` (Runtime-pinned canonical schema) → ordinary Python installs → locked local Composition dependency staging → service declaration. The retained replacement selectors passed in the final 4-test run. Runtime remains the sole film writer; no contract, endpoint, force, cache/hook/trust, schema, lock, generated client, or product behavior changed.

Evidence files include the AST/collection conservation result, final JUnit XML, per-ID dispositions, source manifest, disk trace, and manager-ledger entries. No full or browser suite was run because the task required the targeted same-kind run only.
