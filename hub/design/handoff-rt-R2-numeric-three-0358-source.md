# F-R2 numeric-three source handback

Read-only source assessment; no product, test, store, schema, generated, pin,
dependency, or shared-ledger files changed.

## Exact scope

The authenticated packet is `handoff-rt-D86-9211-outcomes-0303` for request
`agent-fd86-successor161-1025025816-9211`. It selected 161 IDs and reported
6 PASS, 43 FAIL, and 112 ERROR under the original 45-second timeout. Its
`numeric9` family is 9 FAIL / 0 PASS / 0 ERROR. The six numeric-move IDs are
rows 87--92 and are excluded from this handback. The exact three are rows
93--95:

| packet row | canonical ID | input pair | status / first exception |
|---:|---|---|---|
| 93 | `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[2-2.0-occurrence:occurrence-1/clip:clip-1]` | `before=2`, `after=2.0` | FAIL / `RuntimeErrorBase`, `inverse stage native writes do not cover its authenticated effect image` |
| 94 | `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[1-True-occurrence:occurrence-1/clip:clip-1]` | `before=1`, `after=True` | FAIL / same |
| 95 | `tests/editing_conformance/test_commit_runtime_numeric_params.py::test_native_film_param_edit_preserves_exact_image_and_inverse[True-1-occurrence:occurrence-1/clip:clip-1]` | `before=True`, `after=1` | FAIL / same |

Each case sets `params.x` on the occurrence-scoped clip through
`capture_clip_set_params`, accepts the change, then submits `timeline.inverse`
and redo. The purpose is exact JSON type preservation across a native
film-parameter edit and guarded inverse/redo, not a move or fixture migration.
The packet records `runtime_protocol/service.py:2518` as the first exception
location; the underlying verifier message is emitted by
`runtime_protocol/timeline_commit_auth.py:1737-1739`.

## Producer / verifier comparison

The Agent producer at current normal source `562ee30b6ed567a90a114f5029a96da2ece9789e`
is unchanged from the numeric packet for `_scalar_commands.py`,
`_commit_patch.py`, and `_step_undo.py`; `inverse.py` has only the later D90
materialization-presence check relative to the numeric source.

- Agent `_scalar_commands.py:68-95` resolves the occurrence/shot identity,
  records scalar dependencies and a target binding, validates only changed
  parameter values without coercion, and records the `params.x` write.
- Agent `inverse.py:1032-1104` applies authenticated inverse guards and
  restores physical writes; `:1127-1181` records inverse stages and native
  ranges. Agent `_commit_patch.py:494-561` derives stage effect diffs and
  effect ranges, then `:595-611` binds `commit.effect` records.
- Runtime `timeline_commit_auth.py:1230-1394` authenticates source stages,
  native membership, and contiguous ranges. Its
  `_inverse_stage_boundaries` at `:1397-1770` reconstructs each stage and
  requires the native image to equal the authenticated stage image at
  `:1737-1739`; `service.py:2517-2518` exposes the rejection.

This source comparison demonstrates the reporting seam and a conditional
Agent candidate seam, but not which side produced the mismatch. The Runtime
store is not implicated by source evidence and remains D94-owned.

## Ownership and missing record

Smallest demonstrated seam: Runtime verifier
`timeline_commit_auth._inverse_stage_boundaries` (`:1737-1739`) is the exact
guard that reports these three rows. It is not evidence that the guard is
wrong. Conditional Agent follow-up remains `_commit_patch.finish` / inverse
stage effect construction only if a complete record proves that the producer
omitted or misprojected the effect image. No Runtime verifier broadening or
Agent fix is authorized by this handback.

The authenticated packet intentionally exports only safe per-ID outcomes and
hashes. Source cannot prove the fault without, for each changed-x publication
and its inverse, the accepted source history record (ordered commands, steps,
writes, derived writes, dependencies, bindings, and ordered step patch), the
rejected PreparedCommit/records (canonical document, inverse-stage native and
effect ranges, and commit.effect bindings), the sequential input/output
boundaries, and the complete before/after closure images including logical
occurrence-to-physical shot/internal-revision mapping. A submitted-versus-
produced command pair is also absent. Do not infer a source fix from the
guard location alone.

The four inverse scenarios from `rt-R2-inverse-auth-sol-0333` remain separate:
they concern word-binding restore order, leaf timing/native-range membership,
and clip-delete root/order projection. These three concern an
occurrence-scoped `params.x` edit and authenticated effect-image coverage;
there is no selector or source-boundary deduplication.

## Tuple and hashes

- Packet source Agent: `cef8a5be53f68a7cd3b5403c362171c5633a5ae9`, tree
  `b0c7de33744c89afa5f34394f92debb6498a1c9f`.
- Packet source Runtime: `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, tree
  `47b376717ce7a919a697c62133de3e74dc9f6d3a`.
- Numeric test source commit: `ec76fa69e6cc8af424ec397512b9422968b7eaf5`.
- Numeric params source SHA-256:
  `8f1020a2ce363abbc11f7fc47b8287a48f963c7d4de3a88b5e5f86a757f6788c`.
- Agent current source SHA-256: `_scalar_commands.py`
  `6b5c1a0db9fcf78533f16ca14d9ab14d96ca31ce19875c062b0470954488b34c`,
  `_commit_patch.py`
  `05a1ebc6b251c75f4d5dc272598adc295ce5bf5a8c4596ad08497de6676264be`,
  `inverse.py`
  `06bd41f404a40c17a1ec06b49c8443e0e755f622134822ede55fb3ca79234cee`,
  `_step_undo.py`
  `a38bb078ecd2579399f131fa0a08a9bedd339226f92b9d8ac27de2b6d27827a6`.
- Runtime source SHA-256: `timeline_commit_auth.py`
  `4ac2b8792fe0389afb6eb710a348c35fa196131a13cab175bd3646f7d2cc0aeb`,
  `timeline_commit_store.py`
  `2a68990b180326585b7f0abaf1ee54c8ff9340e83663f17cd1efff1b2bd78a5c`,
  `service.py`
  `5e79c3b9ed3d2ba5efc129d1cc8d7a43075c4ebc9194026fdb641a8eeb7ff19a`,
  `contract/commit-v2.md`
  `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.
- Packet hashes: per-ID TSV
  `70f99290d1cc09fd4eb692497326181b235e5176497e6645c4d84901e9d7d421`,
  per-ID JSON
  `885e63ebf1d323e5da9e261d86ed706e40d94161adb6b9e2ad46cd4133e1a6f6`,
  run identity
  `e02f9449512ccc7434f53a8d0ba7f87ee94bf8085c07ac45a4b9fc7e1060c32e`.

Peer handbacks consumed: `peer-runtime-to-agent-orchestrator-20261025T0315Z-actual9211-source-owners.md`,
`peer-runtime-to-agent-orchestrator-20261025T0336Z-candidate-join-and-current-bodies.md`,
`peer-runtime-to-agent-orchestrator-20261025T0350Z-command-pair-missing-and-inverse-seam.md`,
and `rt-R2-inverse-auth-sol-0333-report.md` / its source-trace handback.

## Static evidence

- In-memory AST parse/compile: PASS for the selected Agent/Runtime files.
- Runtime `ruff check --no-cache runtime_protocol/timeline_commit_auth.py`: PASS.
- Runtime scoped mypy with private cache and skipped imports: PASS; only
  existing untyped-body notes.
- Agent source-only Ruff on the packet/current producer files was not a clean
  qualification: existing findings were reported in `_commit_patch.py`
  (B010/B023), `inverse.py` (SIM102), and the unchanged numeric params test
  (I001/PLC0414/RUF100). No fixes were applied.
- `git diff --check HEAD`: PASS; Runtime worktree remains clean.
- No pytest, collection, helper/fixture execution, service, browser, socket,
  build, or functional PASS was run or claimed.
