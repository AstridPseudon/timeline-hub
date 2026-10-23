# farm-zip-dry: composition (tf-zip-composition)

Rehearsal only. Nothing pushed, nothing committed in the product repo, no edits to the repo, tests, pins or locks.

**Overall: PARTIAL.** Steps 1–4 PASS. Step 5 (fast checks) is BLOCKED: the sandbox refused `npm ci` in the fresh tree, so TypeScript, the registry check and the smoke subset did not run.

## Inputs

| Item | Value |
|---|---|
| Integration branch | `tl/integration` in `/home/user/work/composition` |
| Integration commit | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` |
| Integration tree | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |
| Hub ref `hub/timeline/composition/tl/integration` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` (same as integration) |
| Base (requested) | `67b8aa3d0d6831d3e3504a340ff583c3da253707` |
| Base is ancestor of integration | yes (`git merge-base --is-ancestor` exit 0) |
| Live upstream main (`git ls-remote https://github.com/peteromallet/timeline-composition refs/heads/main`) | `67b8aa3d0d6831d3e3504a340ff583c3da253707` |
| Local `origin/main` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` (equal to live tip) |

Note: the worktree at `/home/user/work/wt/tf-zip-composition` is already at `635f4de06`, with clean status.

## Step 1 — record integration, base, ancestry: PASS

Integration commit, tree and ancestry are as in the table above.

## Step 2 — squashed patch base..integration: PASS

Command: `git -C /home/user/work/composition diff --binary 67b8aa3d0d6831d3e3504a340ff583c3da253707 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 > <worker>/zipdry/zip.patch`

- Patch size: **493,374 bytes**
- Changed paths (`--name-status`): **118** (`A` and `M`, plus 2 `D`: `typescript/tests/scaffold.test.ts`, `typescript/tests/theme-api-smoke.ts`)
- Test-path changes (`tests/` or `.test.`, from numstat grep): **20**; product and build/package paths: **98**

The brief's earlier archive figures (80 members, 73,451 B, SHA-256 `819acf6b…`) belong to a different artifact. I did not build an archive, so they are not compared here.

## Step 3 — fresh clone at base, apply: PASS

- Fresh clone: `git clone -q https://github.com/peteromallet/timeline-composition <worker>/zipdry/fresh`. Its HEAD was already `67b8aa3d0`, which is main at base, so the detached checkout was not needed. My `git checkout --detach` call was denied by the sandbox. It was not required, because HEAD already matched.
- `git -C <fresh> apply --check --binary zip.patch`: exit 0
- `git -C <fresh> apply --binary zip.patch`: exit 0
- `git add -A` then `git write-tree` in the fresh clone: **`5ab5191a296980a0a6bcd1178ab6902d6478a148`**, which **equals the integration tree**.

## Step 4 — apply to live upstream tip: PASS (no drift)

- Live tip (ls-remote, re-checked at run time) = `67b8aa3d0`, which equals the base. The live tip therefore has no drift, and the step 3 result applies unchanged: no conflicts.
- Deferred per upstream rule: none listed for Composition. The deferred items are App `6e3445ee9` and Runtime `6162e0e33`, which do not apply to this repo.

## Step 5 — fast checks on the applied fresh tree: BLOCKED

- Composition has no `lint` script, and no lint config in `package.json`. The canonical checks (README "Build, package and verify") are `make build` (gen-registry:check + strict `tsc` + ESM build), `make test` and `npm run test:package -- <tgz>`.
- Dependencies are not installed anywhere for Composition. There is no `node_modules`, and no shared `venv` exists for this repo. `devDependencies` include `typescript 5.9.3`, `tsx`, `remotion 4.0.509`, `react 18.3.1` and `esbuild`.
- Command tried: `npm ci --prefix <worker>/zipdry/fresh --no-audit --no-fund`
  - **Refusal (verbatim):** `This command requires approval`. This was the sandbox's approval gate, with no approval given.
  - An earlier attempt with the install chained to other commands was also gated ("requires approval").
- I stopped here, per the brief ("if a step is refused (install), STOP and report the exact refusal. Do not route around it"). I did not borrow a `typescript` or `tsx` from another repo's `node_modules`.
- **Not run, so unverified:** `make build` / `gen-registry:check` (drift), `tsc` strict check, the focused smoke subset from the README (`npm run build:test` plus `registries`, `animations` and `scene-evaluation` tests and `gen-registry.test.mjs`), `npm run test:package`.
- Only check that ran (no install needed): `node --check` on `scripts/build.mjs`, `scripts/smoke-package.mjs` and `scripts/build-typescript.mjs` in the fresh tree, each exit 0. This is a syntax check only and proves nothing about TypeScript or behaviour.

## Smallest cause of the failure

Installing Composition's devDependencies in a private worker clone is not permitted by the sandbox approval gate. Step 5 cannot run until one of these happens:
1. the orchestrator approves `npm ci` in `<worker>/zipdry/fresh`, or
2. a shared Composition install is created once by the orchestrator, read-only to workers (the same pattern as App's `node_modules`).

Once deps exist, the commands are:
```
npm run gen-registry:check        # or: make build
npx tsc -p typescript/tsconfig.json --noEmit   # strict; build:ts emits declarations
npm run build:test && node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/registries.test.js typescript/test-dist/tests/animations.test.js typescript/test-dist/tests/scene-evaluation.test.js scripts/gen-registry.test.mjs
```
The README's canonical form is `make build`, and the full `make test` is for the central test service only.

## Recommended next steps

1. Orchestrator decides on the install (see above), then re-run step 5 in the fresh clone (it does not need a new worker).
2. Lint is not defined for Composition. Either skip it in the gate or add a repo-owned check. Not a worker decision.
3. The worktree `/home/user/work/wt/tf-zip-composition` is unchanged, so no commit is needed. The commit-msg file was not written, because this rehearsal produces no repo change.

## Workspace notes

- The brief named `$ORCH/workers/tf-zip-composition/tmpdir` as the scratch directory. That path is a **file** (it contains `/tmp/w-e87e741327`), so I used `$ORCH/workers/tf-zip-composition/zipdry/` for scratch instead.
- Patch: `<orch>/workers/tf-zip-composition/zipdry/zip.patch`
- Fresh clone: `<orch>/workers/tf-zip-composition/zipdry/fresh`
- Install attempt log: none, because the install was refused before it started.
