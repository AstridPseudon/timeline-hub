## Report

- Added [evidence/g4-managed-duck-0856.row](/home/user/work/wt/agt-G4-duck-row-0856/evidence/g4-managed-duck-0856.row).
- Corrected snapshot guard to require:
  - `HEAD^ = 0ff3d103…`
  - exact tree `1d613f…`
  - duck blob `cfcf373a…` and 17 assertions
  - Runtime `becfe6db…`, auth blob `979225ab…`, SHA-256 `e172f8c5…`
- Kept explicit HOLD for missing installed child, profile, and managed Store receipt.
- Preserved shared shell environment, `--noprofile --norc`, selector forwarding, and failure propagation.
- No product or registry changes.

Validation passed:

```text
bash -n: PASS
stdlib shlex/serialization/source/tree/AST checks: PASS
synthetic selector/failure propagation: PASS
git diff --check: PASS
```

No actual child, profile, receipt, imports, preflight, pytest, service, or full-suite execution was performed.

Commit message written and DONE marker created. Independent no-weakening review and genuine receipt binding remain required.