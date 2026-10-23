# Agent P4 rerun owner review 0904

**PASS — source/owner review only.**

Reviewed `de046064f1632eef96bf08289f50a6ec3fefe4a3` on current base
`2e12b49ba`. The commit contains only the new
`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` test. Its exact
blob is `192efbfa14607f0edfb362d47d5238645c64e984` and SHA-256 is
`02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36`, matching
the independently reviewed Proof0850 donor.

The test keeps the real public `timeline.open()` → `commit(fn)` route and
normal generated HTTP transport. It checks the actual 200/409/200 conflict
rerun sequence; exact original/retry head pairs, request/key/command/step
predicates; independently planned retry; canonical closure and shared
physical identity; authoritative records/steps/dependencies; structured
conflict details; receipt and persisted history; fresh authenticated
re-evaluation; restart/readback; and outbox cleanup. The empty raw dependency
captures are checked only alongside the retained authoritative step scope and
field dependencies.

No product ancestry or dependency/pin/schema/generated-file change was
imported. Existing normal34e/d106 and all other product/test bytes are outside
the one-file addition. No casts, fabricated document/cache, fake runtime
shortcut, or dropped negative assertion was found.

## Commands and results

- Exact Runtime `a5d4258312c979024865ee704da2d632ca5b2730` / tree
  `f74b016ea837f8148db4a602c972073a226ed177` was archived privately for the
  collection environment; shared Runtime was untouched.
- Integration collect-only for the rerun node: **PASS, 1 collected**.
- Scoped Ruff on rerun + ten-note neighbor: **PASS**.
- Private-cache Mypy on rerun + ten-note neighbor: **PASS, no issues in 2
  source files**.
- Private-cache `py_compile`: **PASS**.
- `git diff --check`: **PASS**.
- Exact SHA/tree/blob/SHA-256, one-owncommit, one-path, and outside-file audit:
  **PASS**.

## Limits

The HTTP body is intentionally unrun here. No full/native14/crash24/browser/
journey/new-service run was made. Proof owns the one integrated original node
after home merge; this report gives no behavioral body credit.
