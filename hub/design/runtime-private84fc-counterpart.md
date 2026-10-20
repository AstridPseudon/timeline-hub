# Runtime private84fc counterpart

Status: **APPROVED for reciprocal source/artifact review only.** This is one
unpublished PRIVATE generated counterpart; it is not a normal Agent pin,
integration adoption, release, App activation, rendering, or native outer
workflow result.

## Exact tuple and delivery

- Runtime producer commit: `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`
- Runtime producer tree: `f3ae49d38454ce73a9c91a954bb530b3ce51c122`
- Producer branch: `tl/rt-m2-private84fc-main-normal-artifacts`
- Producer parent / RT08 current-Main source port: commit
  `83a982eb1185477e50817e10b8c61212c43c8e03`, tree
  `becc776a4f0c88ae2f4c8ba9350116a040d223c7`, branch
  `tl/rt-m2-rt08-current-main-internal-source-port`
- Immutable producer checkout for Agent tooling: `/home/user/work/wt/rt-pin-c3d26567`
  (detached at the exact producer commit, retained by `bin/request-checkout`;
  no archive or moving worktree bypass).
- Runtime identity/protocol: `astrid-runtime` / `workspace.v1`
- Private package version: `0.2.15`; ordinary parent floor remains `0.2.14`
  with schema floor `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Agent source and schema

- Agent source commit/tree: `4d4535882f1e028805c3da178bf9a7fa53696da8` /
  `f18245ced9c231ddf8f6f2ee64405a84d3517921`
- Source path: `astrid/core/timeline/schema/edit-command.schema.json`
- Raw schema SHA-256:
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
- Inventory: 59 definitions, 33 operation clauses, 12 explicit v2 clauses.
- Exact authorized floor reconstructions:
  - voiceover: `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`
  - groups: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`
  - project-data: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
  - carrier: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
  - ordinary: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

## Generated artifacts

- Health/schema digest: `sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680`
- Raw Runtime bundle (`runtime_protocol/schemas/timeline-commit-bundle.json`):
  `sha256:bbbae375837456b267d9f0c7de89b962966da79a24abe7c4720301423b333bcb`
- Artifact manifest: 76 artifacts; `contract/artifacts.json` version digest
  `sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb`
- Generated Python and TypeScript roots include all 31 schema `*Args` types,
  including `ProjectDataWriteArgs`, `MigrateGroupsArgs`, `OccurrenceMoveArgs`,
  and `OccurrenceResizeArgs`.
- `occurrence.move` supports either exact integer `start_ms` or the existing
  frame-quantized `on`/`track`/`child_track` form and rejects mixed forms;
  `occurrence.resize` requires positive integer `duration_ms`.
- The current Main/RT08 reviewed materialization helper, commit port, store,
  and Main/catalog/source guards are retained; the generation commit changes
  generated contract/client resources and their generator inputs only.
- No private392, ordinary014, public013, parent-afterClip, or other sibling
  artifacts are mixed into this tuple.

## Review evidence and limits

The independent Runtime review is **APPROVE** in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-review-private84fc-main-candidate/report.md` and verified
the exact source/floors, current Main/RT08 safeguards, manifest, roots,
move/resize semantics, and normal generation. Evidence on the exact detached
checkout: generator `--check`, artifact manifest `--check`, TypeScript
conformance generator `--check`, `git diff --check`, bounded contract/generator
client cohort `111 passed`, and producer central targeted service/client cohort
`1,492 passed, 1 xfailed` (pre-existing). No full suite, old44 replay, native
outer workflow, pin, adoption, release, activation, rendering, or retirement
was run or claimed.

Next gate: Agent performs the reciprocal source/artifact review using the exact
producer checkout above. After both owners approve, the manager may coordinate
one normal private pin and one bounded native outer-workflow proof. Original
speech/outer authoring gaps remain OPEN.
