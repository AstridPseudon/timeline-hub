Implemented R2r D83: `_verify_accepted` decodes retained metadata once per fresh verification. Only `timeline_commit_store.py` changed; all authentication predicates remain intact.

- **Measured gain:** median CPU **8.34% lower**, 0.47536s → 0.43571s per three verifications. Metadata decodes **7 → 1**; all **42 validation/keyword/type/equality count frames match**.
- **Focused tests:** **378 passed, 1 failed**. The legacy metadata assertion fails identically on parent dc55 because storage includes `recorder_abi: 1`. No assertions changed.
- **Central controls:** **16 HTTP/history tests passed; 3 ABA/undo tests passed**.
- **Static checks:** zero new Pyright diagnostics (76 existing); zero Ruff findings in the changed function (11 existing elsewhere). Compile and diff-check passed.

[Exact commands, selectors and results](../orch/workers/rt-D83-history-cost-return-sol-2113/evidence/commands.txt) are retained alongside XML, logs, exits, origins and measurements.

Chose repeated JSON conversion because it provides a measured saving without introducing a cache. Original 45-second acceptance remains unverified. Next: independent security review, then coordinate the existing original submitters.

Commit message and `DONE` written.