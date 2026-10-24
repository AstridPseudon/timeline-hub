**Source remains HELD; no install. One of three counterexamples is closed.**

Changed only `ops-bench-store-legacy/`:

- Recovery requester derives its queue from its script location, ignoring inherited `RUNTIME_ORCH_ROOT`.
- Queue creation uses validated, nonsymlink directory descriptors and exclusive file creation.
- Regenerated `source.patch`.
- Retained both deletion adversaries with safe-outcome assertions and visible expected failures. All other original tests remain unchanged.

| Adversary, normal and `env -i` | Result |
|---|---|
| Pending-directory symlink substitution | Refused; substituted directory unchanged |
| Substitution immediately before queue-file creation | Refused; substituted directory unchanged; request remains only in displaced owned directory |
| Victim substitution immediately before final `rmdir` | **Still unsafe:** replacement deleted; returns success |
| Replacement immediately before projections | **Still unsafe:** refusal follows suite/index writes; journal retained |

POSIX inode comparison and name removal are separate operations. Quarantine would still require trusting the owning UID against replacement inside it. The smallest honest existing boundary is that owner-UID processes cooperate with the Store mutex and lease rules. I did not claim an additional check establishes atomic safety.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python ops-bench-store-legacy/test_legacy.py` — **24 tests: 22 passed, 2 expected failures**. This is **not acceptance PASS**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-bench-store-legacy/bench_store.py ops-bench-store-legacy/test_legacy.py` — passed; installed core baseline also passed.
- `bash -n ops-bench-store-legacy/request-runtime` and `bash -n ops-bench-store-legacy/dispatcher-daemon` — passed.
- In-memory compilation — passed for both Python files and embedded requester Python.
- Private installed-baseline `patch --dry-run -p1`, actual `patch -p1`, and `cmp` — passed for all three source copies.
- `pyright --outputjson` on private baseline/candidate copies — version **1.1.414**; baseline 21 diagnostics, candidate 19; **zero new diagnostic identities, including multiplicity**. Both commands exit 1 for existing findings.
- `git diff --check` — passed.

The fixture exercises the actual requester → production dispatcher branch → `Store.recover()` in normal and `env -i` execution, plus inherited leases, interruption recovery and protected-current preservation.

All six installed kit hashes remain unchanged; dispatcher hash is unchanged. Actual Runtime remains clean at `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`. Product contract/schema/client/pins were untouched. Scratch totals **19,386,533 bytes**, below 20 MiB. No live target action, deletion, installation, full suite or network operation occurred.

Candidate SHA-256 values:

```text
bench_store.py  b294213889bf1e0b884f1d5192abc47055928052a06ebaf6080ef847c8a476aa
request-runtime 01990c58813dbcd5ffe2ed8f9b7983c46ca30e48ce0e2a0a8cf08d8ea046a3e4
test_legacy.py  361490197a7d222222fe06dda5adb4844e4314fcc4635e4ae8f7c43236295000
source.patch    ee39c103ab5fe4d7daf9474c3df6b107b7a645702021384c31fa537312f4a069
```

Legacy readiness remains separately **BLOCKED**: all seven lack Store ownership; five retain current references; both failed partials lack historical launch custody. Those facts were retained without another inventory audit.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Next: independently review the queue fix, keep this packet uninstalled, and resolve the existing launch-fence/current-reference requests before qualifying any legacy action.