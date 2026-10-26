# D141 REG upgrade identity correction validation

Result: PASS for the finite read-only identity correction. This derivative closes the one metadata identity finding; it does not alter or relabel the original review artifacts.

## Mechanical identity checks

- Assigned worktree branch: `tl/rt-F-D141-REG-upgrade-identity-correction-0505`.
- `git rev-parse HEAD`: `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`.
- `git rev-parse HEAD^{tree}`: `f71c60df29ab29cbea678794e882db8c0d053214`.
- `git rev-parse HEAD^`: `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`.
- `git rev-parse 'HEAD^^{tree}'`: `ac5b862744bece65b2e30565db1777bacd60da28`.
- `git cat-file -e 012889c1b0bbfe5f290f757cb6d31dd7d995ccc6^{commit}`: exit `128`; requested object absent.
- Commit subject: `fix(runtime): repair U1 D141 REG upgrade inspector`.
- `git diff --name-status HEAD^ HEAD`: `M runtime_protocol/upgrade.py` only.
- `git diff --stat HEAD^ HEAD`: `1 file changed, 3 insertions(+), 1 deletion(-)`.
- `git diff --check HEAD^ HEAD -- runtime_protocol/upgrade.py`: exit `0`.

The changed path's preimage is Git blob `d2cb5afb56ebacbc09c3b59e41c44de4626182ae`, SHA-256 `c3f44783b1145877ceec913a4bddeb925e711275296550570fa58a1bc8648cdb`. The actual blob is `4daea429c71a1e96ee2649bd14d9e6b742923162`, SHA-256 `c8787dc29b3fa0097ee7aaa9daa704c1626523498cd2c4574f10e14d7e840d50`; the worktree file has the same SHA-256.

## Identity-input checks

The manager brief and dispatched worker brief are byte-identical, each SHA-256 `7a30ebdbbe7e6de60248602c79a171197b84143a424d4c94fe40a92dc745e059`, and each names `...ccc7`. The worker `meta` SHA-256 is `1a85f714266bda3dec54ea7bca1af45954f2d91b42d6a7595cee72518d4acedd`, and its base is `...ccc7`.

The original five review evidence files remain byte-preserved. Their exact SHA-256 values and byte lengths are recorded in `correction.json`. The correction withdraws only the false `requested_author_commit=...ccc6` attribution from that historical metadata; it does not overwrite it.

## Carried-forward qualification

The original independent review recorded `source_verdict_for_actual_head=PASS` and the exact unchanged 13-selector result `13 passed in 7.77s`, with no failures, errors, skips, or xfails. Those qualifications are reused, not rerun. No new semantic review, test, lint, typecheck, production-caller run, or new-head proof was performed by this identity correction. No product fix is requested.

Final finding state: zero remaining findings after correcting the exact intended immutable author identity to `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`.
