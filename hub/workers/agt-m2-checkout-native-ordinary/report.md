Implemented `Checkout.attach(session)` for bounded move, trim, hold, asset-clear and literal parameter edits. Commands persist before preview changes; targets use raw scope bindings. No new writer, schema or state framework.

Validation:

- Targeted adapter/session/provider/media/parameter tests: **136 passed**.
- Conformance/transaction/sheet tests: **290 passed**.
- Central pinned Runtime lane: **6 passed**, including renderer-off restart, exact retry, dependent trim, CLI capture and guarded undo.
- Ruff and whitespace checks passed. No full suite run.

Exact commands, failed attempts and results are recorded in [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-checkout-native-ordinary/notes/report.md).

Selected-pack parameters and unsupported DSL families remain explicitly held. Legacy CLI edit/apply and snapshot publication remain migration work; this does **not** claim AG02/WC7-8 completion or writer deletion. Repository-wide mypy/cycle gates remain unresolved, alongside five untouched stage1 retired-route failures.

`commit-msg` and `DONE` are written. No commit, push, integration-tree or shared-dependency changes made.