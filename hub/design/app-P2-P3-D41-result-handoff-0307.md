# D41 terminal handoff

No App source/test changes. Worktree remains clean.

Runs used exactly as authorized:

- `app-readiness-D41-caller-sol-0250-full-e2e-three-products-1024030427-12221`
  - Request: 2026-10-24 03:04:27Z
  - Observed start: 03:04:36.027Z
  - End: 03:12:57.064Z
  - Exit 1; duration 501s
  - P2 original 8: 3 failed, 5 did not run.
  - Earliest failure: element edit, line 376; expected status `applied`, received “captured timeline head changed or is missing.”
  - Later failures: popup ADD response timeout (90s); parent move response timeout (90s).

- `app-readiness-D41-caller-sol-0250-ap2-P3-gate5-h6-0348-1024030427-3362`
  - Request: 2026-10-24 03:04:27Z
  - Observed start: 03:04:36.137Z
  - End: 03:07:03.270Z
  - Exit 2; duration 147s
  - D21 native seed/history passed.
  - Earliest failure: D28 mounted readiness, line 301; outbox read was `unknown`, expected `verified`.
  - Original Gate5: selected 1, executed 0, `NOTRUN` by wrapper. No Gate5 verdict.

Both runs passed source/tree/body guards, exact Agent/Runtime pin checks, imports, Node/npm checks, graph checks, and native seed/history setup. P2 mounted-readiness preflight passed separately: 1 passed in 37.4s. These are source/preflight results only; they do not make the proof green.

Exact identities:

- App: `804134d74782d40855146aa568ff289200b79142`, tree `8437e47666853b62e03a58af3716235346316fba`
- Agent: `079580ca46af77e0292d49dc34386b25c8391f99`, tree `2deab1a1494fbccfce5e9235412bacb8a949c0cd`
- Runtime: `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`, tree `be4114705127f9ee9e86b26cd6de3f467e771c01`
- Child key: `5464e85332660e8d6d133653d0600709f2aac5a6c9a0ff0e0bc1fb18312d7f2f`
- Remotion reuse: `agent-remotion-app-ready-079-37eb-0258`, tree `b01dca9b3b24f54093c20b7c5657316f997725db`
- Actual observed backend module: `runtime_protocol.cli`; actual daemon import/source metadata remained `UNKNOWN`.
- Node `v20.19.4`; npm `10.8.2`.
- Ports: P2 `41751`; P3 door `40861`, runtime `43649`, hosted `39579`.

Safe artifacts qualified against existing producer allowlists and bounds:

- `d21-environment.json`: 5,230 bytes, SHA256 `09c8735dc238ea1fabef173f145435e8090da26822d2dc4cfb602dfb0b94df26`
- `mounted-readiness-diagnostics.json`: 652 bytes, SHA256 `eea4457ba7eec02b80e6cfa4c5d1d65f6692159b42293cc61660d9d1ef84c9ce`
- `mounted-bootstrap-lifecycle.json`: 12,494 bytes, SHA256 `679cc75ec9507d42538d4c8364ba28b9c3355fe0b4b6c8964336e3f188cee77b`

All remain at their original local result paths. No raw request/reply JSON, tokens, URLs, private traces, or errors were exported. Historical PASS evidence was not imported into the actual verdict.

Recommended next step: Proof/manager should classify the two actual failures and decide remediation; no product cause is asserted here.