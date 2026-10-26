# D141u handoff

Repair: restore the detached document publication caller from `session._capture_bundle(session_state)` to `session._bundle(session_state)`.

Classification: the two independent selector failures are a product-source regression introduced by `8a4103dd16` (repeated by `8d14d5be18`), not a product/setup inference from the exception alone. The original duck-typed public publication sessions expose `_bundle`; the current production `TimelineSession._bundle` retains authenticated private capture and strips `_runtime_document` from the returned public projection. The repair therefore preserves D71 authority, exact revision/publication authentication, and the no-leak boundary.

Tests are unverified because the exact mandated Runtime checkout is missing. The requested command stopped before collection on `runtime_protocol` import. Lint, AST, scoped mypy, diff-check, source/test hashes, and byte/mode conservation passed.

Next step: restore or provide the exact Runtime worktree at `/home/user/work/wt/rt-pin-6a011d58` with the expected tree, then rerun only the two named nodes using the command recorded in `validation.md`.
