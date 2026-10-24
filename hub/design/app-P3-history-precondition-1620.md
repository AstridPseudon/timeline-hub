Implemented the strict Gate5 history fix.

- Added `recorder_abi: 2` to the authoritative-history oracle and fixture.
- Added a wrong-ABI rejection control.
- Preserved the original journey/spec files unchanged.
- Wrote commit message and `DONE` marker.

Tests passed:

- `node --import tsx --test ...gate5-reset-precondition.test.mjs ...gate5-fault-order.test.mjs` — 2/2
- Serialized App/Node/fake-runtime `tsc` checks — passed
- Scoped ESLint — passed
- `git diff --check` — passed
- Protected six-file diff check — passed

Cause: Runtime D62 emits `recorder_abi: 2` for records with physical bindings; the prior oracle omitted this authoritative history field. No blockers.