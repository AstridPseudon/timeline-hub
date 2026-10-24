Implemented the narrow D61 consumer continuation from `e32a8a87c9`. Only `commit.py` and the existing regression file changed. `commit-msg` and `DONE` are written for the harness.

Reservation history now consumes authenticated-entry `recorder_abi`, rejects ABI2 full rewrites and malformed metadata, and preserves absent-field/ABI1 behavior. Original test bodies remain unchanged.

Validation, with exact commands linked:

- [Focused cohort](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-recorder-ABI-consumer-sol-1417/evidence/final-fork-command.json>): **249 passed**
- [Strict baseline](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-recorder-ABI-consumer-sol-1417/evidence/strict17-command.json>): **17 passed**
- [Null/validation](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-recorder-ABI-consumer-sol-1417/evidence/null46-command.json>): **46 passed**
- [Source-copy/v2 controls](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-recorder-ABI-consumer-sol-1417/evidence/source-copy-v2-negatives-command.json>): **134 passed**

Fifteen old-source failures become GREEN. Scoped mypy, artifact checks and diff checks pass. Ruff retains exactly three pre-existing I001 findings. Durable XML and source/AST evidence are retained. No full/gate/live runs performed.

**Integration hold:** Runtime `e68cf23164` still lacks the producer field. The production consumer call chain is verified; producer authentication is unqualified. R-recorder-abi-authority must supply the exact field slot, producer SHA/tree and tamper qualification. Then obtain independent Luna security review and manager merge-forward onto home `5492fc8041`, retaining the saved1354 repairs and current Runtime lock.