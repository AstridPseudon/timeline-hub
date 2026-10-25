# D141 Runtime full/pristine route candidate

This directory is a private candidate for the existing Runtime test service.
It contains no live registry entry and does not alter product, test, config,
dependency, checkout, Store, or service files.

`route-config.json` binds Runtime cut `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`
and pristine Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2`; both Agent
bindings are intentionally pending. `route.py status` therefore reports
`NOT_READY`. A reviewed controller handoff must populate actual Agent commit,
tree, checkout, receipt, provider/client origins, and lock values before
rendering or CAS-installing the two rows.

The rendered rows preserve the normal Runtime command (`python -m pytest -q
-n3`) and add only durable JUnit output. The service supplies `D66_OUTPUT_DIR`.
`receive.py` accepts a completed service output only when the raw exit, log,
JUnit, and KEEP witness are present.
