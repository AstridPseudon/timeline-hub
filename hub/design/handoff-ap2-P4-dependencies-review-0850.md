# P4 dependency-oracle review — PASS

Independent Luna readonly review of `tl/ap2-P4-rerun-dependencies-sol-0844`.

## Qualification

**sourceREADY + OPSREADY.** The candidate is exactly one test-file oracle delta
over `2abeea693` and remains exactly one cumulative test-file delta over the
original `f5ec9ed24` port. The correction is contract-consistent: plain
`doc.patch` command `dependencies` are empty, while authoritative
`steps[].dependencies` retain the conservative timeline scope and canonical
guarded field. The independent expected plan executes the submitted retry from
the authenticated peer base; it is not response-derived.

Exact candidate identity:

- SHA `f0847d8a304c731b215b69a4c023c4a65a902931`
- tree `52a203caa936a286e7b65d26668680c1e22153f3`
- target blob `192efbfa14607f0edfb362d47d5238645c64e984`
- target SHA-256 `02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36`
- cumulative file list: only `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`
- cumulative diff: `70 insertions / 8 deletions`

The original request/base pair, raw path, authenticated peer/retry boundary,
full command records, full authoritative steps, canonical closure, opaque/null/
absence/shared identity, conflict details, key freshness, restart/readback,
show/history, digest, publisher/provider/compiler and metadata assertions remain
protected. Exact scope/ref/path/before, physical refs, key, base pair, evaluated
head, step, ordinal and phase assertions are present. No loose suffix/path-set,
either-path, fallback, or response-derived expected value was added by this
delta. The prior 32 strict negative-control categories remain unchanged outside
the positive oracle file delta.

## Evidence

- Exact named-node collect-only: **PASS**, 1 collected.
- Ruff target + neighboring ten-note file: **PASS**.
- Private-cache Mypy target + neighboring ten-note file: **PASS**.
- `py_compile`, `git diff --check`, and vendor-lock check: **PASS**.
- Offline doc.patch/error/public-command controls: **119 passed**.
- Source/AST exact independent-plan and one-file-scope audit: **PASS**.
- Runtime: SHA `a5d4258312c979024865ee704da2d632ca5b2730`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`, clean; module origins exact.
- Existing readonly `p4-v2-http-nodes` row unchanged; row SHA-256
  `fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.

## Limits / handoff

No HTTP/body/socket/browser/service/full/build/request-test run was made, and no
offline result is body credit. Manager may run exactly one changed-evidence
original node now; no further source change is recommended.
