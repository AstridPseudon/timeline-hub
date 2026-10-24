**BLOCKED: full recovery safety and actual legacy readiness.** Delivered a bounded descriptor fix and reproducible counterexamples; no live installation or cleanup occurred.

Changed only `ops-bench-store-legacy/{bench_store.py,test_legacy.py,source.patch}`. Recovery now passes retained root/parent descriptors into deletion, revalidates observed ownership/path/marker/permission changes before transaction writes, and uses parent-relative `rmdir`. Existing journal, mutex, flock, leases, transactions, and guards remain.

Normal and `env -i` requester → exact dispatcher branch → `Store.recover()` fixtures establish:

| Adversary | Outcome |
|---|---|
| Root/parent substitution, permission changes, or marker corruption at preflight | Refused before projection/index/journal mutation |
| Parent rename immediately before final `rmdir` | Replacement directory preserved |
| Victim-name substitution immediately before final `rmdir` | **FAIL:** replacement deleted; recovery returns success |
| Replacement after revalidation, before projections | **FAIL:** `REFUSED: deletion root replaced` after suite/index writes; journal retained |
| Pending-queue directory replaced by symlink | **FAIL:** requester writes into substituted directory |

The final inode comparison and name-based removal remain separate operations. Retained descriptors close the reopening gap but do not establish atomic deletion authority. These counterexamples prevent a safety PASS.

**Validation**

From the assigned worktree:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python ops-bench-store-legacy/test_legacy.py` — **21 passed**, including three explicit vulnerability reproducers; this is **not** acceptance of those unsafe outcomes.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-bench-store-legacy/bench_store.py ops-bench-store-legacy/test_legacy.py` — passed.
- Ruff against exact installed `bench_store.py` baseline — passed.
- `bash -n ops-bench-store-legacy/request-runtime ops-bench-store-legacy/dispatcher-daemon` — passed.
- In-memory `compile()` of both Python files — passed.
- Private installed-baseline `patch --dry-run -p1`, actual `patch -p1`, and `cmp` — passed for all three source copies.
- `pyright --outputjson` against `/tmp/w-b5bfec720c/qualification/{baseline,candidate}.py` — Pyright **1.1.414**, identical existing diagnostic, **zero new identities**.
- `git diff --check` — passed.

Scratch totals **11,765,332 bytes**. No full suites, network, installation, or shared-dependency writes.

**Legacy readiness remains blocked.** All seven exact original targets remain outside Store ownership. Five retain current references; the two `verify-installed` partials lack historical launch custody. `provision-agent-machine` explicitly requires/builds/verifies `venv-agent-child-s2`, so deleting that dependency is unsupported. Existing makers establish new managed births; neither recovery nor creation authenticates historical custody for these legacy paths. No legacy adoption success is claimed.

Retained SHA-256 values:

```text
candidate bench_store.py
630870208ecccf7c0f841483b58fc74bbbbfbbcefec47ca3195092f2d7eba531
test_legacy.py
24aadb004653fb7ae28d4d74d424b95b9ec3b1dc656d656087199638eb2b8fd8
source.patch
f46eb2da7a444cabc79c5bae5ba2e6d7cfa4523ca81c618c8feb4bfde61a8928

unchanged installed bench_store.py
6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8
test-run
f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4
make-child-venv
c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2
request-child-venv
3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33
make-runtime
873ddcfa636b3ae9e285613a6fb65c643e21ac749e00197d582e0c820dd70149
request-runtime
471fd470efeae102140b96b4f97db857e0d6d79b0839afa10a1a00e911b33b5f
```

Installed dispatcher also remains unchanged. Actual Runtime remains clean at `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`.

Commit message and `BLOCKED` written. Recommended next step: independent review of the mitigation and counterexamples; continue the existing peer0008 request for authoritative launch-fence/current-reference facts. No new permission gate proposed.