# P4 admission cause: Runtime owner handoff

**Diagnosis complete: Runtime admission bug, not invalid canonical seed.** No repository changes or live rerun.

On exact Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`, `runtime_protocol/store.py:6392` treats an omitted occurrence `gain` as null during its field check. The writer (`timeline_commit_store.py:1220`), row verifier (`:550`), service validator (`service.py:2697`) and admission's own sequence check (`store.py:6411`) use unit gain. The schema makes gain optional (`contract/schemas/shot-composition.json:200`).

The real retained NEW8731 realm produces exactly two admission failures: `composition_revision_occurrences / occurrence_field_mismatch / gain`, one for each canonical occurrence. Normal and deep offline inspection agree; all other configured integrity checks pass. Source-file fingerprints are unchanged. The retained accepted canonical document equals the exact original publication/trusted-closure constructors with the authentic 69-byte PNG pin; actual Runtime schema, closure, parent-row and commit-history validation all pass. Two occurrences still share one physical `chapter-shot/shot-1` and `chapter-1/internal-1`.

Owner: **Runtime lane**. Manager independent review, then smallest Runtime correction plus a regression proving omitted gain survives admission and actual stored-gain corruption is rejected. Do not add gain to the fixture, bypass admission or weaken restart. No unchanged-node retry before correction.

Agent base remains `ce4dc2b879a81688b10b870959837bb266ac3f39`; test blob remains `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`. Collection: **1 test**; scoped Ruff, private-cache mypy, diff and clean-tree checks: **PASS**. Available local Ruff/mypy versions differ from repo pins; shared venv lacks those modules. No installs or shared-dependency writes.

Full evidence, exact commands, source lines, limitations and sanitized witness locations: [worker report](../workers/ap2-P4-ten-admission-cause-sol-0622/report.md). Private scratch resolved from worker `tmpdir` metadata: `/tmp/w-b44a409109`. No credentials, keys or raw DB content are included in reports.

P4 behavior after the seed restart remains unverified; this diagnosis does not qualify the original ten-note HTTP node. Diagnosis completed within the 20-minute bound using 45-second command timeouts.
