Implemented element-only declaration validation without phantom params writes. The original strict-xfail now passes; pack ownership, exact retained inputs, restart, retry, replay and inverse are covered.

- Local targeted tests: **287 passed**
- Direct Runtime tests: **9 passed**
- Central named suite: **34 passed**
- Ruff, schema validation and diff checks passed.

**Blocked:** the required generated Runtime schema/Agent pin pair remains outstanding. Next: generate that pair, refresh the pin and requalify.

Schema SHA-256: `c520c7fa5269f837965b308607dcc7c73a9e4fd5f1da6bb09022996ba86620e6`.

Wrote `commit-msg`, the outgoing schema and `BLOCKED`; no `DONE`. [Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-element-declaration-retain/report.md).