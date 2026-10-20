# App public12 residual alias cleanup

Worker: `app-m4-public12-residual-alias-cleanup`

## Change

The embed demo now resolves the installed public Composition package through its normal package exports. Removed the private/public-source probe and the committed fallback aliases:

- Old `examples/embed-demo/vite.config.ts:2,10-35`: `typescript/src/theme-api.ts`, `typescript/src/registry.generated.ts`, the `existsSync` probe, and fallback aliases to `stubs/timeline-composition/*`, plus the package-root alias.
- New public consumers are the existing bare imports of `@banodoco/timeline-composition/theme-api` and `@banodoco/timeline-composition/registry.generated`; the package export map resolves them to `dist/theme-api.js` and `dist/registry.generated.js`.
- Deleted `examples/embed-demo/stubs/timeline-composition/theme-api.tsx` (84 lines) and `registry.generated.ts` (9 lines). Their only live references were the removed Vite fallback aliases; no copied default theme or new fallback remains.

The existing Composition package guard now includes `examples/embed-demo/vite.config.ts` in normal Vite resolution coverage and adds a Node SSR import check for the two public consumer subpaths. The guard still checks every public12 export and shared peer identity.

Also removed confirmed-dead legacy bindings:

- `tests/e2e/fake-runtime/tsconfig.json`: retired `@workspace-animations/*` path to `vendor/banodoco-animations`.
- `tests/e2e/fake-runtime/launch.mjs`: stale comment describing that mapping.
- `supabase/functions/complete_task/deno.json`: retired `@banodoco/timeline-composition` and `@banodoco/timeline-theme-2rp` mappings to deleted vendor trees. The remaining ops/schema mappings are untouched.

## Evidence for deletion

Before editing, repository searches found no fake-runtime source import of `@workspace-animations/*` and no `complete_task` Composition import. After the migration, the scoped residual search found no private Composition source path, embed stubs, fake-runtime animation path, or retired complete_task vendor mapping.

Diff size: 120 deletions and 13 guard/config additions, net `-107` lines. Product behavior, package versions, lockfile, public12 artifact, React 18.3.1, Remotion 4.0.509, and the existing 0a7b6152… artifact identity were not changed.

## Proving checks

- `node --test --test-reporter=spec config/vite/timelineCompositionPackage.test.mjs` in a private archived worktree with the checked-in public12 tarball overlaid and shared peers symlinked read-only: **PASS**, 1 file / 9 subtests (including embed normal resolution and Node SSR imports).
- `git diff --check`: **PASS**.
- `node --check tests/e2e/fake-runtime/launch.mjs`: **PASS**.
- JSON parse of `tests/e2e/fake-runtime/tsconfig.json` and `supabase/functions/complete_task/deno.json`: **PASS**.
- Scoped `rg` residual-reference check over `examples/embed-demo`, `tests/e2e/fake-runtime`, and `supabase/functions/complete_task`: **PASS**, no matches.

The same guard run directly in this worktree was attempted but could not qualify against the shared dependency tree: shared `node_modules/@banodoco/timeline-composition` is 0.0.10 while the immutable checked-in public12 guard requires 0.0.12. No shared dependency was modified; the private overlay supplied the required artifact.

## Limits

No full suite, build, browser/e2e, localhost/live-socket run, project typecheck, install, or current-release claim was made. This is source/config cleanup and package-resolution guard evidence only.
