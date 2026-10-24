## Report — FAIL/HOLD

Reviewed commit `434feb92d3` against `c5525bffa6`; no worktree changes made.

The protected-body/tail/native/encoded authentication, Runtime blob mappings, source guards, registry checks, wrapper probes, and optimized-mode controls all passed.

Commands/results:

- `python3 caller-publication.py` — PASS
- `python3 -O caller-publication.py` — PASS
- 20 distinct negative controls in both modes — all `rc=0` (refused as intended)
- `py_compile` normal/`-O`, JSON validation, `git diff --check` — PASS
- `caller-publication.py` SHA256 matches required `97e36cb460f8a20676f28368e9788950e0b7a5b1e641dd57c0ebe43944b25adf`

Current paired tuple was stable during both preparations:

- App `971a29e…`, tree `349691b…`
- Agent `47b744d…`, tree `68a7300…`
- Runtime `becfe6d…`, tree `7edc08e…`
- All clean on `tl/integration`

Dry source guards ran first: P2 `0.150/0.181s`, P3 `0.235/0.203s` normal/`-O`.

Remaining source defect: `REQUEST_FIELDS` contains 60 names and `REPLY_FIELDS` 148, while the authoritative generated-type closures contain exactly 51 request fields across 22 types and 133 reply/history fields across 53 types. The candidate includes all required fields, including `receipt_id` and `idempotency_key`, but also 9 request extras and 15 reply/history extras. Therefore the claimed exact C0 inventory is not actually represented or enforced.

No live service, browser, backend, HTTP, installation, or full suite was run. Commit message and `DONE` marker were written.