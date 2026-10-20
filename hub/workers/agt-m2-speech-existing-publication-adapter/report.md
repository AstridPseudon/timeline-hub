Implemented the narrow speech publication adapter.

- Added exact v1 audio intent for `speech/main/original/ordinal 0`.
- Preserved explicit caller intent, text/settings, idempotency, readable audio, and RIPPLE behavior.
- Retained terminal Runtime task/attempt/association/publication context.
- Added focused admission/context tests; no Runtime/API/DTO or publisher changes.

Tests: `76 passed in 3.42s`; `git diff --check` passed. Ruff remains non-clean due existing legacy findings.

Report/design/commit message and `DONE` marker written under the orchestrator paths. Live Runtime settlement remains unverified pending the counterpart fixture.