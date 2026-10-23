# Handoff: ap2-P3 custody fixture review

Review of `7eee76432efdf1abd1960eb868d27f5ecdb9897d` is **FAIL**.

The diff is exactly one existing fixture setup change (13 insertions, 1 deletion), and
ESLint, App typecheck, Playwright discovery, diff checks, Agent owner controls, and
empty-shell/closure controls were run. The proposed POST create-timeline call is not a
valid legacy-baseline adoption:

- Current Runtime `49ce532...` retires the seed's legacy composition POST before the
  authoring-profile restart (`server.py:589-591`, `service.py:2795-2797`).
- The available same-ID production path is explicitly empty-shell-only and rejects
  authored timeline scope (`service.py:1712-1757`, `timeline_commit_store.py:1390-1412`).
- Agent `bd239/a813` owner-reader strictness correctly explains the original checkout
  failure but does not repair or persist a missing manifest.

No repository changes were made. See the worker report for exact commands/results and
the two current integration follow-up failures caused by Agent/Runtime provider-command
mismatch. A real transactional legacy-closure importer (or a supported commit-native
fixture seed) is required before this fixture can pass.
