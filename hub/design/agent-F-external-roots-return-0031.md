Implemented in [generic_host.py](/home/user/work/wt/agt-F-external-roots-return-0031/astrid/core/execution/generic_host.py:4285) and focused tests.

- Bound installed external execution to Runtime-held source inventory identity.
- Rejected foreign/recomputed roots, changed sources, symlinks, package collisions, and caller admission tampering before launch.
- Added installed child `-I` isolation.
- Added real managed-source positive coverage and reviewer attack regressions.

Tests:

- Focused/security: 33 passed.
- Source setup neighbor: 8 passed.
- Ruff test file: passed; production diagnostics unchanged at 101.
- Mypy diagnostics unchanged from parent: 139 vs 139.
- Broader V3: 155 passed, 60 failed due sandbox lacking installed `runtime_protocol` under isolated `-I`; 51 deselected.

Actual installed subprocess positive remains pending because the qualified installed Agent/Runtime pair is unavailable in this sandbox. Commit message and `DONE` marker were created.