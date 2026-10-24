## Review report

Verdict: **FAIL — source candidate not qualified for farm installation.**

The four private tests pass, but the helper fails the required replaced-inode refusal. After creating a valid empty store, I replaced each of `entries`, `locks`, `staging`, `mutex`, `owner.json`, and `index.json` with same-shaped nodes. The helper returned `0` and `reused` for all six instead of refusing.

Cause: [`init-bench-store.py:57-71`](/home/user/work/wt/rt-OPS-farm-full-review-0405/ops-handoff/farm-agent-full/init-bench-store.py:57) calls private `_load()` directly; inode checks only occur through `Store.mutex()`.

Checks:

- `pytest ... test_farm_agent_full.py`: **4 passed**.
- Private 8-process initialization race: **1 initializer, 7 reusers; final store valid**.
- Ruff: **passed**.
- In-memory compile: **passed**.
- Manifest SHA verification: **all OK**.
- Template `cmp`, decoded row/env hashes, row parsing, env key validation, `bash -n`: **passed**.
- Row preserved current `agent full` command; current row: 86 bytes, SHA-256 `65fd24facbce3b1661aaedab1967033a2b2c7d00345a92b0bd8db7969673c184`.
- Decoded row excluding LF: `ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`.
- Decoded env: `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`.
- `git diff --check`: **passed**.
- No product, C0, ORCH, registry, queue, store, install, network, or full-suite changes.

The selected Agent lock currently names Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`, matching the candidate, but `/home/user/work/wt/rt-pin-45c3a7f4` is absent locally. This is not evidence that the farm lacks it. No actual `full-farm` row, snapshot, or qualification run was observed.

Production `request-test` → `test-run` uses the normal Store lease path, but this candidate was not registered or executed. Existing `Store.ensure/recover` transaction code was inspected; no install or rollback operation was performed.

Recommended next step: repair the helper to invoke the store’s ownership/inode validation path before reuse, add the replacement tests, then repeat independent review before any normal checkout, registration, or farm run.