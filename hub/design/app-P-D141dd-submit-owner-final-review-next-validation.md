# Validation

- Exact unchanged checker: `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/candidate/check.sh` — exit 0; 43 controls PASS; stderr empty.
- New run retained at `.../private-controls/runs/20261026T110739-4`; stdout, stderr, and exit are retained under this worker's `evidence/private-controls/`.
- Checker validation: AST/private-cache compile PASS; `bash -n` PASS; Node syntax check PASS; Ruff `--select F` PASS; source and outside conservation PASS.
- Historical read-only check: four exact detached clean source pins and five existing native IDs PASS; no service operation.
- Reviewer-owned disk trace: 5-second interval samples, standing 4GB stop not reached, sampler signalled and reaped. First-tool coverage is explicitly NOT MET because it began after the checker; no backfill.
- Product typecheck/lint/tests/full/browser are N/A and were not run; this task is source-only and the product tree is unchanged.
