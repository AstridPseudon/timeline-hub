# D141 REG TypeScript handoff

The two independently proved TypeScript generator regressions are repaired by normal generation from the current Runtime contract inputs. The exact generated outputs are now fresh and the required targeted tests/checks pass.

Changed paths are limited to `conformance/typescript/contract-metadata.ts` and `conformance/typescript/generated.ts`. Contract/schema inputs, all 15 canonical client inputs, tests, fixtures, generator source, and all other worktree bytes remain unchanged.

The production generator/check route is preserved. The 13 upgrade regressions remain assigned to `rt-F-D141-REG-upgrade-fix-next`; this task did not inspect or modify `runtime_protocol/upgrade.py`. Python P5 source applicability may be documented from the prior retained receipt, but this repair does not claim a new-head P5 proof or move any consumer pin.
