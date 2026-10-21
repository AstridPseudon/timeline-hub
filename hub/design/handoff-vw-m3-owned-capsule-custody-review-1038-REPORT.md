# REQUEST CHANGES — owned SceneSurface source carrier 1028

## Disposition

**REQUEST CHANGES. Do not authorize another physical run from this packet.**

The owned capsule is a valid source-only closure witness, but it is not itself
an admissible `ASTRID_REMOTION_PROJECT_DIR`. No accepted attachment exists in
the reviewed state without either a complete project with a real in-project
dependency graph/CLI already present, or a dependency copy that this task
forbids. A symlinked graph/CLI and a foreign validation artifact are rejected
by the real guards.

This was an independent review of 1028's packet and validator. No product,
Runtime, App, Composition, frozen ref, shared dependency, or shared runtime
file was modified.

## Reviewed identities and exact packet hashes

- Frozen Agent authority: commit `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`;
  tree `6adb4a1190dfb2874e101565f37eccd392b1ae2f`.
- Positive packet:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scenesurface-owned-source-carrier-1028/packet.pnylvl/positive`
- Positive packet census: 26 regular files, 176,719 bytes; zero symlinks;
  every regular file has `st_nlink=1`; real parents and realpath containment
  pass. The negative tree intentionally omits the three direct SceneSurface
  closure files.
- Immutable read-only graph reference: SHA-256
  `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`,
  21,455 entries. It was not copied or changed.

Packet file SHA-256 values reviewed independently:

```text
astrid/packs/rendering/editor/live-scenes/SceneSurface.tsx 830b7966ed736431ef688242c0917273d563e9716f3f58a633b5402879e7c2f9
astrid/packs/rendering/editor/live-scenes/authoring.ts 0a555b38ad93727e87f0dc08ed958a90412511be94a8bb632830c234f233d276
astrid/packs/rendering/editor/live-scenes/diagnostics.ts 012c8d739dfddf33742e0479a19a59d0a1f1b7e618e1e3948a049b962080a022
astrid/packs/rendering/editor/live-scenes/extension.tsx 4a77f276c6f1ac2725441bb93ade19bf51032c38cc8f95a76642eeeacb7c9f83
astrid/packs/rendering/editor/live-scenes/identity.ts ab1fa9c6972518d85dd39f5f1fdeee983a2754b6ad04a738d3e4dff13ed2b3b9
astrid/packs/rendering/editor/live-scenes/runtime.ts 3bdfa73290d935699d3937798df950376cfd25209a442fc9b294fc12c98a14f2
remotion/src/BoundsProbe.tsx 63eb3e93e22cb3333d8126b5c0761aca3e7670c208883a8391cb77e059fa45f3
remotion/src/FrameDiagnostics.tsx 7e15b692174a8a76c7c56ccc242e719669894852f70e6ae61669eba20b9a9368
remotion/src/LiveSceneClip.tsx 9e09d14557b5715b33bc9ae3e301d0e47066900eaa1085e582b45029d16d9d72
remotion/src/ReviewOverlay.tsx fdd57c56c937961b5f6964f570c2574945c63608936796ba08e624d7cac20cac
remotion/src/Root.tsx afde359fcf7324f0885543e3f3292372bd1b94bb3f219477bd15a2a4ee704f90
remotion/src/ThreeTimelineComposition.tsx 67e3edfb944970460d455fb41bbb1e25ba43b5baed78fd5646880462f8fc1609
remotion/src/animations.generated.ts b78ce0baa5a25bed3db9de377820b37f822b1651b53bfb0a9d52e19793ce8fea
remotion/src/asset-source.ts 9e98beae0405538b5d23778c46561240d4f95a6b313afeb4ef081bd4ff1c0b96
remotion/src/astrid-frame-worker.mjs 3b31d86c630c9f765f48d1c7c4f7880ea9caf2e1567ea3ac81c00d2c53124b85
remotion/src/astrid-frame-worker.test.mjs b06b47ac59913e44d085fda06083fe68fee95802bfebaac4084a1137eb461522
remotion/src/astrid-hashed-imports.d.ts be30280b9b7e453cf4307417827046d43457dcb20a623f120476438c6d38eadb
remotion/src/bounds.ts e8f668d3522616551e9acacae898bb48e2c70b0c8b6aca336a3ac40e98ad8609
remotion/src/effects.generated.ts bf6af4fbe7e5eeef9dcc267c21728b3253544f94170871310a45661729184b88
remotion/src/fonts.ts 5292071414d67cfaeee2eb7c04724d030809f5ef0ed6a3fbaaff58cde98d9bdb
remotion/src/host-registries.ts 16cb1c2068e6643edca57e89dc155f757418676adab6658192539ed7036b83df
remotion/src/host-scene.ts d4ed31477f3775018c96d4416f6652b8d1310476ce16f960c0cfd57218b17f98
remotion/src/index.ts a58f804bf74bab68b4549aa5c715eb4a89ec5835206d198fc79b462b4fc71ef9
remotion/src/transitions.generated.ts 2a2fd68e81ab0875803321051608a23493b812182a02d8674522cd25b25450a0
remotion/src/types.augmentations.d.ts 17933380b9ef3deb05c790ceef3a0df6aa52b4fa8b72f95cd29d6807d6b1f258
remotion/src/types.generated.ts 7214cb999cb5a59eba4b085faf6f136a686b2fc28c98e96eb0a89035a1d296aa
```

The 23 non-generated packet files matched `git show d0a:...` byte-for-byte.
The three generated registry files are ignored by d0a's `.gitignore`, so they
have no commit blob to compare; their packet hashes match the supplied d0a
generated-input authorities. This provenance must remain explicit in the next
run record; it is not silently treated as a commit hash.

## What passed

Exact commands, run independently:

```sh
BASE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scenesurface-owned-source-carrier-1028
PACKET="$BASE/packet.pnylvl"
node "$BASE/validate-source-closure.mjs" "$PACKET/negative" negative
node "$BASE/validate-source-closure.mjs" "$PACKET/positive" positive
node --check "$BASE/validate-source-closure.mjs"
```

Results:

- Negative **PASS**: four expected unresolved edges (the two
  `LiveSceneClip` -> SceneSurface/runtime edges and SceneSurface's two omitted
  sibling edges), with bundling not attempted.
- Positive **PASS**: all enumerated local edges resolve, exact direct closure
  hashes match, and esbuild emits a 75,274-byte bundle.
- Validator syntax **PASS**.
- Worktree `git status --short --branch` remained clean and `git diff --check`
  passed. The owned `tmpdir` is empty. The shared target
  `/home/user/work/runtimes/astrid` is absent/untouched.

## What the positive esbuild witness does not prove

The validator externalizes every bare package import with an esbuild plugin.
Therefore its non-empty bundle does **not** prove:

- any package was installed, resolved, or is the d0a/public13 version;
- `package.json`, `package-lock.json`, the Remotion CLI, frame worker,
  configured Node, schema, Composition package, or the 21,455-entry graph are
  present or owned by the selected project;
- dependency symlink/hardlink/containment or package file identity;
- the normal `prepare_remotion_validation` / `_validated_runtime` artifact,
  context, registry inputs, package roots, exact runtime-input digest, or
  completed original-probe custody;
- a browser, Remotion launch, frame, audio, render, or physical behavior.

It also checks a fixed list of local edges and direct closure hashes; it is not
the normal runtime source-validation/admission path.

## Exact admission failure and minimal conditional recipe

Setting `ASTRID_REMOTION_PROJECT_DIR` to
`<packet>/positive/remotion` currently fails the ordinary project contract:
that directory has source and `src/astrid-frame-worker.mjs`, but no
`package.json`, no `package-lock.json`, no `node_modules`, and no
`node_modules/@remotion/cli/remotion-cli.js`.

The existing read-only runtime
`/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b` has a real local
CLI and graph, but its d0a `src/LiveSceneClip.tsx` import resolves
`../../astrid/...` to `/home/user/work/runtimes/astrid/...`, which is absent.
Modifying that shared runtime to add the sibling source is outside scope.
Making `<packet>/positive/remotion/node_modules` or its CLI a symlink to the
existing graph would resolve the CLI outside the selected project and is
rejected by both `resolve_remotion_runtime_tools` and
`HostRemotionSession.lease` (`cli_resolved.relative_to(project)`). Hardlinks
and dependency copies are also disallowed here. The available validation
artifact is bound to another project (`/tmp/theme-readiness-final-3e1rq0sn/...`);
`_validated_runtime` compares its context and all measured project/CLI/lock/
source/package inputs and rejects foreign validation.

The smallest layout that would be accepted is therefore conditional on an
already-complete, owned project at this exact shape:

```text
<run-root>/
  remotion/                         # ASTRID_REMOTION_PROJECT_DIR
    package.json                    # complete d0a/public13 project
    package-lock.json
    node_modules/                   # already-present owned graph; no escaping links
      @remotion/cli/remotion-cli.js # real regular file inside this project
      ...
    src/                            # d0a source, including frame worker
  astrid/packs/rendering/editor/live-scenes/
    SceneSurface.tsx
    runtime.ts
    diagnostics.ts
    authoring.ts
    extension.tsx
    identity.ts
```

The source carrier must be attached as regular files, preserving that sibling
relationship and the exact d0a import path. Then, and only then, the runner
must run normal owned validation against that final root, publish a fresh
owner/mode-0600 validation artifact and its four environment bindings, and
re-run source/dependency containment and graph checks before any physical
request. If the only available dependency graph is the shared runtime above,
this recipe cannot be instantiated without a prohibited graph copy; hold.

## Remaining prerequisites

1. Supply or provision an already-complete compatible project with a real
   in-project CLI and dependency graph at the layout above, without symlinking
   the CLI or importing a foreign validation artifact.
2. Rebind and publish fresh normal runtime validation after the source
   attachment; retain its exact project, CLI, lock, package, registry, schema,
   and custody identities.
3. Re-run the source witness from the final attached root, then perform the
   separately authorized physical Gate 6 run. No browser, helper, Runtime,
   server, render, install, copy, marker, token, or full suite was run here.
