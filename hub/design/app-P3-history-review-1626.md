## PASS — P3 protected-oracle review

Reviewed exact commit `471dc827b631247179b2295ad7a9151b6ab6fe5d`, tree `c13980c7c35c835b804d32c5bc9e501bdb8c1282`, parent `1540b3f12e`.

- Delta: 2 intended files, 9 insertions/2 deletions.
- Runtime lock pins `8b32cacea617c6d45241d7db90b34893a06d3026`.
- Runtime derives ABI 2 from authenticated `physical_ref` bindings and stores it in history/event metadata, not response data.
- Strict `recorder_abi: 2` expectation and explicit wrong-ABI rejection are correct.
- Existing exact-key matching rejects missing ABI; existing wrong-head controls remain intact.
- 20 Gate5 precondition controls + 3 fault-order controls; Node TAP: 2/2 files passed, 0 failures/skips.
- Typechecks passed: App, Node, fake-runtime.
- Scoped ESLint and `git diff --check` passed.
- Protected six original spec SHA-256 values unchanged.
- Fault-order helper/control hashes unchanged.

Helper/control hashes:

| File | Before | After |
|---|---|---|
| `gate5-reset-precondition.ts` | `94568a9baec294cd6848ad37d01163c057c0c4fb0cea202eafe3838b493c71ab` | `70030d76733902445b4f25540d130112f2a6bcd79fcd5216a475c2dfe326afb3` |
| `gate5-reset-precondition.test.mjs` | `430d75012714c7c183f467bba533f1b2122fa834c9711395de935d8ebef02fee` | `160f05fa01c6bbed6ba8f7b8c4e1f00709733237ee8bc28b73eeb4c691c54f8c` |
| `gate5-fault-order.ts` | `8ea7522aa8a6a22f3f5a93616a4bcd9af89eacf46af315465b24fa771a36d7f5` | unchanged |
| `gate5-fault-order.test.mjs` | `e7235bc7074ddb4c75e4dcd958c0c3cf71f640604d968fd750c4162bbd2ae06b` | unchanged |

Ledger row:

| Task | Behavior change | Citation | Receipt status |
|---|---|---|---|
| `app-P3-history-review-1626` | Require authenticated `recorder_abi: 2` for this physical-binding Gate5 history record; reject ABI 1/missing via exact oracle matching. | C0 §4, §7; D62 authenticated recorder ABI authority | PASS; pending manager merge |

No blockers. Source/design files were not modified.