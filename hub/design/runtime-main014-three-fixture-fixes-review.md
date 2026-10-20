# Runtime main014 three-fixture-fixes review

## APPROVE

Independent review approves candidate commit
`0bc1e7a5f239dff2b14158a6dfb0b8006b749b56` (tree
`a122d1f32a1e2839384ac60215960e13d17d09c2`) against baseline commit
`6e845a187684919c162b29568496c015bda1a591` (tree
`7f11d7e159d46a88a22111c414aa7bdf7b599d9d`).

## Review findings

- The candidate changes only `tests/test_timeline_authority_door.py` and
  `tests/test_timeline_shot_authority.py`. `git diff --name-status` shows no
  product, schema, CAS, or artifact paths; therefore the 76 artifact bytes
  remain identical to `6e845a`.
- The foreign-shot assertion at
  `tests/test_timeline_authority_door.py:104-113` is a legitimate boundary
  correction. Runtime’s unchanged `_require_project_shot_scope` at
  `runtime_protocol/service.py:3526-3531` deliberately maps a foreign catalog
  row to `NotFoundError`, so 404/`not_found` is the nondisclosing contract.
  The same parameterization retains 410/`retired_route` for timeline,
  document, and render families. The unchanged credential-first test at
  `:71-87` still requires 401 and a byte-for-byte no-write snapshot, and the
  unchanged owned catalog positives include
  `tests/test_runtime_e2e.py:222-264` and
  `tests/test_project_shot_catalog_custody.py:129-179`.
- The timestamp update at `tests/test_timeline_shot_authority.py:324-332`
  targets only the one `shot.text_binding.set` receipt for the copied fixture’s
  pinned binding. Archive/backup bytes are not changed, the request hash and
  exact key identity are still checked at `:352-362`, and the exact retry still
  asserts receipt-only replay, unchanged DB/CAS snapshot, unchanged
  `total_changes`, and unchanged binding at `:370-391`. It changes no Runtime
  expiry logic or authority/history behavior.
- Existing expiry and restart controls remain untouched: the actual expiry
  assertion is in `tests/test_spec_dedup.py:111-143`; a real text-binding
  exact retry after daemon restart remains covered by
  `tests/test_shot_text_bindings.py:83-140`. The retained rationale is also
  preserved: fixture freshness is limited to the ephemeral copied receipt,
  while production expiry, exact request identity, no-write behavior, and
  restart replay remain exercised elsewhere.

## Evidence read

- Exact three-node full result on the pre-repair candidate tree
  `7f11d7e159d46a88a22111c414aa7bdf7b599d9d`: the three failures were exactly
  the foreign-shot 404/410 assertion and the service/HTTP historical exact
  retries; the other 245 entries were setup errors, not additional product
  failures (`rt-m2-main014-corrected-current-candidate-compose-full-1020230205-26822`).
- Repair worker’s local exact service node: `1 passed`; local HTTP nodes were
  socket-blocked by the sandbox.
- Central direct-neighbor run on candidate tree `a122d1f32a1e2839384ac60215960e13d17d09c2`:
  `python -m pytest -q tests/test_timeline_authority_door.py tests/test_timeline_shot_authority.py`
  — `112 passed in 61.77s`.

No full, browser, renderer, pin, or broad unchanged-suite run was performed
for this review.
