Implemented and published the bounded read-only census.

- Result: `EXACTMISSING`; Farm root and bench-store are absent.
- Covers embedded `STORE_VERIFY` (46), `bench_store` (121), dependency verifier (143), and production call graph.
- Added bounded traversal/report/deadline limits and explicit visited/refused/skipped/error boundaries.
- Focused probes confirmed simultaneous hardlink/symlink/writable failures and dependency `EXACTMISSING`.
- Installed source hashes unchanged.
- Worktree clean; no product or production verifier changes.

Artifacts:

- [Census script](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-OPS-Farm-census-return-1516.py) — SHA256 `34c685384cc5e0ea10d840528455712e065cb45e87590cfecc5deb24d06b4881`
- [Result JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-OPS-Farm-census-return-1516.json)
- [Report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-OPS-Farm-census-return-1516.md)

Tests passed: Python compile, `bash -n` maker, JSON parsing, focused probes. Next step requires the exact owner-authorized Farm handoff and independent review before rerunning.