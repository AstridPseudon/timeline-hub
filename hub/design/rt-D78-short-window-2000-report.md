## D78 report

- No Runtime source changes; helper already supports `watchdog_seconds`.
- Qualified App D78 route: `p2-element=2s`, ordinary `p2=20s`, others unset. App commit: `860e9755c876ce510aabc5af0511ffe1886626f6`.
- Verified cap `1`, positive-only bounds, `0600` all-thread output, cancellation on return/stop/restart, and cap-1 limitation.
- Evidence: [D78-short-window.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-short-window-2000/evidence/D78-short-window.md)

Tests:

- Runtime focused pytest: `12 passed in 2.72s`.
- Private helper sanity: compile/default/2s/invalid controls passed.
- App D66 test command: `22 passed`.
- `git diff --check`: passed.

Actual live/browser/full harness was not run per scope; native-seed activation and later dispatch were source-confirmed. Commit message and `DONE` marker written.