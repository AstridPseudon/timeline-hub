# P4 ten-records independent review handoff

**PASS — source-qualified; live body intentionally unverified.**

## Identity

- Final SHA: `148235cd8478764940dc116d3a4e3a89040f137a`
- Final tree: `b42919b24d27675b4da95339608b06147c244261`
- One-file changed blob: `94069d2cff0d0d479c19128b4e149bb8206855d7`
- Base: `f5ec9ed242c6b84aa35743e9e3741088c3e96a87`
- Candidate delta against `tl/ap2-P4-public-command-testport-0755`: only
  `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.
- Conflict/rerun test unchanged: blob `72d11a2a8f9f8915a22e325bc15f2edadbae96ff`.

## Review result

The added `expected_plan` is computed solely from the authenticated pre-edit canonical
closure, captured request, and base head. It is created before reply assertions and never
uses `data`, `result`, `receipt`, or stored history. The reply's `data["commands"]` is
compared to the full authoritative `expected_plan.records[*]["command"]`; stored history
records and steps, label, merge mode, schema, and undo metadata are also compared to the
same plan. The nested projection compares every submitted field at the nested command
boundary.

Offline evidence: ten records/steps; seven authoritative enrichment fields beyond the
five submitted fields; 50/50 submitted-field mutations rejected by the candidate oracle;
5/5 provider core-field mutations rejected by the real command engine.

Original seed, ten notes, shared physical closure, public `timeline.open`/`command`/
`commit`, exact v2 request shape, canonical/digest/head/receipt, step patches,
show/history, restart, per-step undo/redo, and non-note preservation remain. The
separate conflict/function-rerun test and its structured diagnostics are unchanged.

## Commands and readiness

- Named collect-only for
  `tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`: **PASS**, 1 collected.
- Scoped Ruff: **PASS**.
- Private-cache Mypy: **PASS**, no issues.
- Syntax compile and `git diff --check`: **PASS**.
- Runtime pin `a5d4258312c979024865ee704da2d632ca5b2730`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`, clean: **PASS**.
- Module origins for Runtime/provider and Agent generated client: **PASS**.
- Existing `p4-v2-http-nodes` row: exactly one, unchanged; row SHA-256
  `fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.
- Runtime vendor-lock check: **PASS** (`ok runtime.lock.json`).

Body limits: no live HTTP/body, browser, socket/service, full suite, build, or central
test-service request was run. The central owner should run the exact named node once.
