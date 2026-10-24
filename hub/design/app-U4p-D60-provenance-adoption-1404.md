## U4p report

Adopted Runtime producer e68 through the normal sync tool. Only [runtime.lock.json](/home/user/work/wt/app-U4p-D60-provenance-adoption-1404/runtime.lock.json) changed:

- source: becfe6d… → `e68cf231641db98a72805a586b51ab5c4fae2c16`
- producer version: `sha256:650857…` → `sha256:9af2df…`
- producer tree: `a2cbedd185c7e576e20ed060d993deba17111b78`
- parents: `becfe6d… 60e7838…`
- manifest: `contract/artifacts.json`, 80 artifacts
- mappings: 14; all before/after/producer/manifest hashes identical

| App output | Runtime source | Hash |
|---|---|---|
| `commit_conflict_409.json` | `conformance/responses/commit_conflict_409.json` | `e06c5818…` |
| `events_page_1_200.json` | `conformance/responses/events_page_1_200.json` | `6aaaabe5…` |
| `events_page_2_200.json` | `conformance/responses/events_page_2_200.json` | `d5bffdc9…` |
| `invalid_cursor_400.json` | `conformance/responses/invalid_cursor_400.json` | `16a02d8…` |
| `managed_outputs_200.json` | `conformance/responses/managed_outputs_200.json` | `6bcef19a…` |
| `not_found_404.json` | `conformance/responses/not_found_404.json` | `4a40fedb…` |
| `retired_route_410.json` | `conformance/responses/retired_route_410.json` | `e3b43083…` |
| `task_admission_201.json` | `conformance/responses/task_admission_201.json` | `108559a9…` |
| `task_read_200.json` | `conformance/responses/task_read_200.json` | `cc590c4f…` |
| `validation_error_422.json` | `conformance/responses/validation_error_422.json` | `2a02a914…` |
| `generated-contract-metadata.ts` | `packages/typescript/src/contract-metadata.ts` | `1028aaec…` |
| `generated.ts` | `packages/typescript/src/generated.ts` | `7be7f351…` |
| `timeline-commit-types.ts` | `packages/typescript/src/timeline-commit-types.ts` | `bf472883…` |
| `timeline.schema.json` | `contract/schemas/timeline-config.schema.json` | `4d74a4ae…` |

Tests:

- Sync tool: passed.
- Producer-aware vendor-lock check: passed.
- Vitest vendor-lock + recorded responses: 37/37 passed.
- Schema guard: 2/2 passed.
- `git diff --check`: passed.
- Initial `--configLoader=runner` attempt failed before collection due existing `__dirname` config incompatibility; normal bundled loader passed.
- No full/browser/service tests run.

No blockers. Commit message and `DONE` marker created; no commit performed.