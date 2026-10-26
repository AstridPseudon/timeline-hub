# U2 F D141ee installer2 independent review

Verdict: `PASS_EVIDENCE` only. This is a source/AST/Git scope review; it is not a behavior PASS, REG0, retirement, or ship claim.

## Exact assigned set

The bound `restoration-manifest.json` has SHA-256 `ebfa4f9def71aa3bf7656a31ea759068bd6946e735f5e007040048c5b61bea2d`, exactly two unique IDs, and zero owner-approved retirements. Both IDs are present in pristine Agent `64197afa297f86f1e738238d5e80aff6d33e303a` blob `ede759060078ab18a9eac75fd682ddb429073518`, and both exact bodies/assertions are restored in review commit `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf` only.

### 1. `tests.test_installer_schema::test_staging_installs_the_npm_locked_schema_before_declaring_services`

- Classification: `c_DROPPED_BY_OUR_PATCHES_REG`.
- Pristine signature: `(tmp_path, monkeypatch)`; exact stripped source SHA-256 `a918238932392fdab15be4cd797092af1d14853e3060a9efab48dfb4d43c60d6`; AST SHA-256 `0912f78626e71ca3a390142a6ad091499db781c2324b22d95d7cad83892ae428`.
- Review-commit location: `tests/test_installer_schema.py:199-283`; the body and protected assertion set match the pristine AST/source after line relocation.
- Every protected assertion is retained: npm `ci` index is before schema pip install and service declaration; declared schema ends with `/a/remotion/node_modules/@banodoco/timeline-schema/python`; the ordinary initial install contains no `timeline-schema`; pip install 0 is the hashed Agent runtime lock; pip install 1 is the four-source no-deps install (`r`, `r/packages/python`, `a`, `v`); pip install 2 is the no-deps schema path install; the profile exists; and the schema `pyproject.toml` exists.
- Current production caller is live `astrid/installer/backend.py`: `Backend.stage` verifies the local canonical schema at `:446`, performs the two ordinary pip installs at `:450-453`, runs `install_remotion_dependencies` at `:461-462`, then declares services at `:463-466`. The current npm lock has no transitive `@banodoco/timeline-schema` package. That source mismatch does not establish retirement.
- Current named candidates are `test_staging_verifies_the_local_schema_before_declaring_services` and `test_local_schema_verification_rejects_a_changed_schema`; retained schema8 evidence records them as passing in its separate review, but this worker did not rerun them and gives no behavior credit. Their assertions are not the original transitive-schema assertions: they require the local canonical path and exactly two pip installs.
- Minimal next scope if preservation is chosen: one manager-owned author restores the exact pristine body under this original ID, then runs this same installer selector. Do not add a third writer or alter the Runtime schema from this review.

### 2. `tests.test_installer_schema::test_remotion_lock_pins_the_transitive_schema_package`

- Classification: `c_DROPPED_BY_OUR_PATCHES_REG`.
- Pristine signature: `()`; exact stripped source SHA-256 `c10befe3af82a12a9bb69c04a7fc919506ac6bef39341576c254b14c99540069`; AST SHA-256 `0eb5098277f634059f80fdc32e72593079ae96b450a2e37473b166ef15fe7bed`.
- Review-commit location: `tests/test_installer_schema.py:286-304`; the body and protected assertion set match the pristine AST/source after line relocation.
- Every protected assertion is retained: the Composition dependency is the external `v0.0.6` archive; Composition depends on the external schema `v0.0.1` archive; the schema version is `0.0.1`; its resolved URL is that exact archive; and its exact SHA-512 integrity is `sha512-m7oUjUV+q1dPb78N6+5B3iayTXkV/WBrQLxNDrlt32j4GXY2sQOIOwpGBw4kNjjngVpSwSaAGneQKUWCgUS8lQ==`.
- Current production/source map is different: `remotion/package.json` uses the local Composition artifact; `remotion/package-lock.json` records Composition `0.0.14` and no schema or theme package; and `runtime.lock.json` maps the Agent local schema to Runtime `contract/schemas/timeline-config.schema.json` with digest `sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`. Agent and Runtime schema bytes independently hash to that same digest.
- Current named candidates are `test_remotion_lock_pins_the_immutable_composition_public_entry` and `test_d66_upstream_remotion_lock_pins_the_transitive_schema_package`; retained schema8 evidence records them as passing in its separate review, but this worker did not rerun them and gives no behavior credit. Their protected assertions are the approved local artifact/Runtime pin and absence of obsolete external references, not the five original external-graph assertions.
- Minimal next scope if preservation is chosen: one manager-owned author restores the exact pristine body under this original ID, then runs this same installer selector. Preserving it would require an owner-directed coordinated artifact/lock/source-of-truth decision; this review authorizes none.

## Disposition and controls

The authoritative D141ee rule is exact per-ID: (a) same body **or** assertions under a new ID plus actual current PASS; (b) owner-approved retirement, with D120 item 5 as the only cited retirement route and none assumed; otherwise (c) patch-dropped and treated as REG. No exact protected assertion set moved to a current candidate, so both IDs are c. D120 retained reports concern App P2 outcomes and do not approve retirement of these Agent installer selectors.

C0 `design/commit-v2.md` remains a Runtime-only writer contract and does not authorize old installer behavior retirement, a second schema source, or separate writers. The supported Runtime path independently resolves through `commitTimeline` → `_execute_timeline_commit` (`runtime_protocol/service.py:2469-2565`) and the registered `timeline_commit_provider` (`runtime_protocol/timeline_commit_provider.py:16-93`). Nothing in this installer review changes that canonical writer or Runtime schema.

No product, test, pin, generated, manifest, profile, environment, child, request, CAS, registry, install, render, or Git/hub/ledger file was changed. No pytest, collection, typecheck, lint, body, service, full suite, browser, or live request run was performed. The private XML cited by earlier work is not claimed as present; only the retained summaries/manifests were used.
