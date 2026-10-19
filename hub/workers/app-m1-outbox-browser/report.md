## Completed

Added [command-outbox.spec.ts](/home/user/work/wt/app-m1-outbox-browser/tests/e2e/timeline/command-outbox.spec.ts), proving with real Chromium:

- Native IndexedDB persistence and strict reservation before transmit.
- Exact A request retry after persistent-context restart.
- Original B payload/guards/IDs retained with a fresh key and base `HA`.
- Native `navigator.locks` exclusion across pages.
- Independent owner isolation.
- No sessionStorage owner adoption.
- A acknowledgement cannot erase dependent B.

Chromium: `/opt/pw-browsers/chromium`; temporary profile is cleaned up.

## Tests

- `npx eslint tests/e2e/timeline/command-outbox.spec.ts` — passed.
- Targeted TypeScript syntax check — passed.
- Central browser suite — passed: **1 test, 17.3s**.
- `git diff --check` — passed.

Commit message written to the required path. No blockers or out-of-scope changes.