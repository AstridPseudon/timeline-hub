## Result: FAIL

Found one remaining defect:

- `preflight.py:431-458` validates the six test modules’ imports but never compares their recorded SHA-256 hashes. A changed test body with unchanged imports could pass preflight, violating the unchanged-test-hash requirement.

Validation passed:

- Exact Ruff/config: PASS
- JSON, private compile, diff check: PASS
- Frozen hashes/AST manifests: 21/21 and 7/7 PASS
- Venv/system negative censuses: all 7 imports attempted; refusal before body
- XML positive/malformed/missing controls: PASS

Actual Farm preflight and six-file pytest body: **NOTRUN**.

Evidence: [findings.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-Farm-preflight-final-review-2135/evidence/findings.md).