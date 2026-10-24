## Result: open; no count credit

Created [inverse22-qualification.json](/home/user/work/wt/agt-F-inverse22-evidence-0526/evidence/inverse22-qualification.json).

- Identified all 22 exact nodes: 16 corruption cases and 6 retained-scope cases, all phase `call`, owner `Agent`.
- Retained full25691 result: `17159 passed, 262 failed, 5 errors, 4 skipped`; all 22 exact nodes failed with `inverse needs authenticated physical binding normalization`.
- Prior R2 evidence remains limited to `56 + 14` (plus reused `186` controls); it does not enumerate these 22 selectors.
- The later `47 passed` fixture packet used a modified test body (`f416…`), not the original full25691 body (`1dc6…`).
- Current `2007cf7aaf` tree: `68b0309c…`; relevant production hashes differ from reviewed `114694ad…`, so current equivalence is unproven.

Checks:

- `python3 -m json.tool evidence/inverse22-qualification.json` — PASS
- `git diff --check` — PASS
- No product/test changes.
- No tests, probes, body reruns, or full suite were run.

Smallest next qualified command is recorded in the evidence artifact: run only the two parameterized test functions on current qualified Agent/Runtime source with exact node and import-origin capture.