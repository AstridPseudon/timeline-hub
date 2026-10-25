# D139 independent security/source review

Result: **FAIL**.

## Exact checks

- `df -B1 /home/user/work`: **PASS**, 5,244,248,064 bytes available; above the 5,000,000,000-byte source floor and 4,000,000,000-byte stop line.
- `TMPDIR=/tmp/d139-review-2232 /home/user/work/venv-agent/bin/python -m pytest -q ops-d139-retirement/tests/test_store_retirement.py`: **PASS**, 11 passed in 1.41s.
- `python3 -m py_compile ops-d139-retirement/bench_store.py ops-d139-retirement/tests/test_store_retirement.py`: **PASS**.
- `bash -n ops-d139-retirement/retire-child-venv`: **PASS**.
- `ruff check ops-d139-retirement/bench_store.py ops-d139-retirement/tests/test_store_retirement.py`: **EXPECTED FAIL**, only `EXE002` on executable no-shebang `bench_store.py`.
- `ruff check --ignore EXE002 ops-d139-retirement/bench_store.py ops-d139-retirement/tests/test_store_retirement.py`: **PASS**, all checks passed.
- `ruff check /tmp/.../orch/bin/bench_store.py`: **BASELINE**, `EXE002` plus the three pre-existing style diagnostics (`I001`, `C410`, `BLE001`).
- `ruff check --ignore EXE002 /tmp/.../orch/bin/bench_store.py`: **BASELINE**, the same three pre-existing style diagnostics. The candidate normalizes those diagnostics; no broad lint ignore was added.
- `git diff --check`: **PASS**.
- `diff -u` against installed `123bb93` and `954d`: **PASS for scoped review**, with only the source-manifest hunks; modes remain 0755.
- Read-only SHA-256 checks: candidate and caller hashes match `source-manifest.json`; no installed source or caller was modified.

## Findings

### D139-R1 — retirement recovery accepts unrelated victims

The candidate routes `retirement` through the eviction validation branch at `bench_store.py:618-622`. Recovery then accepts any `journal.victims` set equal to the removed entry set and deletes every victim at `:664-681`. It does not bind a retirement journal to exactly one requested registration and one child entry.

An isolated private fixture modified `pending.json` after `retirement:journal` to add the unrelated `venv-agent-child-d40-ba8f-f320` entry to `victims`, removed that entry and registration from `after`, and recomputed the candidate's own projections. `recover()` accepted it and produced:

```text
tampered_recovery_deleted_target= True
tampered_recovery_deleted_unrelated= True
retired_names= ['venv-agent-child-d137-a4e016', 'venv-agent-child-d40-ba8f-f320']
```

This violates the finite requirements for journal validation/recovery, index/registration integrity, and no unrelated deletions.

### D139-R2 — KEEP is not rechecked before owned deletion

`Store.retire` checks `KEEP` before writing the journal (`:571`), but `_delete_owned` has no KEEP check (`:428-498`). An isolated private fixture created `KEEP` at the `index` checkpoint, after the journal transition and before deletion. The entry was still deleted:

```text
keep_added_after_index= False
entry_deleted_despite_keep= True
```

The first value is false because the directory was removed; the marker was created by the checkpoint hook. This leaves a deletion-window race against the required KEEP protection.

## Route and custody checks

The unchanged production caller remains `request-retire-venv` → `RETIREVENV` → normal `dispatcher-daemon` → `retire-child-venv`; the candidate's defaults point to the same `$O/bin/bench_store.py`, `$WORK_ROOT/bench-store`, and `$O/tests` locations after normal kit installation. The real read-only index maps `venv-agent-child-d137-a4e016` to the owner-authorized `child-3e163…` entry; `venv-agent-child-d40-ba8f-f320` maps to the suite-referenced `child-3b5cb…` entry and was not operated on.

No live install, queue/request/dispatcher execution, Store operation, real cleanup, refusal retry, manual index edit, kit write, full suite, child/core/profile/acquisition test, or D130 work was performed. The 2210 route review remains authoritative that the direct pre-candidate route was `EXACT_MISSING` and that no age-only or manual cleanup authority exists.
