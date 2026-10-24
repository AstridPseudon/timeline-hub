# D72 Installer Review — FAIL

Reviewed candidate `3b61e8ef7825801210d337e20b7574d9745f8636` (tree `208597a67aa1fc4b22b9d0d27eb64555c73b42d4`). Only `tests/test_installer_schema.py` differs from parent.

Findings:

1. `Backend.stage` still installs the obsolete path `@banodoco/timeline-schema/python`, but the approved lock/archive contain no such package. The test masks this by fabricating the directory during mocked `npm ci`.
2. Negative checks do not cover all obsolete theme/schema references in package manifests, archive metadata, or nested lock dependency metadata.

Verified:

- Targeted tests: **49 passed**.
- Composition SRI matches lock: `sha512-Ajl7...Dt65oQ==`.
- Canonical schema digest matches Runtime source: `sha256:4d74...deb3`.
- Ruff target, compile, and diff checks passed.
- Mypy/typecheck-v2 unresolved: requested venv is absent; available environment lacks YAML stubs and has incompatible NumPy stubs.

No product changes made. Evidence: [review-decision.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D72-installer-review-1722/evidence/review-decision.md). `DONE` and commit message were written.