# D118 Agent core progress

Submitted exactly one central-service body through the existing route.

- Body ID: `agent-agent-core-full-1025102221-15065`
- Request: `integration:agent agent-core-full --no-cache`
- Initial service status: `queued`
- Controller worktree: Composition; test target: Agent
- Tuple: Agent `120d71202a9ebafa99011aec417cfca6d67fafc2`, Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`, App `96d4754b4eef0591a208d6b51b60c30fc44b6915`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
- Admission: D89a named-heavy floor installed and controls passed; no other heavy slot was live at submission.
- Free bytes at submission: `4843900928`.
- Durable tuple, manifest, argv, controls and request receipt: `workers/agt-F-D118-core-D89a-1024/evidence/`.
- Canonical compatibility path: `handoff-agt-D108b-core-local-0811-progress.md`.

The body is unfiltered and uses the published 22-root command with `-m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45`.

## Setup retry

The first service record `agent-agent-core-full-1025102221-15065` is retained as a zero-body launcher setup failure: its manifest input path equalled the evidence destination. The same request scope was repaired by moving only the manifest input to the task temp directory and rechecking the existing controls.

- Corrected retry body ID: `agent-agent-core-full-1025102421-30693`
- Retry initial status: `queued`
- Retry manifest input: `/tmp/w-e4e38edaae/agent-core-full-input.manifest`
- Retry evidence destination: `workers/agt-F-D118-core-D89a-1024/evidence/`
