# OPS-bench-store lease review — FAIL

Independent Luna review of the finallease1850 packet against the settled plan/interface/common header: **FAIL**.

The 21 private fixtures pass, but caller coverage is incomplete. The embedded production seam accepts `Store.names_for_suite(...) == []` when the suite row is unchanged, then calls the command directly as if it were an unmanaged legacy suite. A custom pre-existing gate row can therefore use a managed bench by absolute generated path without acquiring its flock.

Reproduction used only the exported seam and tiny core API: managed entries were created with generated `BENCH_PATH={bench_path}` and no managed suite row; an existing custom `suites.conf` row referenced the first managed path. `names_for_suite` returned `[]`; while the exact seam command was alive, creating a third managed entry evicted that first path. Output:

```text
names_for_suite=[]: True
custom_row_not_created_by_ensure: True
managed_path_evicted_while_command_alive: True
command_rc: 0
```

Relevant source: staged `test-run` lines 66–71 and 92–98; exported seam lines 25–30 and 51–57. Existing `test_unregistered_existing_suite_has_no_lease` (`test-leases.py` 275–277) encodes the unsafe broad expectation and must be narrowed to genuinely unmanaged legacy usage.

Required 21-test replay passed (`Ran 21 tests in 7.877s`, `OK`, core hash `53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14`). Syntax, compile, manifest hash, patch replay, Runtime cleanliness and diff checks also passed. No source or product edits were made; no live service/full suite/installation ran. See the worker report for exact commands, hashes, limits and recommended remediation.
