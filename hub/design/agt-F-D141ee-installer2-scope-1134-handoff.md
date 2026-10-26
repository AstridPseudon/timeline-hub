# U2 F D141ee installer2 handoff

Disposition is two `(c) DROPPED_BY_OUR_PATCHES_REG` IDs, zero owner-approved retirements, and no behavior PASS claim.

## Owner decision list

1. `tests.test_installer_schema::test_staging_installs_the_npm_locked_schema_before_declaring_services`

   Decide whether the old npm-transitive `@banodoco/timeline-schema/python` staging behavior is still promised. The original test requires that package to exist in the npm lock, be installed as a third pip operation before service declaration, and provide `pyproject.toml`. The supported path instead verifies the Runtime-pinned local canonical JSON schema and performs the ordinary two pip installs. A one-line restoration of the old pip operation is not viable because the current lock has no such package; adding it would reintroduce a second schema source. If the owner chooses preservation, assign a coordinated production/lock/source-of-truth task. If the owner chooses the current D72 path, explicitly approve retirement or replacement of this exact upstream selector; do not infer it from G5 or from the historical migration commit.

   Current replacement selectors, retained as PASS in the schema8 evidence: `tests.test_installer_schema::test_staging_verifies_the_local_schema_before_declaring_services` and `tests.test_installer_schema::test_local_schema_verification_rejects_a_changed_schema`.

2. `tests.test_installer_schema::test_remotion_lock_pins_the_transitive_schema_package`

   Decide whether the old external Composition `v0.0.6` → schema `v0.0.1` graph and exact integrity are still promised. The supported lock deliberately uses the local Composition `0.0.14` artifact and Runtime contract schema digest `4d74a4ae…`; all five old assertions therefore conflict with the approved source map. Preserving them needs coordinated artifact/lock/source ownership changes, not an Agent-only installer repair. If the owner chooses the current D72 path, explicitly approve retirement or replacement of this exact upstream selector; do not infer it from generic C0/G5 language.

   Current replacement selectors, retained as PASS in the schema8 evidence: `tests.test_installer_schema::test_remotion_lock_pins_the_immutable_composition_public_entry` and `tests.test_installer_schema::test_d66_upstream_remotion_lock_pins_the_transitive_schema_package`.

## Required follow-up

If preservation is selected, a manager-owned author must restore the exact pristine bodies from blob `ede759060078ab18a9eac75fd682ddb429073518` under the original IDs and run the targeted installer selector. This worker intentionally did not edit tests or product code. If the current path is selected, record the explicit owner decision before any retirement/adaptation; this report does not grant it.
