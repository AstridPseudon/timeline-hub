## D78 report

- Preflight: PASS, exit 0, 2s  
  `app-pin-860e9755-d78-watchdog-live-2001-preflight-1024200212-27752`
- Normal: FAIL, exit 1, 188s  
  `app-pin-860e9755-d78-watchdog-live-2001-1024200242-14383`
- Readiness: 1/1 PASS, 26.0s.
- Element body: did not reach gesture; native seed ended with Runtime `transport_timeout` at the harness’s 120s limit.

Command run exactly once:

```sh
D66_SUBMIT_SUITE=d78-watchdog-live-2001 D66_OUTPUT_DIR=.../submission \
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
--max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

Runtime evidence retained:

- `p2-commit-phase.stacks.txt`: mode `0600`, 4,206 bytes, 57 lines, captured `2026-10-24 20:05:17.584Z`, SHA-256 `eb2e55e78734850ad08f7f36724f3e316e4535f8fec54591d6ac645796276f04`.
- Phase sink: 108 JSONL lines, SHA-256 `8966b306726f91a805342fff0a1ed3b43317acda53c85218176bb47eeb77b3a9`.
- One genuine watchdog capture occurred. Safe frames include `p2_commit_phase_capture.py:_watchdog_fire:226`, `auth.py:_read_bytes:69`, `auth.py:_read_actor:102`, `server.py:_authorize_timeline_commit:276`, `timeline_commit_store.py:_validate:942`, `timeline_commit_store.py:accept:1229`, and `commit.py:commit:1444`.
- Request 1: 22 starts / 22 ends / 0 raised, HTTP 200, 2.743s.
- Request 2: 31 starts / 30 normal ends / 1 raised, locally HTTP 200, 34.498s.
- The 2s snapshot demonstrates a pending dispatch, not a hang by itself; the later 120s transport timeout is the measured failure bound.

Pinned manifest retained four source heads/trees and service versions:

- App `860e9755c8` / `662f848a…`
- Agent `22d00393f7` / `4a1a3a54…`
- Runtime `44917baf59` / `609c6e54…`
- Composition `635f4de06f` / `5ab5191a…`
- Node `20.19.4`, npm `10.8.2`, Runtime `AstridRuntime/0.1 Python/3.13.16`, schema digest `sha256:867f3553…`.

No source, test body, pin, generated file, registry, or design file changes. Worktree is clean. Existing outputs `13100`, `22847`, and D80 outputs were preserved. Commit message and `DONE` marker created.

Recommended next step: Runtime owner should analyze the retained auth/commit stack and phase timing; no speculative App fix is indicated.