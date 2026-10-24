## Completed

- Implemented D73 one-command `--submit` flow:
  - Captures one exact four-repo tuple.
  - Validates checkout receipts and stable App target.
  - Atomically registers unique preflight/normal recipes.
  - Queues and waits for preflight, including 124 resume on the same ID.
  - Queues exactly one normal request only after terminal preflight success.
  - Persists plan/IDs to prevent duplicate retries.
- Added mocked ordering, refusal, timeout, duplicate, and registry-concurrency tests.
- Wrote commit message and `DONE` marker.

## Verification

- Node 20.19.4 syntax check: passed.
- Focused Node tests: 18/18 passed.
- Collections: P1 2, P2 8, P2-element 1, P3 1.
- Scoped ESLint: passed.
- Generic `tsc --noEmit`: passed.
- `git diff --check`: passed.
- No real service, browser, gesture, or original journey was run.

Strict-island lint/typecheck remain baseline-blocked by missing repository paths/modules unrelated to this change.

## Manager invocation

After merging into `/home/user/work/app` and approving the source:

```bash
cd /home/user/work/app && env -u D66_SUBMIT_TARGET -u D66_SUBMIT_SUITE /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p3 --submit
```