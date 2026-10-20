Implemented R1/N1; preserved the historical theme and all 286 SSR expectations.

- Local targeted tests: **47 passed**.
- Central `remotion-0012-nodes`: **13 passed**; its default marker filter excluded 34 integration cases.
- Manifest and whitespace checks passed.

**Blocked:** merge-forward cannot write read-only Git metadata. The orchestrator must run it externally, then qualify the merged tree with integration tests enabled. The shared Remotion lock also lacks eight `libc` fields.

Wrote `commit-msg`, `BLOCKED`, and the [report with exact commands, hashes, tuple, and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent12-current-adoption.md). No DONE claimed.