# F-D22 installed identity final cumulative review — 1653

Disposition: **FAIL / not qualified** for the actual installed Remotion gate;
source custody and no-weakening review **PASS**.

The full cumulative diff from bac `bac094180aef38a77b86ab165962e6159f873c60`
contains only `tests/sdk/test_host_bootstrap_source_identity.py`. It adds
authentic `remotion_runtime.py` and `_effect_registry.py` carriers and a
host-bootstrap-boundary validation collaborator isolation. Production
`host_bootstrap.py`, `remotion_runtime.py`, and `_registry_origin.py` are
byte-for-byte unchanged (hashes recorded in the worker report).

The inventory/restart helper is AST-identical to bac with 27 unchanged
assertions. The installed-profile function retains its four original launch
assertions (`-I -m`, no `PYTHONPATH`, unrelated cwd, three launches), but its
function AST is intentionally not identical because isolation was added; the
worker report records both hashes and the unchanged assertion inventory.

The installed-profile selector passes in the requested Agent 8c / Runtime 9ce
/ Node 20.19.4 / Remotion 819acf environment, and the independent bounded
controls pass 9 nodes. That pass is not installed Remotion qualification:
the isolation performs the expected second inventory read but bypasses the
real validation transaction, while the retained central D22 result remains
108 passed / 1 failed at installed registry source binding. Strict canonical
file/argv, foreign, alias, and missing-carrier controls were run separately.

Checks: Ruff 2149/2149, Mypy 1912/1912 using `venv-agent-typecheck-v2`, vendor
lock check with producer `34eac004`, artifact manifest, and `git diff --check`
all pass. No full/109/113 suite, repair, environment/provisioning change,
guard change, skip/xfail, or generated/lock change was made.

Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D22-installed-final-review-1653/report.md`.
