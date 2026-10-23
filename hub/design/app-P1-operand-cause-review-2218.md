## Result: PASS — Sol2218 `PRODUCTDEFECT`

- Classification: `PRODUCTDEFECT`
- Custody: PASS. Safe diagnostic is 144,118 bytes, SHA-256 `faa0df...e4b0f`; no credentials, headers, cookies, principals, raw requests, receipts, full URLs, or raw trace exported.
- Sourcepath: PASS. At base `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a`, production flow is:

  `useTimelineSave.ts:231` → `buildTimelineData` → `timeline-data.ts:461` → direct `adoptCanonicalData` → `checkSource`.

Evidence:

- Retained resource `244e06481d456bb90e1128e571f8efaa574adde6.json` parsed successfully.
- Canonical document and receipt result are identical; accepted revision/project/timeline match the safe head.
- Parent output contains `resolution`, `fps`, and `file`; `background` and `background_scale` are absent.
- Production reconstruction results:

  - source vs loaded: `false`
  - source vs projected: `false`
  - registry vs projected registry: `true`
  - excluding output: `true`
  - meaningful differing fields: exactly `output.background`, `output.background_scale` (absent vs `null`)
  - selected clip numerics: `from=0`, `to=8`, `hold=2`, `speed=1`, `at=0`

- Real `createTimelineLocalSaveHandoff` source reproduced `TimelineVersionConflictError` before `appendDocument`; append calls: `0`.
- `commitData` directly adopts `nextData`; no intervening normalization was found.

Commands/results:

```text
git rev-parse HEAD
PASS: e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a

sha256sum app-P1-24510-safe-diagnostic-2201.json
PASS: faa0df373a0ae84dfd3ba56aab81988a65435c31b339ec91864be1bb299e4b0f

offline Node production-source probes via node --import tsx loader
PASS: all comparison and handoff assertions

git diff --exit-code
git diff --check
git status --short --branch
PASS: clean worktree
```

No product or test changes were made. No full suite, browser, live HTTP, backend, Agent move, Runtime 409, or rollback was run. Historical mounted operands remain unrecorded; those values are reconstructed from the retained canonical document and production source.