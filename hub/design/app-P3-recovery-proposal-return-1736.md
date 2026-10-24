## Report

Created:

- [proposed-v2.patch](/home/user/work/wt/app-P3-recovery-proposal-return-1736/proposed-v2.patch)
- [proposal-evidence.txt](/home/user/work/wt/app-P3-recovery-proposal-return-1736/proposal-evidence.txt)

The v2 proposal restarts Runtime before reopening, arms route observation before production automatic recovery, verifies delivery to the new Runtime origin, and preserves exact A/B payload, ordering, history, canonical, reset, legacy, and undo assertions. No source files were modified.

Validation:

- `git apply --whitespace=error --check proposed-v2.patch` — PASS.
- Existing Gate5 controls — PASS, 3/3.
- Private fast/slow lifecycle and negative schedules — PASS, 6/6.
- Node20 ESLint — PASS.
- Node20 virtual TypeScript comparison — PASS, zero new diagnostics.
- Protected source hash: `a6468188…`
- Virtual-after hash: `fe8a4666…`

Unverified: no browser, Runtime service, original P3, or full-suite run. ORCH approval and independent review PASS remain required before applying.