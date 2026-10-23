# R1 actual integrated private-capture proof

Result: **PASS**, bounded Agent controls only.

- Agent start/end head: `bac094180aef38a77b86ab165962e6159f873c60`, tree
  `3c9296e3670586e920f921c9b1b95bbb99b53b82`; clean before and after.
- Reviewed source: `67ba416bca813f4931b557f6f2ca2abf935d7d35`, tree
  `172916ee683f5bda5274c0db49eb9d21825fb2ef`.
- Runtime checkout: `e6a844696daec3eacf5682b09c871e3e2a3df34e`, tree
  `a822f628ba6452f595360f94465be1da7da11054`; source port
  `5328241c2759c79c70213c0655d8d42b308ac7e2`, tree
  `6c94fd42c56950d769b81850a6d5b2cbdf097bd9`.
- Collection: **16 collected, 0 deselected**.
- Exact bounded command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-e6a84469 PYTHONPATH=.:/home/user/work/wt/rt-pin-e6a84469 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py`
- Result: **16 passed in 14.34s; exit 0**.

The integrated merge adds exactly the approved six paths relative to its
first parent: three Agent producer files and three control tests. The only
current-vs-67ba delta is 26 later integrated `_commit_patch.py` lines; no
other production path changed. Private test AST bodies have no overlap with
the Runtime-owned `test_doc_patch_sequential_rebase.py` bodies.

Runtime handoff 1604 independently records 395 current-port passes, 366
passes for the final nine-file verification, and the original nine as 9
passed in 166.57s. Those were not duplicated or rerun here. This report does
not claim the final Runtime accepted-history proof; Runtime owns it.

Actual-head vendor lock, artifact manifest, diff check, and scoped Ruff all
passed. Existing reviewed normal Ruff 2149/2149 and private Mypy 1912/1912
had zero added identities; broad Mypy was not rerun. No full/public/native/
browser/socket/daemon/benchmark/install run occurred.

Full details and hashes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-private-integrated-1629/report.md`.
