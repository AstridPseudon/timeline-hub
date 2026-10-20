# Runtime M4 current-main delivery preflight

Read-only snapshot, 2026-10-20 UTC. Sources were the four `tl/integration`
worktrees and their frozen-reference repositories; all four worktrees were
clean.

| Repo | `origin/main` (tree) | `tl/integration` (tree) | main ancestor? |
|---|---|---|---|
| Agent | `96b283d5d6fd8031538f881e486bb2ebf45dce75` (`1e31c58ff3aa35229ba07a8f6bb9c04dc31dd795`) | `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1` (`6de356067d251e644101da19272c5424fa4f3a68`) | No; `0/247`, no merge base |
| Runtime | `240d5bb202af709294551045554012f079fd06ca` (`2e77d0df220885e978c5fbdf5d6072292ac07284`) | `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd` (`94c5ffbc0b636e25475c0f351bfb384dd06ee8ab`) | No; `0/165`, no merge base |
| App | `86d7def4f7c2b8bc1ae1b50031bfea6750256517` (`1ac90a1e3ca57341537c6e76f2c463c715597b79`) | `22788084f9b9a69322fca1c6aff35d17c5c2c189` (`ecd3d0f250b8ca597a1627832c35003441a79186`) | Yes; `4/148` |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` (`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`) | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` (`13e375534fffd704305eced5686699d2c8c9c948`) | No; `0/40`, no merge base |

The frozen-reference repositories reported the same four SHA/tree pairs.

## Main drift affecting Timeline-owned paths

The three unrelated repositories cannot honestly be described as “main ahead”
by commit. Their tree-side differences are still delivery-relevant:

- Agent: 52 owned-path differences (32 deletions, 20 modifications), including
  `astrid/sdk/timeline*` and `astrid/packs/timeline`.
- Runtime: 207 differences (136 deletions, 71 modifications) across the
  contract, `runtime_protocol`, generated clients, and Timeline tests.
- Composition: 106 differences (2 additions, 85 deletions, 19 modifications)
  across the package/build and `typescript` evaluator sources.
- App: current main is four commits ahead (`c447c6f89`, `b7a1d3826`,
  `bedb6229b`, `86d7def4f`) and all four touch owned paths. The integration to
  main tree diff is 182 owned paths (7 additions, 77 deletions, 98
  modifications), including the known main drift in Timeline editor/runtime
  code.

## Delivery-build compatibility

`bin/delivery-build` is the approved `cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e`.
It is source-read-only: it pins base/tip SHAs, uses private verifier clones and
rechecks both source refs after each repo; it does not mutate source refs or
indexes. It creates a linearized synthetic patch from the integration tree,
applies it with `git am` to a fresh main clone, verifies the bundle, and compares
both resulting trees to the pinned integration tree. A failed verification
prevents ZIP creation.

The script does not enforce main ancestry. It truthfully records ranged versus
unrelated history and uses a full bundle for the three non-ancestor repos, but
that is a warning/exception rather than an M4 hold. Small follow-up: add an
explicit ancestry/preflight refusal or recorded exception, and carry a
whole-four-repo source-freeze manifest into the final M4 refresh. Do not request
that refresh before the M2/M3 gates; no ZIP or gate/film/macOS claim is made by
this preflight.

Evidence: read-only `git rev-parse`, `merge-base --is-ancestor`,
`rev-list --left-right --count`, `diff --name-status`, `status --short`, and
`sha256sum` checks; no full suite or delivery dry-run was run because neither
the source nor the approved script changed.
