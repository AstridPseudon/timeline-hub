## D80 report: bounded attribution

**Result: FAIL for gesture qualification; PASS for bounded source/evidence attribution.**

All four isolated runs reached readiness, then failed during native fixture seeding:

- `13134` register asset
- `20974` automatic child placement
- `30454` popup swap
- `7151` transition-none single

Each had readiness `1/1`, original `1 test, 0 assertion failures, 1 setup error`, with `transport_timeout` at `support/harness.ts:990`, called from `seedThreeProducts:1197`. No gesture body or product assertion ran.

Evidence: [producer packet](/home/user/work/app/design/app-P2-D80-1855.md), plus each retained [manifest](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d80-p2-register-asset-1855-1024185450-13134/d66/manifest.json>) and [phase log](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d80-p2-register-asset-1855-1024185450-13134/d66/runtime-private/p2-commit-phase.jsonl>).

The actual route is direct Python `AstridClient` → existing Runtime commit endpoint. Runtime received each request: request 1 returned HTTP 200; request 2 entered the handler but retained no HTTP response. Phase captures are bounded at 128 events, so they do not prove lock contention or a Runtime deadlock.

The exact observable seam is SDK transport policy: generated `WorkspaceClient` uses a fixed default `timeout=30.0` and maps expiry to `transport_timeout`; App’s surrounding subprocess timeout is 120 seconds. The underlying Runtime-progress/cost cause remains **UNKNOWN**. Relevant App harness, Agent client, generated client, and Runtime commit-route sources are unchanged between the failing tuple and passing P131083 control. P228847 also had the same generated transport client.

No source, test, pin, registry, or generated files changed. No repair or timeout relaxation is justified. Next owner: existing Runtime execution/cost owner, using these retained phase logs to determine why the native seed commit did not return within the SDK’s 30-second request window.

Checks:

- Node20 `--check scripts/testing/d66-plain-stack.mjs` — PASS
- `git diff --check` — PASS
- Worktree clean
- No suite repeated

Commit message and `DONE` marker were written.