# G5 SDK/current CLI qualified join — blocked integration witness

Imported the exact two reviewed SDK history test blobs onto Agent draft
`cc8be25d4`:

- `tests/sdk/test_timeline_checkout_history_runtime.py`: blob
  `73092f1a333e10be6d7966213ccc0a82a7ec7106`
- `tests/sdk/test_timeline_checkout_history_boundaries.py`: blob
  `d2ee3d0e928896fb8b127b2f3dd556c3d5ebe078`

The 13-node inventory collected as 9 boundary nodes plus the original 4
integration nodes. Boundary qualification passed (**9 passed**). The sole
actual central four-node execution reached the shared fixture but Runtime
`9ce4242` refused the inherited `publish_parent_composition` bootstrap with
`RetiredRouteError` before any public test body ran (**4 errors, exit 1**).
Per the task stop rule, no fixture, route, or assertion workaround was
attempted. Detailed commands, hashes, interface preflight, service IDs, and
limits are in the worker [report](../workers/agt-G5-sdk-qualified-join-1545/report.md).

Status: draft/P1-gated; no integration merge. Runtime/owner must resolve the
approved current commit-based fixture bootstrap, then rerun exactly the same
four nodes.
