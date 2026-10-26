# Owner decision, typed by the owner in the main session (12:50 UTC, 26 Oct), verbatim

"I agree My recommendations, all in one place:
1. Inverse, 38 tests: A. Put back the upstream module our 19 Oct commit deleted.
2. Installer, 2 tests: A. Retire the two tests for the old npm package, and keep ours.
3. Writers, 15 tests: A. Migrate them to the commit path, keeping their checks, with `force` still refused.
4. App's upstream target: the latest upstream, with one catch-up merge first. That costs about 1–2 hours, and the shot-layering plan builds on it.
5. Shot-layering plan: start read-only prep on Farm now, and build the release after the ZIP lands."

Scope (main, D141ii):
- (1) applies to the exact 38 inverse IDs and to astrid/core/timeline/inverses.py, deleted by our commit fc33e0e76c.
- (2) applies to exactly these two IDs:
  - tests/test_installer_schema.py::test_staging_installs_the_npm_locked_schema_before_declaring_services
  - tests/test_installer_schema.py::test_remotion_lock_pins_the_transitive_schema_package
- (3) applies to the exact 15 writer IDs in escalations/agent-20261026T1158Z-D141ee-final55-owner-scope.md.
