# AM-footage current Root typing proof

## Result

**Blocked at the existing generated Root type boundary; AM-footage source
evidence is green.** No product files were changed. The current normal
generator still emits one `text-card` type error, so this worker does not claim
Root qualification or approved public-host readiness.

## Private candidate and custody

- Current worker HEAD: `5c5173dcb57669a9d43e5add2674543333f1c6d2`.
- Approved AM-footage donor overlaid privately: `2e9fb6e260778e0ae6dc4a39a498d0f36a837ef6`.
- The private candidate was current HEAD plus the donor's complete
  `am-footage` directory and its `pack.yaml` resource declaration. This
  preserved the donor's corrected `component.tsx`, `helper.ts`, `scene.ts`,
  and `scene.test.mjs` without changing the worker checkout.
- Node: `v20.19.4`; npm: `10.8.2`; Node SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Runtime lock SHA-256:
  `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311`.
- Immutable node graph: `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`,
  21,455 files.
- Public Composition 0.0.13 artifact SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Source manifest: [source-manifest.git-ls-tree.txt](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-am-footage-current-root-typing-proof/source-manifest.git-ls-tree.txt>)
  (1,426 current-tree entries); staged source hashes:
  [stage-source-manifest.sha256](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-am-footage-current-root-typing-proof/stage-source-manifest.sha256>)
  (1,432 files).

Private staging used real scope directories and leaf-only links through the
existing guarded helper. Shared dependencies/runtimes were read-only; no
install, extraction, or cache write targeted a shared path.

## Evidence

- Normal generation: **PASS**

  `ASTRID_REMOTION_PROJECT_DIR="$STAGE/project/remotion" ASTRID_NODE_EXECUTABLE="$NODE" PYTHONPATH="$STAGE/project/astrid" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B "$STAGE/project/scripts/gen_remotion_types.py" "$STAGE/project/remotion/src/types.generated.ts" --include-element-registries`

  The generated registry contains the normal `am-footage` import and
  registration; no generated file was patched.

- Root typecheck: **FAIL, one existing out-of-scope error**

  `cd "$STAGE/project/remotion" && ... /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm run typecheck`

  Exact error:

  `src/effects.generated.ts(97,47): error TS2345: Argument of type 'EffectComponent<never> & SceneCapableComponent' is not assignable to parameter of type 'EffectComponent'. Types of parameters 'props' and 'props' are incompatible. Type 'EffectProps<unknown>' is not assignable to type 'EffectProps<never>'. Type 'unknown' is not assignable to type 'never'.`

- AM-footage scene direct neighbor: **PASS, 5/5 cases** with pinned Node.
- AM-footage volume direct neighbor: **PASS, 5/5 assertions** (the Node test
  runner reports one file-level subtest containing five tests).

## Concrete boundary and owner handoff

The installed public13 declaration at `dist/registries.d.ts:15` exposes
`effects` as `Readonly<Record<string, EffectComponent<never> &
SceneCapableComponent>>`. Current `scripts/gen_effect_registry.py` emits
`selectOwnedEffect(..., winner: EffectComponent, owners:
Record<string, EffectComponent>)`, where the default is `EffectComponent<unknown>`.
The generated line 97 passes `PUBLIC_EFFECT_REGISTRY['text-card']` directly as
both winner and owner, causing the invariant function-parameter mismatch.

[PATCH](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-am-footage-current-root-typing-proof/PATCH>) contains the
minimal **unapplied** Agent-owner correction: cast the public-registry values
to the host `EffectComponent` type at generator emission (including the
`include_local=false` public symbol). This worker did not edit the generator,
Root, public types, generated output, schemas, DTOs, pins, or AM-footage
product paths.

There was no missing-resource block: the donor resource declaration was
present in the private stage and normal generation consumed it.

## Not run / next step

No browser, render, bundle, localhost/socket, full suite, physical proof,
install, network, activation, archive, adoption, or public-host qualification
was run. The Agent owner should review/apply the unapplied generator boundary
correction, regenerate normally, and rerun the Root typecheck before claiming
approved source-host readiness. The private generated stage was removed after
the manifests and logs were recorded.
