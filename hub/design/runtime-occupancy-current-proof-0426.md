## PASS — R5 occupancy qualification

- Imported only `tests/test_timeline_legacy_occupancy.py`, byte-identical to reviewed commit `3441bc34a8a74ed51ad8b6e63b3b4f433f107dd6`.
- Runtime base: `2b49da8d6d8dbb8245a1a7cc8d7eee7d3bdaae65`, tree `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`.
- Agent custody: `9f2da582a6767030055e54092287d40f2b8f74bb`, tree `80c4f98ca5a57c19b99f9e729ef6963ac662c32b`; reviewed parent `12701589abffd840054515996612d0ed0dd33af0`.
- Agent source resolved exclusively from the private exact archive; no installed overlay.

Qualification command:

```text
ASTRID_CHECKOUT=/tmp/w-b2e3463ce8/rt-R5-occupancy-current-proof-0426/agent-source-9f2 \
PYTHONPATH=.:packages/python \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_legacy_occupancy.py
```

Result: `16 passed in 43.89s`.

All 16 nodes passed, including accepted/refused/retry/preview and both historical inline/reference inverse cases. No boundary failed, so no failure packet was required.

Checks passed:

- Reviewed-parent/final Ruff diagnostics identical: four pre-existing diagnostics.
- Pyright: zero errors; identical two unresolved Runtime-helper warnings, same Agent archive path.
- In-memory compile/body identity and original 65-assert preservation.
- `git diff --check`.
- Only the fixture file changed; no product, schema, client, Agent, pin, or kit changes.

The current integration’s pre-import fixture was an older file with different lint diagnostics; the mandated exact reviewed fixture was retained unchanged.

Next owner: independent Runtime review, then the Runtime merge queue. Commit message and `DONE` marker were written; no commit was performed.