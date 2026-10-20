Completed the bounded history unit; wrote `commit-msg`, [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-local-history-cut/report.md), and `DONE`.

- Checkout publication undo/redo and CLI publication redo use the native outbox/inverse path.
- Local snapshots stop at accepted-base boundaries; older sheet bases can come from retained Runtime revisions.
- **54 product lines replaced/deleted**, net **+52**.
- Validation: **325 targeted tests passed**, **60 parity/facade tests passed**, and **3 real-service integration tests passed**, including edit → reload → undo → redo with the renderer blocked.

AG01/AG03/WC7/WC8 remain open: legacy journal consumers and whole-candidate checkout/sheet writers still need migration. The report lists exact callers, commands, failed diagnostic runs, lint/typecheck limitations, and recommended ledger updates. No full suite ran.