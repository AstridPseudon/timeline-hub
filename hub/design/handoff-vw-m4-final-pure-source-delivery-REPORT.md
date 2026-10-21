# Composition final pure-source delivery

## Result

Refreshed the Composition source-only delivery from the actual final
`tl/integration` source `7bb54bbd64107e5090643ecca1e4d33164173e85`.
The retained patch, bundle, manifest, path lists, and command log are under
`delivery/`. No product source was changed in this worker tree.

## Exact source and frontier

| Item | Value |
| --- | --- |
| Source ref/commit | `tl/integration` / `7bb54bbd64107e5090643ecca1e4d33164173e85` |
| Source tree | `20467712e66dbadff4d562c0d5baae22b8c077a7` |
| Base ref/commit | `origin/main` / `67b8aa3d0d6831d3e3504a340ff583c3da253707` |
| Base tree | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` |
| Main-to-source changed paths | 116 |
| Source tracked paths | 119 |
| Source tracked modes | 119 paths, all `100644` |
| Changes since superseded `4788e107f` | 17 paths |

The exact 17-path final delta from `4788e107f` is retained in
`delivery/prior-to-source.paths`; it includes the build/projection and
generated-metadata files:

```text
.gitignore
Makefile
README.md
package.json
scripts/build-remotion-primitives.mjs
scripts/build-remotion-primitives.test.mjs
scripts/build-typescript.mjs
scripts/build.mjs
scripts/gen-registry.test.mjs
scripts/gen-registry.ts
typescript/src/animation-metadata.generated.ts
typescript/src/animations.generated.ts
typescript/src/lib/clip-look.ts
typescript/src/lib/remotion-primitives.generated.d.ts
typescript/src/scene-evaluation.ts
typescript/tests/animations.test.ts
typescript/tests/remotion-primitives.test.ts
```

## Delivery artifacts

| Artifact | SHA-256 | Bytes |
| --- | --- | ---: |
| [source patch](delivery/composition-origin-main-to-7bb54bbd.patch) | `327178ed354ed9f624addecd86f859820f0607b27d779d9f355adcce84f50063` | 492080 |
| [source bundle](delivery/composition-origin-main-to-7bb54bbd.bundle) | `f06812274384792bb6a3d5103448d3eada33ca6f869550ce463481f60e615981` | 234407 |
| [manifest](delivery/composition-origin-main-to-7bb54bbd.manifest.json) | `e4cad42b1106bbd85eb6d3440a6eba2c215d38d1e3ee0a392366cd68c3c6db5d` | 13769 |

The bundle verifies with head `7bb54bbd... refs/heads/tl/integration` and
requires `67b8aa3d...`. The manifest records the complete 116-path frontier
and all 119 target paths.

Scanner/carrier inputs were hash-checked only and not invoked or copied:

- scanner 1.0.8: `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- carrier: `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`

## Commands and results

- `bash -n .../COMMAND` — **PASS**.
- `bash .../COMMAND` — **PASS**. The command validated clean worktree and
  exact refs/trees/ancestry; wrote the patch and bundle; ran `git diff --check`;
  verified bundle head/prerequisite; applied the patch to a fresh Main archive;
  reverse-applied it; and compared every tracked path by SHA-256 bytes and
  stat mode.
- Fresh-main forward apply — **PASS**; patched tree equals source for all 119
  paths.
- Fresh-main reverse apply — **PASS**; reverse tree equals fresh Main for all
  29 paths.
- `git status --short --branch` — **PASS**; worker worktree remains clean.

The private regenerated proof tree was removed after comparison. No build
output remains in the worktree.

## Not run / next step

Per the brief, no product tests, full suite, browser, physical run, npm 0.0.14
archive, scanner/carrier execution, or whole-repository ZIP was run. Package
packing remains held for the authorized actual-13 physical attempt. The
Runtime/delivery manager can consume the retained source patch, bundle,
manifest, and `COMMAND`.
