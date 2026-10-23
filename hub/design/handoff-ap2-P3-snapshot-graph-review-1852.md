# P3 snapshot-graph review 1852 — bounded transport

Verdict: **PASS for the final post-eval source boundary only**. This is not
Farm preflight or Gate-5 acceptance evidence.

## Exact flat replacement

Apply exactly one replacement in Farm's already-current
`ap2-P3-gate5-h6-0348` row. Refuse if the old primitive occurs zero or more
than once. Do not rewrite or regenerate the row.

Old primitive (unique occurrence required):

```sh
test "$(git rev-parse HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c
```

New primitive:

```sh
( test "$(git rev-parse HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c ||
  test "$(git show -s --format=%P HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c ) &&
test "$(git rev-parse HEAD^{tree})" = a3ff3584e9b559bbb3c3a82b77be7516ed8e761c
```

The complete `%P` comparison is intentional: it admits exactly one parent,
not `HEAD^` alone, an arbitrary ancestor, an equal-tree commit, or a merge
parent. Applying this replacement must preserve every other Farm byte,
including the actual mounted-test hashes and the Farm `GRAPH` path, until
Farm qualifies its own graph. Do not send or adopt the whole local row.

## Reviewed identity and row evidence

- App source: `2107e1870e51c650d59315f4cc1ab6af338f198c`.
- App tree: `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`.
- Actual 2107 has two parents, so the direct-source arm is required for the
  real checkout; the synthetic Farm snapshot is accepted only when its full
  parent list is exactly the single 2107 hash and its tree is exactly a3ff.
- Target row: `tests/suites.conf:36`, one row-name occurrence.
- Current row SHA-256 including newline:
  `6a1934adad23a6233ba96cce84feffeaa8bf320ff046c843052d92a5171989c4`.
- Outside-P3 config digest:
  `e6d4d240181975d560f6c8e7177911dcc231ae7229fabd89eee5653bd5de0153`.
- New source primitive count in the target row: 1; tree guard count: 1;
  stale direct `58bf24ce…` source primitive count: 0.
- Existing source, tree, clean, ancestry, blob, producer, resolver, pin,
  body, 55 protected-property, and 21 AST guards remain in scope. The full
  v2 request fields (`api_version`, `scope`/base pair, `commands`, `label`,
  `steps` with id/label/intent/tags/command ordinals/patch/reads, `merge`,
  `reads`, key, `dry_run`, source, rationale, `group_id`) and full
  `{data, receipt}` accepted/merged/historical/rebased/head/document/records/
  dependencies/effects/steps/history/undo_steps/preview/would_status/
  conflict-reason-head/invalid-code-path-hint-command reply fields remain
  untouched, as does the original Gate-5 caller.

## Farm boundary and graph handoff

Farm evidence remains limited to the retained 3794/29449 result: provisioning,
report-all setup/actual-beforeAll, and native 21 seed were green; original
37ca Gate-5 was **NOTRUN**. Diagnostic 30416 skipped guards and is not
acceptance evidence. The local proof row may contain stale `58bf`-era
`useTimelineSave.test.tsx` and P1-spec expected hashes; Farm bench2 correctly
re-derived the actual 2107 values
`bd6adf9ad6b2cd9fcde594a41120e10d4c5c249274186b89a004b41d5a37af82` and
`074ecd9e6408218633bc6a997e509459f2034321a655d1555de38dc8f37cdca3`.
This review does not claim local whole-row or whole-environment readiness.

For Farm's graph qualification, reuse the existing
`scripts/testing/auto-real-proxy-main95.mjs::prepareNodeModulesOverlay`
workflow with an own Farm worker worktree as `appRoot`, a physically private
`privateRoot`, and the existing dependency root read-only. Use the tracked
physical Composition archive
`vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`
unchanged: version `0.0.14`, 73,451 bytes, SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, and
80 regular files. Preserve the existing SRI, public exports, resolver-origin,
source-pin, lock, and clean-source guards. Only helper-owned physical Vite /
Rollup copies may be private; ordinary/scoped dependencies remain links to
the read-only shared install. Generated exports must resolve to
`dist/effects.generated.js`, `dist/animations.generated.js`, and
`dist/transitions.generated.js`. No package-root generated modules,
package-root TypeScript, source fallback, repack, pin change, shared install
write, Remotion-graph substitution, 80-file skip, or new launcher/code is
permitted. No graph build was performed here.
