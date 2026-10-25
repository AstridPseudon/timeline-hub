# PASS — R2 integrated-head acceptance

- Runtime: `bc487974a5a9e6179805f0d76462f228f56b4aaf`
- Tree: `b440a6aeb3ebb7993fdc42f9641e7bfae3995791`
- Reviewed candidate tree matched exactly; no outside merge changes.
- Agent: `8d2d58828a9b03ea6868c339e45369bb5f96adad`
- Regression SHA: `e166ca832bad75df0415e004bcd854058387b4aa38c6393f781f126828b8af44`
- Runtime auth SHA: `572700dede669dd3d30370b643824b9bb760bbbefb8fac524da8e2b57e9a0799`
- Origins verified before/after against the genuine Agent checkout and integrated Runtime.

Results:

- Registered-provider nodes: `2 passed`, exit 0.
- Native-provider smoke: `2 passed`, exit 0.
- Scoped Ruff: pass.
- Scoped in-memory compile: pass.
- `git diff --check`: pass.
- Admission remained above 5 GB; no heavy runs or installs.

Exact test IDs/commands and durable XML are in [evidence/summary.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-step-home-proof-1519/evidence/summary.txt).

Limits: parent repeat, original-four/ten, P4, full, browser, and complete wire-contract coverage were not run. No product files or tests were modified. `DONE` and the task-named commit message are prepared.