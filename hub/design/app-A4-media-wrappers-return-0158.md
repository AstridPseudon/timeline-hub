## Report

- Removed `applyProvisionedMediaCommandToConfig` from [config/contracts/registry.json](/home/user/work/wt/app-A4-media-wrappers-return-0158/config/contracts/registry.json).
- No generated inventory required; registry is hand-maintained.
- Three original A4 source files remain unchanged.
- Scope: one file, one deletion. No blockers.

Checks passed:

- `/opt/node20/bin/node scripts/quality/check-contract-governance.mjs`
- `npm run check:contracts`
- `npm run check:contract-surface-map`
- `npm run check:sdk-public-exports`
- Locked Root/App/Node `tsc --noEmit --incremental false`
- `git diff --check` and scope/outside validation

Independent source-test PASS was reused as instructed because no runtime source changed. Commit message and `DONE` marker created.