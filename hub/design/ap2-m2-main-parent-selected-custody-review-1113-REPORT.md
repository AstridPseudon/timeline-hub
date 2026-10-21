# App2 M2 parent/selected main custody review

## Verdict

**HOLD.** No browser, build, service, socket, actual, install, or full-suite
run was performed. The parent packet has one precise handoff blocker; the
selected packet has one separate exact-keeper blocker. Neither packet is an
executable exact packet yet.

## Parent packet

The committed candidate source is recoverable as:

```text
commit 6707a30f14bf3a5ee19cb9e481b7dbd95b77522a
tree   6ff32d797f0e774b8574274a3494ce8755fa160c
spec   tests/e2e/local/three-products.spec.ts
spec sha256 40f35d7d09471b8a255724b4330e61128c9fd4f94733ce55dc30b0d9fafb837d
```

Static review of that commit passed for the real UI `Zoom out timeline` setup,
unchanged pointer `22.5`, centered five-second left edge `20`, V1 placement,
strict 404 body, native `clip.add-media`, and the existing File/DataTransfer,
raw/opaque/order/source/epoch/ACK/retry/restart/undo/zero-legacy assertions.
The frozen original parent source remains `8eb4d08e60f434b938ea885c8cadca4bd87151b3`
(tree `ea317333400d1a342f2520556eef8ce9399666c1`, spec SHA-256
`5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603`).

The required `design/run-on-main-app2-parent-viewport.md` is not present in
the available worker worktree or shared design area. The worker log records
the handoff as `parent_role_sha=PENDING_HARNESS_FINAL_COMMIT` and
`parent_role_tree=PENDING_HARNESS_FINAL_TREE`; it also records the claimed
handoff as `NOT READY`. I did not reconstruct or silently bind those fields.
This is the required single parent HOLD. Minimal correction: restore the
complete run-on-main handoff as an available artifact, then bind the existing
guarded parent gate/driver data-only to the exact committed SHA/tree and clean
keeper, retaining its helper/driver reverse-binding, list-1, zero-test, child
RC, short-root, Remotion-off, credential, and retention guards.

Frozen R4 refs were read without checkout and resolved as:

```text
candidate-sdk          11caf1d9de291d76f491cf69f7942606b7471d7a tree f6f4fad77ded050b1e9c2d802cc3da35b459e610
candidate-runtime      31c7ac3a00f7a205f507bf5bd4d4625628d429bd tree 73e676f420ba0545b6eebe45870d532344a9e69b
candidate-app-qualified 8f0c2484463e9b666d184a744d52e252984e551a tree 26ad064632fac9ff123670aa7d6ed0e3d8f89178
candidate-composition   c82eb7c459d0a41263954bf007071a6a0e8e0a6a tree 49975e7a54fd594e1b7fc807681fe28611d57864
```

## Selected packet

The committed current source and original source identities are consistent:

```text
current App       0cc2583aaf07e89190b9344b5ac82849d6279586
current tree      320e74a93676c781e83885b86ec237b4a1465d80
selected spec     2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
original App      a50ca4a0172cce9c73ce3c040290bf9479098b0f
original tree     92391f9a57dd38ce327b0a63990725053ea34601
original spec     10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1
e5af order fix    e5afdaed02a7bf57fdd3768bb6cbe356e9c776f7
runner sha256     dcd4bf11e178cabd63a0a450e206b7450abb098a27110a2eca6ecd085794cefc
```

The selected source retains original P1/P2 admission, `draft-1` seed,
source removal, retained-P1 refusal and dirty draft, lost ACK, restart/reload,
exact body and idempotency key retry, inverse/undo, and zero legacy traffic.
The e5af source check confirms publication before authoring enablement and
credential provisioning after Runtime restart; the returned `new_head` is
passed to P1.

The owned runner’s exact offline guarded preflight passed, including shell/JS
syntax, source and ancestry, Agent/Runtime bindings, 76 Runtime artifacts,
schema/wire hashes, Composition 0.0.13 archive with 77 members, Node
22.22.0, Vite 5.4.21, Playwright 1.60.0, helper/driver hashes, private graph,
wrong-role/tree/argv/zero-test refusals, and exactly one collected test in one
file. The unchanged approved retention review was reused: explicit returns
guard each copy/identity/manifest operation, partial trace/context retention
does not require DOM, and child RC versus retention failure is preserved.
`env -i` is the only actual entrypoint; the runner adds only its per-process
private Node/Python/cache/TMP settings and no Remotion variables.

The selected actual remains held because its exact command requires
`APP_KEEPER_ROOT=/home/user/work/app` at current source/tree and clean status.
That keeper is currently:

```text
HEAD  92c30b570cf8105dc021a64874c258e6c950b841
tree  c34d65b66481fd0015279451b175c53b7b5e8f4f
dirty ?? vendor/fake-indexeddb/fake-indexeddb
      ?? vendor/timeline-ops/timeline-ops
      ?? vendor/timeline-schema/timeline-schema
```

The runner’s actual-path `verify_protected_keeper` rejects both the identity
mismatch and non-clean status. Minimal correction: provide a separately
protected clean keeper at the packet’s exact current commit/tree, or update
the packet’s data-only source/keeper binding after an orchestrator-approved
identity change. I did not remove or alter the untracked paths.

## Commands and results

Passed:

```text
sh -n <selected current runner>; node --check scripts/runtime-discovery-proxy.mjs
selected runner env -i ... SELECTED_FINAL95_MODE=preflight ...
  PASS: all 11 offline guards and exact list-1
parent static assertion/hash/provenance checks
git diff --check (worker source remained clean)
```

The current worker worktree and shared dependency symlink were unchanged.
No source, pin, helper, driver, graph, or shared worktree mutation was made.
