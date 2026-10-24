## PASS — current App home qualification

- Head: `a2a6e4abbd5cd8611510ee8aeaf882a0962259ec`
- Tree: `6cae4f2fc4bb0813b0cbb90388d232cb169596b4`
- Tracked paths: `4910`
- Worktree: clean; no source, test, pin, ledger, or design edits.

Reviewed path blobs matched their originating commits exactly:

- Voice: `db6cf3f…`, `06c5ef5…`
- Fullscreen: `20b9398…`, `4bc052b…`
- P2 parent: `79c2111…`, `e10cfe3…`
- P3 Gate 5: `43ffa2b…`, `4b20561…`

Protected hashes retained:

- Voice frozen body: `d2925e066d4a600f23866cb09112c75082f5e4accd8c9eb5290e012ef2f522fc`
- Fullscreen frozen body: `40564bab4179dbcf0165fe652658abb43f6b2c13a34a8c06ac078c29b44b6339`
- P2 original cases: `be3db6fe…ba36`, `522c98e2…138c`, `df955842…010f1`
- P3 protected specs: `95d9a3e7…d296`, `2b9723db…1593`, `50960dd2…ebf17`, `c0624a04…e797`, `4292d0b5…d1de9`
- P2 whole-file before→after:
  - `67662468…c9cd0e0` → `07fe3d84…ed2f3c`
  - `225a4c43…df47e90` → `98934ece…d1d272`
- Gate-5 reset helper before→after:
  - `94568a9b…c71ab` → `70030d76…6afb`
  - `430d7501…2fee` → `160f05fa…4f8c`
- Gate-5 fault-order hashes unchanged: `8ea7522a…d7f5`, `e7235bc7…e06b`

Focused checks:

- AgentChat Vitest: **58/58 passed**
- Fullscreen + host neighbor: **15/15 passed**
- P2 parent/transition/document controls: **10/10 passed**
- Semantic oracle private Vitest run: **7/7 passed**
- Gate-5 reset/fault controls: **23/23 passed**
- Root/app/node/fake-runtime TypeScript: **all passed**
- Scoped ESLint, `check-no-raw-skips`, `git diff --check`: **passed**

Runtime pin verified: `bc227de07262accb702eae8a44c4a666b568c08e`, schema `sha256:867f3553…1708b`, 14/14 lock mappings byte-identical to the pinned Runtime commit object.

The unsafe placement draft `fe773e45aa…` is not an ancestor, and current placement files match its parent.

### Behavior ledger rows

| ID | Current behavior | C0 citation | Actual home proof |
|---|---|---|---|
| P3-history | Authenticated `recorder_abi: 2` is required for physical-binding Gate-5 history; wrong/missing ABI is rejected. | C0 §§4,7; D62 history-only `recorder_abi` | Author `471dc827…`; home merge `9f4ec08f…`, tree `c13980c7…`; 23/23 controls passed. |
| P2-parentreads | Submitted request `reads` must match authoritative history exactly; omitted reads remain absent. | C0 §§1,4,5,7 | Author `6b7b6e7a…`; integrated home `a2a6e4ab…`, tree `6cae4f2f…`; 10/10 P2 controls passed. |

No browser, original journey, service, or full suite was run. Prior old-RED/new-GREEN and live-case preservation evidence was reused only where exact source/test blob identity matched.

One limitation: `vendor-lock.mjs check --producer /home/user/work/runtime` saw that shared worktree move to `5c1a03f…` instead of pinned `bc227de…`; the pinned commit object itself matched all 14 App mappings exactly.

Commit message and `DONE` marker written.