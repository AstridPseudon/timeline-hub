# App M2 Gate5 — seven-case native Agent-helper migration

Status: partial candidate, blocked on a frozen S2 public SDK surface. No behavior assertion was weakened, deleted, skipped, or marked expected-to-fail.

## Exact source

- App worktree: `/home/user/work/wt/app-m2-sevenjourney-native-agent-migration`
- Base App commit: `b1ef4b9b910ba72375c34cf319692f90d22edc25`
- Base App tree: `8d8a10b057ed31fed69517e18a23b8ec3811447a`
- Frozen Agent source checked: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Frozen Runtime source checked: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Changed files: `tests/e2e/local/support/astrid.ts`, `tests/e2e/local/three-products.spec.ts`

## Old-to-new mapping

| Existing Agent helper write | Candidate native path | Result |
| --- | --- | --- |
| `timelines checkout` + `timelines edit --swap-asset ...=task:<id>/marker#0` + `timelines publish` in marker case | Resolve the immutable managed-output row, then use exact five-field media selection/provider reads and `occurrence.swap-media` | Blocked before capture: frozen S2 has no public SDK media-selection/provider read. The seeded `f2-placeholder` is also an ingested object, not a managed generation/variant, so it cannot supply the required old five-field selection. No private generated-client bypass, fake provider, manual SQL, or legacy writer was added. |
| `timelines checkout` + `timelines edit --extend 1` + `timelines edit --clear-asset` + `timelines publish` in concurrent case B | One `timelines.commit` made by `AstridCli.commitCaptured`, containing bounded native `clip.set` commands: `hold = current hold + 1` and explicit `clear: ['asset']` | Migrated. The App-owned transition clear remains in case C, preserving the original ordering and Keep/Use latest assertions. |

The retained helper still uses CLI reads (`status`/`show`) and the fixture preflight checkout/check/discard. Only the retired Agent publication writes were removed from `agentOf`.

## Native controls used

- `capture_clip_set(... values={'hold': ...})` for extent-preserving hold extension.
- `capture_clip_set(... clear=['asset'])` for explicit asset removal.
- Runtime commit endpoint with the original pinned `base_revision_id` and `base_publication_id`.
- Marker case is deliberately fail-closed until the supported five-field selection/provider read exists; its adoption, opaque-data, root/asset, reload, and follow-on App assertions remain intact.

## Checks

- `./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts tests/e2e/local/support/astrid.ts --no-cache --max-warnings 0` — passed.
- `git diff --check` — passed.
- Browser/e2e/full suites were not run, per task instruction. The seven-case lane is not a passing gate candidate because marker case reaches the documented public-SDK gap.

## Unsupported gap / proposed ledger entry

Proposed ledger entry: “App Gate5 marker migration requires public Astrid SDK wrappers for Runtime `get_project_media_selection` and `get_project_verified_media`, plus a managed five-field old-media selection for the seeded clip. Until then, retain the marker assertions and fail closed; do not delete the old behavior contract or create a compatibility writer.”

Recommended next step: expose and qualify the exact public selection/provider read against the frozen Agent/Runtime pair, or replace the fixture’s placeholder with a real managed generation/variant while preserving the same assertions. Then implement `occurrence.swap-media` with both verified selections and run the central gate once.
