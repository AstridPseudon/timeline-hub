Updated only the six permitted files: corrected request/receipt ordering, bound Store custody to the exact tuple, reused normal-maker validation, restored Remotion guards, and added executable private tests. Registry byte, backup, atomic-update, and rollback protections remain.

The installed Store has no verified-child method; the packet uses its existing registration/lease APIs and pinned maker verification.

Validation:

- Earlier targeted run: **47 passed**.
- Latest run: **34 passed, 24 setup errors** because Store refused `free-space reserve unavailable`. Stopped without bypassing it.
- Ruff, mypy, compile, `bash -n`, manifest verification, and `git diff --check`: **passed**.
- Final acceptance with durable JUnit remains **outstanding**.

Exact commands and results are in [test-outcomes.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-farm-v3-return-sol-0812/evidence/test-outcomes.txt).

The [private production-caller demo](/home/user/work/wt/rt-OPS-farm-v3-return-sol-0812/ops-handoff/farm-agent-full-v3/test_farm_agent_full.py:433) passed: production awk selection and lease extraction, guarded installation, staged fixture execution, inherited descriptors, and a second isolated child. Its sources/packages are invented fixtures; **no Farm READY claim**.

Farm still needs exact checkout receipts, current Store/registry inputs, the normal-maker child receipt and custody key, authenticated installed metadata/sources/origins, approved Remotion graph, and actual parent/child import results.

Commit message and `BLOCKED` marker written. Next: restore disk headroom, rerun acceptance with JUnit, then independent review.