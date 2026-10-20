# RT07 current Runtime compatibility qualification

2026-10-20. This is a bounded private qualification only; it does not activate
the native cohort, restore render, or change Runtime/Agent source.

## Exact sources

- Requester parent: Agent commit `32d6de6a8a50f05032a9b1f110ff1ac5a8975f4f`,
  tree `4c000d64c9048910889266f00fd4036a47ffebd3`.
- Durable successor: Agent commit
  `ed39c027f9f21b824c763610f18343b2bf0d682e`, tree
  `a0650c21b268f879969a9420bdb2921e4008289b`.
- Current Runtime tested: commit
  `7f6dd8920e1ceec41b137358df5e7fecc304888d`, tree
  `4cccb2d643194df7df95d624e89a6cd9f6f268fc`.
- Central snapshot tree (includes only the temporary Runtime-lane adapter):
  `07c7491c92e767d8d8a71b8ae52aba24570db97c`.
- Private generated pair: full 53-definition S2-superset schema SHA256
  `fafb1985a326e6121aa8c9fb34bbda196edc3dfaf462352070372e631bea1f52`,
  contract version `0.2.14`, normally generated artifact manifest
  `sha256:48c7b6533e2774a70e36517948a18fd5cee07f4d30e8f339776be9b3ec74ed4e`.
  Generation/checking reported all 75 artifact hashes valid. No public schema,
  lock, DTO, endpoint, or Runtime source was changed.
- Product source hashes in the archived durable successor:
  `astrid/sdk/timeline/assembly.py`
  `e5faf15b139c4da8463da3b01dedd6c746f9d8ef41ba8927eddec30cef7ef346`;
  `astrid/sdk/timeline/sync.py`
  `6c82655db96e8ff6d15fb08eacb2263683af2f55664acef79992db3f79e79781`.

The source archive and private locator adaptation are retained only under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-registered-current-runtime-pair/source-agent`.
The adaptation changes no product or assertion bytes; it makes the existing
pair helper archive the committed Agent parent and this current Runtime
worktree instead of the historical `2c4ac180...` Runtime.

## Central result

Request:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$($ORCH/bin/request-test rt-m2-registered-current-runtime-pair targeted \
  --files tests/test_registered_native_pair_private.py)
$ORCH/bin/wait-test rt-m2-registered-current-runtime-pair-targeted-1020140436-1676
```

The temporary adapter invoked the existing `test_registered_native_pair` body
and its unchanged four inner test files. Final central result:

- Inner raw count: **17 total = 15 passed, 2 failed** in 122.86s.
- Outer adapter: **1 failed** in 129.73s.
- The 15 intended native requester/admission positives passed against current
  Runtime, including normal generation, real action, normal upload/settlement,
  proposal handoff, exact-attempt fencing, admission ACK-loss/restart replay,
  duplicate/distinct CAS, scope/actor refusal, and pending-suffix preservation.
- The two failures are the unchanged legacy completion cases
  `test_registered_assembler_settles_on_normally_created_timeline[False|True]`.
  They reach the current Runtime publication guard and receive
  `ApiError('conflict: tracked timeline publication requires a timeline command')`.
  Their retained strict xfail recognizes only `UnsettledRegisteredAssembly`,
  so the xfail itself is an unexpected failure under this current server.

The current Runtime guard is intentional and remains intact:

- `runtime_protocol/service.py:6736-6737` refuses tracked legacy publication
  with details reason `timeline_commit_required`.
- The analogous parent-composition guard is at `service.py:2766-2767`.

This is not evidence to weaken old-endpoint denial. It is a compatibility seam
for the Agent owner of the retained legacy test: after review, the strict xfail
can recognize the current structured Runtime refusal while preserving its
assertion body. No Runtime compatibility fix was authorized or made.

Two setup attempts are not qualification evidence: an absolute `--files` path
was rejected by the central service, and a repository-relative run with the
Runtime venv stopped at inner collection because that venv lacks Pillow. The
final run used the installed Agent venv only for the existing Agent inner tests;
the Runtime source under test remained the current commit above.

## Limits and disposition

- This proves accepted file/proposal and admission/retry behavior only. It does
  not prove decoded render output, render execution, pixel/audio parity,
  historical render, macOS, or legacy completion publication.
- `rendering.assemble_timeline` remains distinct from `rendering.render` and
  STITCH aliases remain on `rendering.render`.
- No nearest-current-9 commit run was needed: all 15 intended current native
  positives passed, and the only failures were isolated to the two retained
  legacy completion xfails.
- No full, broad, matrix, release, pin, merge, shared-dependency write, public
  activation, or test assertion change was performed.

Recommended next step: Agent owner review of the strict-xfail exception seam;
keep the Runtime denial and qualify render decode/admission separately before
making any RT07 replacement or D13 claim.
