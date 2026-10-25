# Report

- Verdict: qualified `ab1e` grouped inverse/redo correction does not cover the App graph child-alias seam.
- Proved missing applicability: Runtime auth handling is limited to `occurrence:<id>/collection:track`; graph adds `collection:clip` and `clip:title`.
- Exact causal owner remains `UNKNOWN`; accepted records, stage ranges, physical bindings, closures, and continuations are `EXACTMISSING`.
- D130 SWAP/WAL scope remained held and untouched.
- No product or test changes made.

Evidence:

- [applicability.json](/home/user/work/wt/rt-R2-graph-boundary-applicability-1744/evidence/applicability.json)
- [source-manifest.json](/home/user/work/wt/rt-R2-graph-boundary-applicability-1744/evidence/source-manifest.json)
- [validation.md](/home/user/work/wt/rt-R2-graph-boundary-applicability-1744/evidence/validation.md)

Checks: AST, source predicates, graph source checks, JSON parsing, `git diff --check`, and source-diff checks all passed.

Tests were not run by this read-only task. Retained evidence: graph set `8 PASS / 1 FAIL`; original `[True]` case `1 FAIL` during redo-birth. `DONE` and commit message were written.