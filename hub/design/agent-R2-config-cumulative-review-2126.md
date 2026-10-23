## Review report

### Decisions

- No product/test edits made.
- No G5 ancestry, retirement, generated files, locks, Runtime/App/Composition changes imported.
- `parent.occurrences` support is exact-path-only, deep-copied, and accepts only full-row permutations; changed owners, pins, fields, membership, duplicates, and arbitrary parent paths are rejected.
- No assertions were weakened.

### Results

| Scope | Result |
|---|---|
| `4b874103e` own scope | **PASS** — 96 targeted tests passed. It cannot satisfy the later neighbor test alone because `_command_state.py` support is intentionally supplied by `507a664`. |
| `507a664` own addition | **PASS** — captured neighbor tests: 41 passed. |
| Cumulative `07e6d83 → 507a664` | **PASS** — exact five-file suite: 137 passed in 55.87s. |

The cumulative diff contains exactly the four allowed paths; all 3,429 outside-scope tracked identities are unchanged. Ancestry is exactly `07e6d83 → 4b874103 → 507a664`.

### Verification

Passed:

```text
exact five-file pytest: 137 passed in 55.87s
captured neighbor test: 41 passed in 1.83s
Ruff: passed
mypy: no issues in 4 source files
vendor_lock.py check: passed
artifact_manifest.py --check: passed
git diff --check: passed
```

Security controls covering native/effect/range/ordinal/publication/step/owner/order/shape/ABA/authored-row/foreign/managed-edge/history provenance all passed. No corrupt snapshot or arbitrary-parent acceptance was observed.

### Provenance

- Agent module origins remained this worktree.
- `_step_undo.py`: baseline `459151d5…` → final `e47e880c…`
- `_command_state.py`: baseline `030d06a3…` → final `5584a8d0…`
- `_root_inverse.py` unchanged: `6715f34f…`
- Runtime imports resolved to `/home/user/work/wt/rt-pin-8ea0766f`; tree `6047ac3…`, matching merged `abd47e…`.
- Runtime module hashes and vendor producer identity were unchanged.

No full suite, browser/HTTP/journey, original c271 body, benchmark, daemon, or Git mutation was run. G5 remains P1-gated. No blocker remains for the stacked reviewed merge.