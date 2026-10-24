Implemented [evidence/extract_farm_traces.py](/home/user/work/wt/agt-F-farm-trace-extractor-0655/evidence/extract_farm_traces.py).

- Read-only stdlib extractor with fixed log/list SHA checks.
- Emits all 96 closed IDs and 187 setup-error records.
- Preserves byte offsets, bounded traces, exact matching criteria, hashes, redaction counts, and explicit unknown classifications.
- Fails finitely for missing, invalid, mismatched, or mutated inputs.
- No product imports, reruns, network, or log mutation.

Validation:

- `ruff check evidence/extract_farm_traces.py` — PASS
- `python3 -m py_compile ...` — PASS
- CLI help and `git diff --check` — PASS

Blocked: Farm26511 raw log is unavailable here, so extraction itself was not run and no causes were claimed. Commit message and `DONE` marker created.