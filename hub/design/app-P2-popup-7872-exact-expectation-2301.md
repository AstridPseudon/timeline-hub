## Report

Implemented the strict P2 popup oracle correction in `three-products.p2-popup.spec.ts`.

- Captures raw pre-gesture revision JSON.
- Derives parent digest and revision identity independently via Runtime canonicalization.
- Preserves full document deep equality and reload/undo assertions.
- Retained values:
  - Parent digest: `sha256:4293ed...09103b1`
  - Parent revision: `authoring-parent-revision-c8b8...c03e0ff`
- Old JS expectation reproduced RED; four payload/digest/revision/unrelated-field mutations failed equality.

Checks passed:

- `tsc -p tsconfig.node.json --noEmit`
- `tsc -p tsconfig.app.json --noEmit`
- `tsc -p tsconfig.json --noEmit`
- Scoped ESLint with `--max-warnings=0`
- Node popup oracle controls: 2 passed
- `git diff --check`

Source SHA: `f2d63c703ba506b52dfd8bb0ebaee56ed3f1f58600650c36f09ceaa76a154d10`. Neighboring readiness SHA unchanged.

Vitest cannot collect the existing `node:test` oracle file; no browser/original body was rerun per D83. Independent reviewer should qualify and run one original case.