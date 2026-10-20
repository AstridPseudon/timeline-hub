# Runtime private carrier with current catalog fence

Status: **private source candidate, final peer review required**. No public pin,
release, activation, merge, or comprehensive native-pair qualification.

## Exact sources and scope

- Current Runtime source image: `81f8c7e0b22c34804015c054762af3d737e4698a`
  (catalog restoration `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f` plus native
  historical retry `c45cbc6ba3772ac2cebb5a5c94f91be24231e2d5`).
- Reviewed private carrier: `83fe4a1cc8e79ba6db2f06271097a96ff2e7c59a`, tree
  `2d9d740ef22eea3b9ec4899bb8e400251bd6d444`.
- Candidate central snapshot tree: `d20b745c26a33c2ea4e20863f846335c8cf33e1e`.
  The assigned branch starts at 83fe; this is a file/tree composition with
  current 81f source, not a claim to have changed Git ancestry. The harness
  supplies the new commit after worker exit; no pre-commit SHA is invented.
- Exact Agent counterpart: `3730d0bd51686a1692450359482205df64dcc839`, tree
  `3892a10bcffa9bf520b4c79591637cf3259d6724`. It was extracted with `git archive`
  to this worker's private `agent-source` directory. All actual-provider checks
  below use that archive, not moving `/home/user/work/agent`.
- The command schema is byte-identical to that Agent source: SHA-256
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`,
  **48 definitions / 22 operation clauses / 13 source-bound v2 operations**
  (Agent's existing `SOURCE_BOUND_OPERATIONS`; `track.create` has an open schema
  version and is also registered at v2). No ordinary 55/29 source was imported.
- The packaged command resource equals that schema. Bundle SHA-256:
  `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`;
  manifest SHA-256:
  `9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62`.
- Public floor `tests/fixtures/published-command-schemas/agent-26ef2bbb.json`
  remains SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

The previous 17-path allowlist is retained (16 paths differ from 81f; the
allowlisted door-audit test is byte-identical). An independent read of every
81f tracked blob found **415 paths outside the allowlist, zero mismatches**.
The 125-line native historical test, Main promotion implementation and tests,
current door audit, empty/fresh/absent-head safety, connector code, all public
schema fixtures and all other current tests are retained. No outside path was
removed. Full scratch inventory: `workers/rt-m2-carrier-catalog-fence-compose/source-inventory.json`.

## Composition delta and authority

Only two carrier paths change relative to reviewed 83fe:

- `runtime_protocol/timeline_commit_store.py`: **+19/-5** lines. At all three
  existing ownership authorization sites (current film image, inverse source,
  accepted historical slot), the exact project-scoped `shot_revision_heads`
  revision must equal the authenticated accepted image before a new mutable
  projection is authorized. The current Main same-physical-owner historical
  proof is retained; it still needs the existing binding/read/active-owner
  checks, and carrier materializations additionally need the unchanged
  `_same_materialization_slot` provenance join.
- `tests/test_timeline_projection_ownership.py`: **+55** lines, one genuine
  frozen-Agent regression. It creates a v2 shared-source allocation whose
  physical slot differs from its source, promotes a catalog candidate in that
  slot, proves ledger-first exact retry bypasses the provider, refuses both
  current-slot and historical-slot new writes atomically, and proves C4 exact
  historical reuse retains the newer catalog head and immutable film closure.

Current 81f service/store and promotion/authority/native-historical tests are
restored byte-for-byte. Every other carrier path remains byte-identical to
83fe. The accepted-ledger-first order, source/owner/item joins, global raw-item
reservation, canonical `item_id` precedence over opaque `id`, and immutable
reuse short circuit are unchanged. No ancestry/read exemption was widened and
no blanket historical-reuse ban was added. No DTO, table, endpoint, release,
schema fixture, xfail, skip, or test expectation weakening was added.

## Exact inventory relative to current 81f

| Path | Candidate SHA-256 |
| --- | --- |
| `contract/artifacts.json` | `9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62` |
| `contract/schemas/edit-command.json` | `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` |
| `generators/command_schema_compatibility.py` | `57cfb2e5c8cf50be2d5c47ec815e7e0f5d1109dc41bfb405402889a4dd11b90b` |
| `packages/python/astrid_runtime_client/contract_metadata.py` | `71390595d10a33a11110274faa8286bf3888d8afcf6f010ada1ed77140cf686c` |
| `packages/python/astrid_runtime_client/generated.py` | `85ffacd3ae18bb666038dca041aa59b6f8e2774a12736542ae833136474c09be` |
| `packages/typescript/src/contract-metadata.ts` | `61a89340a2d116cec86e7b197222beb7328a7dcecf6aadcea4e79947cd5fd45f` |
| `runtime_protocol/contract_metadata.py` | `45e92b1efbbfe9c54c43f51696d4e029741cd73e31dd197cdb781a6fcbdff482` |
| `runtime_protocol/schemas/timeline-commit-bundle.json` | `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425` |
| `runtime_protocol/timeline_commit_port.py` | `28968f683c064af54da4b767618880781a6ec66e80586d462b8b7e2b1f96ee86` |
| `runtime_protocol/timeline_commit_store.py` | `503cf6a33f1817c4c69b1cbd99859c05ba8a33b8f41d4ac8e1107ea92b5c5203` |
| `runtime_protocol/timeline_materialization.py` | `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` |
| `tests/test_command_schema_compatibility.py` | `bcb43bded5a4813b73c0bf0baeeeb5f27b38f36c5b6978b3087beb02ed029f04` |
| `tests/test_timeline_materialization_authority_review.py` | `cec6806993ec9f48a8ae7c00d80c9e04114894ac66f5ae78467b93daff1f1922` |
| `tests/test_timeline_materialization_continuation.py` | `4c023951ab5cf627b26e86195b9da5a53a3fca1dddec4bc39f82deb18e340bc7` |
| `tests/test_timeline_materialization_join.py` | `3f0456f0cb8826dde308e1dca65720ea216430f2808d4028a2dff96b49bbad34` |
| `tests/test_timeline_projection_ownership.py` | `fb08c97479c6729c6ce9472a7b508877420ef61e4f1a996ef396a19e9f0a9f9b` |

## Verification

Working directory for all commands: `/home/user/work/wt/rt-m2-carrier-catalog-fence-compose`.
Shared dependencies were read-only. Direct pytest used `-B`, disabled bytecode and
cacheprovider, and private `/tmp` basetemps; Ruff used `--no-cache`. The central
service uses its own runner settings, shown in its result summary.
No full suite or comprehensive native pair was requested.

Neutral offline controls:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-fence-offline tests/test_timeline_projection_ownership.py tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py tests/test_timeline_projection_occupancy.py tests/test_shot_candidate_promotion.py::test_catalog_promotion_checks_bytes_and_rolls_back_before_receipt
# 213 passed, 3 deselected, 102.22s; includes strict old-public negative/current typed positive.
# Ran before adding the integration-only regression; final product source is identical.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-fence-generators tests/test_command_schema_compatibility.py tests/test_timeline_commit_type_generator.py tests/test_artifact_manifest.py
# 172 passed, 104.91s.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B generators/generate.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B generators/generate.py --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
# All pass; normal generation leaves the reviewed private artifacts unchanged.
```

Minimal actual-provider controls, with the exact frozen Agent source:

```sh
A=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-carrier-catalog-fence-compose/agent-source
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-fence-native-minimal -m integration tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse tests/test_timeline_projection_ownership.py::test_actual_provider_shared_slot_move_inverse_redo_and_rematerialization tests/test_timeline_projection_ownership.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore tests/test_render_native_historical_retry.py
# 4 passed, 9.49s.

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-fence-shared -m integration tests/test_timeline_projection_ownership.py::test_source_bound_owned_slot_cannot_overwrite_newer_catalog_head
# 1 passed, 3.06s.

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-fence-unplaced -m integration tests/test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards
# 1 passed, 0.80s.
```

Discriminating control: a private scratch pytest plugin replaces only
`_check_shot_destinations` with its AST-extracted 83fe implementation. The
same new native test then **fails as expected**, `DID NOT RAISE RuntimeErrorBase`
at the current-slot overwrite. This proves the regression detects the omitted
catalog fence. This deliberate negative is not counted as a passing gate.
Exact additional command (same A and working directory as above):

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-carrier-catalog-fence-compose
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A:$W" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -p pre_fence_probe --basetemp=/tmp/rt-carrier-without-fence -m integration tests/test_timeline_projection_ownership.py::test_source_bound_owned_slot_cannot_overwrite_newer_catalog_head
# Expected discriminating failure: 1 failed, 3.59s; product files never changed.
```

Central socket-capable current test lane:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$O/bin/request-test rt-m2-carrier-catalog-fence-compose targeted --files "tests/test_shot_candidate_promotion.py tests/test_door_transport.py tests/test_timeline_empty_shell_repair.py tests/test_timeline_fresh_bootstrap_scope.py tests/test_timeline_shot_authority.py tests/test_timeline_commit_closure_invariants.py"
$O/bin/wait-test rt-m2-carrier-catalog-fence-compose-targeted-1020151404-11145 1
```

**PASS: 209 passed, 3 deselected in 171.29s**, exit 0. The central snapshot
is exact candidate tree `d20b745c26a33c2ea4e20863f846335c8cf33e1e`.
Result directory: `tests/rt-m2-carrier-catalog-fence-compose-targeted-1020151404-11145/`.
No source changed after this snapshot request.

The central neutral lane does not import Agent for integration tests; those
are deselected. Actual-provider results above exclusively use the frozen 3730
archive. Initial `wait-test` returned 124 while the log was growing; the same
request was resumed, never resubmitted.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache --select F runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py runtime_protocol/timeline_materialization.py
# Pass.
git diff --check
# Pass.
```

Including the carrier ownership test in that Ruff command reports 28 F811
shared-fixture redefinition findings. A JSON diagnostic multiset comparison
against its 83fe bytes found exactly the same 28 findings; no new finding was
introduced. No broad formatting rewrite was made.

## Hold and coordinated next steps

No implementation blocker remains. Prior 83fe approval was internal and based
on 16ac; it does not approve this newer composition. After the harness commits:

1. Runtime manager supplies the **actual new commit SHA plus tree d20b745c…**
   and this report for fresh Runtime/Agent source peer review. Do not reuse the
   old 83fe ACK as approval for this tree.
2. Once the new committed counterpart receives that review, coordinate **one**
   final native lifecycle/ACK/restart/own-slot/global-item pair and one matched
   normal private artifact with Agent frozen 3730/f802. The present six bounded
   native controls are not that comprehensive qualification. Current Agent
   integration does not qualify this carrier. Avoid duplicate comprehensive
   native/full runs.
3. Final public/adoption judgment remains with the orchestrator. Public pin,
   release, freeze, activation and merge remain held here.
