# A3/P2 report

Implemented managed single-image hover/commit alignment.

Cause: generic hover resolved retained `(368,54)` to `V3/4.5`; semantic managed placement resolved through the existing asset planner to `V2/9`.

Fix: threaded a managed-image intent through the real external-drop caller/coordinator and reused `planAssetDropTarget`. No media identity or duration was fabricated; existing 5s image semantics remain authoritative. Parent `V1/5`, generic behavior, and guards remain unchanged.

Evidence:

- Focused Vitest: 4 files, 37 tests passed.
- Root/app/node TypeScript checks: exit 0.
- Scoped ESLint: passed, `--max-warnings 0`.
- `git diff --check`: passed.
- `--configLoader runner`: blocked by pre-existing `__dirname is not defined`; equivalent `bundle` run passed.
- No browser, full suite, build, install, or service run.

Base SHA/tree: `a90d4251cac526dd2723e037e5c91d4b547dc56a` / `8007f39e5de281f4b47a5b93cf7650b394081e9b`.

Changed blobs include:

- `drop-position.ts`: `b1debc1f2b6ec595c22fbbd50079a66ff99dc1ba`
- `external-drop-utils.ts`: `bd74a756d8df9460a5719a966b11a489390a3afc`
- `useDragCoordinator.ts`: `c5985512aa7c476d880562ec3a088134c68a1397`
- `useExternalDrop.ts`: `33c59ddbb14cf17fa9faa7c63469be0be5ec14d3`

Predicate map: old generic `V2 → V3/4.5` remains asserted; managed preview is `V2/9`; mounted semantic request matches preview track/time; stale scope/head/occurrence/row/media/registry guards pass; parent and generic paths remain covered.

No external ledger/body/receipt changes. `DONE` and commit message were written.