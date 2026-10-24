## D72 whole-path report

- No product or test files changed; worktree remains clean.
- DONE marker and commit message written.

### Verdict

- Installer local-canonical-schema conclusion: **PASS**.
- Whole production host path: **FAIL**.
- Attribution: **distinct genuine schema migration need**, pre-existing on current integration—not correction-caused. D67’s installed-input gap is only a comparator, not proof of this seam.

### Evidence

- `Backend.stage` verifies the Runtime-pinned local JSON digest (`sha256:4d74…deb3`) at [backend.py:173](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/installer/backend.py:173), then installs only Runtime/Agent/VibeComfy packages at [backend.py:404](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/installer/backend.py:404) and records the source/profile at [backend.py:423](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/installer/backend.py:423).
- The service declaration passes the installed source and Python, but no schema environment: [services.py:43](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/services.py:43).
- Host bootstrap derives `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` only from `remotion/node_modules/@banodoco/timeline-schema/python`: [host_bootstrap.py:485](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/sdk/host_bootstrap.py:485).
- Strict validation requires that external Python package and imports its models/functions, not merely the local JSON: [remotion_runtime.py:71](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/core/rendering/remotion_runtime.py:71), [remotion_runtime.py:346](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/core/rendering/remotion_runtime.py:346).
- Actual production callers are generic-host preflight at [generic_host.py:6496](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/core/execution/generic_host.py:6496) and worker validation at [generic_host.py:8101](/home/user/work/wt/rt-D72-installer-whole-path-1738/astrid/core/execution/generic_host.py:8101).

Current integration’s lock/archive contain only the local Composition artifact; no external schema/theme packages. Upstream924 did contain those external packages. The pre-correction integration still had the obsolete stage install, so b4 did not remove a previously working current path.

### Tests/diagnostics

- Reused unchanged finite comparator XML: **50 tests, 0 failures, 0 errors** (`review.xml`, SHA-256 `65af4585fa2dbac607a01a841ea3afd049a901f805b3c1672888189f035aa923`).
- Local schema digest equals `runtime.lock.json` pin: **PASS**.
- Strict schema probe with existing external Python package: **rc 0**.
- Same probe pointed at checked-in JSON-schema directory: **rc 1**, trusted-origin rejection. This proves JSON is not equivalent to the required Python distribution.

No installed host, network, acquisition, or rendering run was performed.

### Recommended next step

Make a separate migration decision: define an approved, guarded source for the strict Python schema model, or prove and implement a local-JSON-compatible host consumer. D72’s installer integrity correction alone cannot satisfy that runtime contract.