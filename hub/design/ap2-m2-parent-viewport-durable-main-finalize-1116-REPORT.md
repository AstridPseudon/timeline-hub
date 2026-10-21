# App2 parent viewport durable MAIN finalization report

## Result

Recovered the recycled 1110 handoff/report into absolute `ORCH/design`,
closed the committed parent source identity, and produced an executable
MAIN-only preflight/actual proposal. No product source was changed in this
worker and no browser/build/socket/service/full/install/actual was run.

Closed parent role:

```text
parent_role_sha=6707a30f14bf3a5ee19cb9e481b7dbd95b77522a
parent_role_tree=6ff32d797f0e774b8574274a3494ce8755fa160c
```

Changed live callers: **NONE**.

## Absolute artifacts

- Handoff: [run-on-main-app2-parent-viewport.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-main-app2-parent-viewport.md)
- This report: [ap2-m2-parent-viewport-durable-main-finalize-1116-REPORT.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-REPORT.md)
- Recovered prior report: [ap2-m2-parent-viewport-current-main-packet-1110-REPORT.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-current-main-packet-1110-REPORT.md)
- Bound helper/runner/driver/gate artifacts are beside the handoff in the same absolute design directory.

The shared helper
`normal014-source-common.sh` remains unchanged at SHA
`96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109`.
The new private helper copy is SHA
`2b3b67bfd29e76d66f05e7c473eff80b6bd9f9609b4dcba4bf2d4cd2dcac59b1`;
it binds only the committed App source and HOME graph/archive inputs and keeps
the final95 Agent/Runtime/artifact/schema guards. Existing 0939 runner and
retention behavior was retained; no helper mutation was made.

## Checks run

Read-only/source checks:

- `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, and clean-status check
  against the exact source — PASS.
- Current spec blob equals donor blob
  `e612c18cac2a651e855e75388498762f034dc63a` — PASS.
- Current source is descended from pointer ancestor
  `44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0` — PASS.
- `git cat-file -e 9018c733...:tests/e2e/local/three-products.spec.ts` —
  PASS.
- `git diff --check HEAD^ HEAD` — PASS.
- `git diff --name-status HEAD^ HEAD` — PASS; the committed source change is
  only `tests/e2e/local/three-products.spec.ts`.
- `sh -n` on bound helper, App/source runners, driver, and gate — PASS.
- The handoff's aggregate shell block was extracted and checked with `sh -n` —
  PASS.
- Hashes were computed directly from each absolute artifact and are recorded
  in the handoff.

Prior 1110 evidence recovered from its surviving worker log records:

```text
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0  PASS
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts:1410 --list  PASS; exactly 1 intended test
```

Those ESLint/list checks were not rerun here because this finalization task is
source-custody/handoff-only and explicitly forbids local browser/service/full
execution. The future MAIN preflight repeats the exact list check under Node
20.19.4.

## Decisions

- The harness commit is now available, so the parent role is closed with the
  literal 40-hex SHA/tree above; no pending placeholder is used.
- The old 1110 Node 22 and worker-local graph assumptions were removed from the
  executable handoff. MAIN must use the concrete HOME Node20/venv/graph paths
  and supply the graph archive path through an explicit identity input.
- `/home/user/work/app` is never a source root. It appears only as the
  read-only shared dependency target and the existing wrong-tree refusal probe.
- The existing strict 404 body, original target/placement/guards, runner,
  retention, and cleanup are preserved. No new framework, endpoint, DTO,
  helper mutation, pin, or product change was introduced.

## Unresolved / blocked

This is intentionally not marked READY:

- MAIN must request the exact detached App checkout for SHA 6707/tree 6ff.
- MAIN must verify the exact Node20.19.4 binary/hash, Chromium, Agent/Runtime
  venvs, and leased symlink-free graph.
- MAIN must provide the existing graph archive path with the fixed 895c hash.
- The actual mounted journey and all post-import assertions remain unverified.

Recommended next step: manager closes those prerequisites with the aggregate
preflight in the handoff, then authorizes at most one actual through the
existing gate. Preserve any failure packet and stop on first new cause.

