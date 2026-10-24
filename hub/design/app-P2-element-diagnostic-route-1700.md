## Report

Implemented focused D66 route:

- `p2-element` selects exactly the unchanged first element test.
- Targeted launch retains private Runtime stdout/stderr.
- Collection works without requiring detached source checkouts; launch guards remain unchanged.
- No original specs, bodies, waits, selectors, or P3 files changed.

Ready command:

```bash
node scripts/testing/d66-plain-stack.mjs p2-element run
```

Registration candidate: `d66-p2-element` mapped to that command.

Tests:

- Target collection: 1 test — PASS
- Existing P1 collection: 2 — PASS
- Existing P2 collection: 8 — PASS
- Existing P3 collection: 1 — PASS
- D66 unit controls: 5 passed
- Node20 syntax, ESLint, `tsconfig.node.json`, `git diff --check`: PASS

Current inputs:

- App `9e1f5818`, Agent `a60f8b39`, Runtime `5c1a03f1`, Composition `635f4de0`
- Node `v20.19.4`; Agent/Runtime Python `3.13.16`
- Expected detached routes: `agt-pin-a60f8b39`, `rt-pin-5c1a03f1`

Runtime phase seam remains uninstrumented. Candidate owner should instrument:

- arrival/handler: `runtime_protocol/server.py:_timeline_commit`
- auth/execution: `service.py:_execute_timeline_commit`
- lock/provider: `timeline_commit_execution.py:75,87`
- receipt: `timeline_commit_store.py:1441`
- response: `server.py:_send`

Required safe fields: phase, duration, numeric status code, and request source classification. No browser/service request was submitted before that candidate was ready.