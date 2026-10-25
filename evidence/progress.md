# Progress

- Read PLAN and the permanent author packet, including the D104/D120 context.
- Verified one-file candidate scope, unchanged ordinary fixture, preserved
  assertions/predicates, normal daemon/provider startup, and authenticated
  AstridClient setup.
- Source checks passed: Python 3.11 compile, Ruff, scoped mypy, and diff
  check.
- Did not rerun unchanged pure/ordinary cases.
- Central prior targeted run was correctly classified as five deselected
  integration nodes, not functional proof.
- One permitted live integration remains unverified because the central
  service lacks an exact-selector suite bound to `rt-pin-ab1e4f61`; no
  alternate runtime, local daemon, retry, or transfer was used.
