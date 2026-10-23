# Handoff: app-F-exports-public-graph-1054

The three `@workspace-*` alias failures are fixed by adding the vendored
effects, animations, and transitions aliases to
`config/testing/vitest.config.ts` and `config/testing/vitest.boundary.config.ts`.
Production `config/vite/vite.config.ts` public Composition export resolution is
unchanged. `vendoredTimelineCompositionAliases.test.ts` is unchanged.

The exact pinned archive is version `0.0.14`, SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. A private
overlay run of the original focused tests still fails the same three renderer
tests (3 failed / 16 passed): the archive emits `bundled:2rp@0.1.0` rather than
the test's `timeline-theme-2rp` source identity, and the two public-host
failures remain undefined installed Astrid catalog components. Tests were not
weakened. App typecheck, scoped ESLint, and `git diff --check` passed. See the
worker `report.md` for exact commands, baseline identities, and failure traces.
