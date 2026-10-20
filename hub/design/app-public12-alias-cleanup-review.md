# App public12 residual alias cleanup review

Verdict: **APPROVE** the bounded source cleanup only.

- Target: `tl/app-m4-public12-residual-alias-cleanup`
- Exact target SHA: `a69b65955d130fd8bce2feecf0711532ff4fae62`
- Exact base: `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`
- Base is the target's merge-base; the target is one cleanup commit.

## Scope and negative LOC

The target changes exactly seven paths: the Vite package guard, embed Vite config, two deleted embed stubs, fake-runtime launch/config, and `complete_task/deno.json`.

Diff is **120 deletions / 13 additions, net -107 lines**. The deleted stubs account for **93 lines** (84-line theme stub plus 9-line registry stub). No `src/` product path, root package pin, lockfile, runtime lock, codec/deserializer/writer, or full-contract source changed.

The embed config now relies on the normal bare public exports `@banodoco/timeline-composition/theme-api` and `@banodoco/timeline-composition/registry.generated`; private `typescript/src` probes, fallback aliases, and the package-root alias are gone. Fake-runtime's dead `@workspace-animations/*` path/comment and `complete_task`'s dead Composition/theme vendor mappings are removed. The retained `timeline-ops` and `timeline-schema` mappings are unrelated and unchanged.

## Identity and behavior boundaries

The target preserves the exact public12 root tuple: Composition `0.0.12`, artifact SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a`, 58,444 bytes / 77 regular archive members, React/React DOM `18.3.1`, Remotion and all relevant Remotion peers `4.0.509`. `package.json`, `package-lock.json`, and `runtime.lock.json` are byte-unchanged against the base.

No renderer/evaluator, registry, theme, mount, unknown-component, public-default, or SSR implementation was edited. Existing custom-registry/unknown/mount/public-default behavior remains in the unchanged source/test cohort. The new guard checks the actual installed public package exports and SSR imports, rather than mirroring implementation files.

## Proving checks

All checks used a temporary target snapshot. The public12 package was extracted into a private `node_modules` overlay; every other dependency was symlinked read-only from the shared tree. No shared dependency, runtime, or cache was changed.

- `node --test --test-reporter=spec config/vite/timelineCompositionPackage.test.mjs` — **PASS**. The guard executed the root artifact identity check, seven Vite configurations including `examples/embed-demo/vite.config.ts`, all public export-map subpaths from App and Astrid importers, shared peer identity, and Node SSR imports of `theme-api` and `registry.generated` (9 checks in the file).
- Scoped residual `git grep` checks over embed, fake-runtime, and `complete_task` — **PASS**: no private Composition source/stub paths; no fake-runtime retired animation mapping; no retired `complete_task` Composition/theme mapping or import.
- `node --check tests/e2e/fake-runtime/launch.mjs`, JSON parsing of both edited JSON files, and `git diff --check 85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c a69b65955d130fd8bce2feecf0711532ff4fae62` — **PASS**.

The shared dependency tree exposes Composition `0.0.10`, so a direct shared-tree public12 guard would be an environment mismatch, not product evidence. The qualified run used the private immutable `0.0.12` overlay. A first combined residual scan was intentionally overbroad and caught the retained, unrelated embed `@workspace-animations` alias; the scoped checks above exclude that valid existing alias and pass.

## Remaining closure limits

This approves the bounded cleanup, not the overall App/M4 integration or current-release claim. Per instruction, no full suite, build, browser/e2e, localhost/live-socket run, project typecheck, or install was run. The embed build itself is unverified; only its real Vite resolver path and the package's Node SSR imports were checked. Full behavior qualification for custom registries, unknown diagnostics, mount behavior, public defaults, and renderer parity remains with the existing package/source suites and the central integration qualification.

No ledger row was changed, no integration-deletion claim was made, and no KEEP approval is requested.
