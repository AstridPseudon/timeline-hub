Implemented the R1 native-order repair in [_step_undo.py](/home/user/work/wt/agt-R1-full-tamper-sol-1105/astrid/sdk/timeline/_step_undo.py:403). It binds native reference order and parent storage-path order to accepted source history, preserving authenticated child item-path remapping.

Added two faithful captured-history positives and four strict source/inverse tamper regressions. Original tests and guards remain unchanged.

Validation:

- New regressions: **4 failed / 2 passed before; all 6 passed after**.
- Final targeted set: **147 passed**.
- Exact five: **2 passed, 3 failed**, versus **5 failed before**.
- Public-command neighbors: **7 passed, 3 failed**.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **PASS**.
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: **PASS**.
- `git diff --check`: **PASS**.

The three public failures are a separate fixture cause: they alter backing data after `timeline.open()` has cached a verified source. Fresh-open probes reject all three damaged inputs. The legitimate seam is to inject damage **before a fresh `timeline.open()`**; no product re-read was added.

One captured-redo neighbor still fails with `shot item source changed`, identically with the original validator. It remains a separate R2 issue.

[Exact commands and results](/home/user/work/wt/agt-R1-full-tamper-sol-1105/evidence/agt-R1-full-tamper-sol-1105/commands.txt), protected ASTs/hashes, origins, and JUnit are retained. Production reachability is documented through `commit.py → inverse_address_resolver → validate_nested_history`. No live Runtime, browser, full-suite, or gate qualification is claimed.

Commit message and `DONE` created. Recommend reviewing this narrow repair, assigning the three public probes to fixture correction, and retaining the separate R2 failure.