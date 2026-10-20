# Runtime union613 normal private generation

Completed: 2026-10-20T17:52:44Z. Worker: `rt-m2-union613-normal-private-gen`.

## Result and identities

Normal **PRIVATE, unpublished** generation is complete. Existing package version
**0.2.14** is retained. No public release decision, consumer adoption, consumer
pin, metadata override, health override, or native-pair claim is made.

- Runtime starting commit: `b8930da4812ec444a36edd768501041e22f6bc3b`;
  starting tree: `6e0c3d9240cd8fa320d28754f4cd589019e14612`.
- Required current parent: `285a3b437c69d20e2af281c3d7fdd212cb784d1a`.
- Final source tree, independently recomputed without Git writes and confirmed
  by the central test snapshot: **`8c027992e34ddf9a940d3e90cd38f7b9e11e4c25`**.
  Final commit SHA will be assigned by the harness; it does not exist at report time.
- Canonical Agent source commit: **`357230816c86da65d5f8cc92b10a3a90d29874e0`**;
  verified tree: **`94692ec85167d5c606626c4ec678fe2a63ee0aa6`**.
- Agent source path: `astrid/core/timeline/schema/edit-command.schema.json`.
  Its raw bytes and Runtime `contract/schemas/edit-command.json` both have
  SHA-256 **`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`**.
- PRIVATE Runtime contract/health schema digest:
  **`sha256:ddf6396dc32bd54bfeed549a99034693eaed76478b45ad0b7242117f6b734d36`**.
- PRIVATE artifact manifest version (75 artifacts):
  **`sha256:0a9a899123e94522abf8b7286a7d48b0da2f2071de10490884aa8db8dff01e26`**.
- Manifest file SHA-256:
  `b8f91fdbe598603c9649ce54db2690d7c899b5ff5b264537d0b69760d1b3e117`.

These identities name this new private source tree, not immutable a0/f021 normal
014 or public 013. Neither frozen checkout/ref nor any other repo was modified.

## Changes and preservation

1. Retained b893's complete materialization join, private capture checks,
   authenticated historical allocation checks, slot ownership, item/occupancy,
   promotion/global-head, raw BASE-plus-declared-pin and single-FD guards and tests.
   `timeline_commit.py`, `timeline_commit_port.py`, `timeline_commit_store.py`,
   and `timeline_materialization.py` remain byte-identical to b893.
2. Carried CURRENT285's publication-only producer Task-input guard and its exact
   UTF-8/script/CAS/restart regression. `store.py` now equals CURRENT285 exactly.
   `cas.py` and `service.py` already equal both b893 and CURRENT285, retaining
   WAV duration, explicit-null and invalid-rate handling and HTTP behavior.
   Carried CURRENT285's visual-lane custom-picture fix and corresponding tests.
3. Applied approved `ff0f69b11e12d5b2a0ea2f07a443874a15f51ca9` compatibility
   helper and null-keyword regression. No compatibility regex bypass was added.
4. Added normal CLI source import with an exact reviewed-source hash check,
   recorded in `generators/agent-command-source.json`. This is generator input
   provenance, **not an Agent consumer pin**. Arbitrary compatible source paths
   still refuse before writing. Default `--check` verifies the imported freeze.
5. Fixed the real generator defects: operation `allOf` conditionals now render
   complete per-op command unions; required-only object union branches retain
   their shared fields instead of `Any`; Python forward references are bound
   to their own module to prevent cross-module union caching from resolving to
   the other generated DTO module. All 55 source definitions are emitted.
6. Kept all seven public source DTO exports, including Python package-root
   exports, and repaired TypeScript root `WordAnchor` export in the generator.
   TypeScript MutationReceipt `project_seq` remains a two-element tuple, with
   short/long tuple rejection tested. Generated outputs were produced through
   the normal Python/TypeScript/resource/digest/artifact pipeline.
7. Four pre-generation schema-hold cases were advanced one-for-one: the public
   frozen S2 validator still rejects the carrier claims; the new private schema
   admits a complete source-bound preview or reaches semantic execution. Closed
   malformed args still refuse before execution; unchanged snapshot assertions
   remain. Those are exactly the two parametrized tail tests in
   `test_timeline_materialization_join.py` and
   `test_timeline_projection_ownership.py`. All other join/slot/ownership
   positives, adversarial cases and strict marks were retained.

## Source discrepancy and deliberate limits

**The exact frozen source has 12, not 13, operations with a v2 branch.** It has
55 definitions, 29 operation conditionals, and **41 generated command branches**
(29 original branches + 12 v2 branches). Verified v2 operations:
`track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `clip.move`,
`occurrence.add-media`, `occurrence.swap-media`, `placement.move`,
`placement.create`, `placement.unplace`, `shot.pool`, `clip.set`.
The source leaves `track.create.version` as a string; this was preserved, not
silently narrowed. The report/brief's 13-v2 inventory needs correction or a
separately reviewed Agent successor; no thirteenth branch was invented.

The ordinary source projection (remove the 12 v2 branches and the additive
item-reference alternatives) exactly reproduces b893's complete 55-definition,
29-operation ordinary schema and SHA-256
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
All five immutable historical floors are checked by normal generation:
Runtime 0.2.2 (reviewed widening proof), 0.2.3, 0.2.10, and both Agent S1/S2
floors. No floor fixture was changed or truncated to the earlier eight-definition
loss. Complete structural containment, not sample-only compatibility, is used.

Runtime's source-bound join adversarial tests prove missing/forged/private
capture and allocation evidence refuses. These are Runtime boundary tests with
prepared fixtures, **not proof that actual Agent357 emits, refuses old unsafe
partial-v1 submissions, executes, retries, or inverses those native commands**.
That native behavior remains for the single actual paired proof after reviews
and a new matching Agent private consumer pin. No native duplicate was run.

The two old 013 parent-ownership cases in `tests/test_timeline_clip_replacement.py`
remain byte-identical to b893:
`test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema`
and `test_native_parent_clip_swap_route_replaces_parent_media` (the latter keeps
its existing strict xfail and all positive assertions). They are the specified
expected version-transition RED/XPASS requirements on 014, not requalified
passes here; neither was run or flipped. Six integration requirements were deselected by the repo's normal integration
exclusion: three source-bound ownership cases, the existing native occupancy
and acceptance cases, and one cross-repo visual-fixture comparison.

## Exact generation and checks

All commands ran from `/home/user/work/wt/rt-m2-union613-normal-private-gen`.
`P=/home/user/work/venv-runtime/bin/python` below; each Python command used
`PYTHONDONTWRITEBYTECODE=1`. Shared dependencies were read-only; no installs.
The external source was exported read-only using `git show` of exact Agent357
and hash-checked into this worker's `agent-edit-command.schema.json`.

```sh
$P generators/generate.py --agent-command-schema /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-union613-normal-private-gen/agent-edit-command.schema.json
$P generators/generate.py
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --output-root /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-union613-normal-private-gen/ts-generated
$P scripts/artifact_manifest.py
```

The two TS conformance outputs were copied from that normal generator's
worker-local output directory to their checked-in destinations. No generated
content was edited by hand. Final read-only checks all exited **0**:

```sh
$P generators/generate.py --check
$P generators/generate.py --check --agent-command-schema /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-union613-normal-private-gen/agent-edit-command.schema.json
$P scripts/artifact_manifest.py --check
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root . --fixture-root conformance/fixtures
tsc --noEmit -p packages/typescript/tsconfig.json
tsc --noEmit -p conformance/tsconfig.json
git diff --check
```

Final local contract/generator command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py tests/test_timeline_current_union_contract.py tests/test_typescript_generator.py tests/test_client_parity.py tests/test_client_release.py tests/test_python_client_public_api.py tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py
```

**218 passed in 59.09s.** Includes Python namespace separation, every generated
source definition/command branch, 29 operations' native args/closed-key checks,
public TS exports/positive-and-negative fixtures, tuple bounds, all historical
compatibility gates, source hash rejection, conformance generator reproducibility
and artifact parity.

Final local source-bound/slot/core command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py tests/test_timeline_projection_ownership.py tests/test_timeline_projection_occupancy.py tests/test_timeline_raw_audio_port.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_checkpoint.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_selection.py tests/test_timeline_commit_contract.py tests/test_timeline_bundle2_contract.py tests/test_visual_seam_admission.py tests/test_canonical_render_admission.py tests/test_timeline_commit_port.py tests/test_timeline_commit_acceptance.py
```

**645 passed, 6 deselected in 102.92s.** No xfail/skip or weakened guard was added.

Central socket/HTTP check:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-union613-normal-private-gen targeted --files 'tests/test_timeline_legacy_occupancy.py tests/test_timeline_null_speed_retained.py tests/test_generated_client.py tests/test_generation_publish_v1_settlement.py tests/test_worker_security_settlement.py tests/test_timeline_verified_media_http.py'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-m2-union613-normal-private-gen-targeted-1020174937-16660 1
```

**131 passed in 30.83s**, service exit 0, 32s elapsed, exact final tree
`8c027992e34ddf9a940d3e90cd38f7b9e11e4c25`.
Result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-union613-normal-private-gen-targeted-1020174937-16660/`.
The runner's exact command is the six-file `python -m pytest -q` selection above.

Earlier diagnostic runs exposed the generator reference/export defects and the
four pre-generation hold assertions described above; all were resolved and the
final selections passed. One earlier broad local neighbor selection accidentally
included `test_exact_f1_over_http`; its socket bind failed with sandbox
`PermissionError`. That selection had 655 passes and the four hold failures.
The socket case was removed from the local selection and passed via the central
service. No local socket result is represented as product failure or green proof.

No full suite, browser suite, native Agent pair, release build, public adoption,
provider/health patch, frame factory, new wire DTO, ID seed or map authority was
introduced or run. Test caches and temporary worktree output were cleaned.

## Source file SHA-256 inventory

- `runtime_protocol/cas.py`: `a926a79b31ee313cdfb4cd07ad919f94c1ace099f8aaa5c15d704cbfb0d34bc8`
- `runtime_protocol/service.py`: `8f0c9ccc25bb627725a512a457702bc2dccd138df2e222159070a9d3e48a3d36`
- `runtime_protocol/store.py`: `89787e3898dfc4cf99d5220f4a4ab9b2dcc7714edab2352023ede3e86d168756`
- `runtime_protocol/timeline_commit.py`: `b981dfd57ab6e6a8b04ffd6558a26d4d088da3685aea006d885e81cb923513f4`
- `runtime_protocol/timeline_commit_port.py`: `ef85355ae063d8ff43d9641ec79c7e405a322681743768ce26d651f795f1e573`
- `runtime_protocol/timeline_commit_store.py`: `503cf6a33f1817c4c69b1cbd99859c05ba8a33b8f41d4ac8e1107ea92b5c5203`
- `runtime_protocol/timeline_materialization.py`: `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb`
- `runtime_protocol/timeline_commit_inputs.py`: `bf04dc5d26fd6e6283ae11c7d0fa55fa5730c45f19e1c55bda529062cab696e4`
- `runtime_protocol/timeline_commit_producer.py`: `12bc59c54e47db5a950dd8e4828609931fabf481fce760d7d6fe794d72f7b33b`
- `runtime_protocol/timeline_commit_producer_checkpoint.py`: `7ce299ffd987462f0fefa7dc7973e9f8515d10e3945bdc5677b5b19f77205795`
- `runtime_protocol/visual_seam.py`: `85986492c86e42ec84fb7bed23f069cc0b711f69558fff65ab77ee8f1534178b`
- `generators/generate.py`: `f05717ae12c519ee9d0edb97be22b5b9ba4eac74f8df569ee8885161d8f73654`
- `generators/timeline_commit_types.py`: `485a35ebec9ef1a1f6ab89e141311bdc4a722f3d817284699d57eda1df85babf`
- `generators/command_schema_compatibility.py`: `57cfb2e5c8cf50be2d5c47ec815e7e0f5d1109dc41bfb405402889a4dd11b90b`
- `generators/python_client_init_template.py`: `d6c751d5ba1b4f2e97235caf558a39c04db007c7948a6d3ab0afefb08ca6a4cc`
- `generators/agent-command-source.json`: `2fd6259d2a6da5a13931b5a9e391973eaee05cf38f34ed65ca1d5a2c2ba1e292`
- `contract/schemas/edit-command.json`: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- `contract/artifacts.json`: `b8f91fdbe598603c9649ce54db2690d7c899b5ff5b264537d0b69760d1b3e117`
- `runtime_protocol/schemas/timeline-commit-bundle.json`: `4a0779db14b9bbd827e964a495367b465bab5c00ee0b5717b8ff27777010a858`
- `runtime_protocol/timeline_commit_types.py`: `ad8deaf65feafb88158d2747d1df2751cde3a0f06d5f122e0d2827c91a846e9c`
- `packages/python/astrid_runtime_client/timeline_commit_types.py`: `ad8deaf65feafb88158d2747d1df2751cde3a0f06d5f122e0d2827c91a846e9c`
- `packages/typescript/src/timeline-commit-types.ts`: `970d306de53e35bb7cd8c599f84f1f5ae62ad23a425987c48048f962afe78828`
- `tests/test_timeline_clip_replacement.py`: `dd74fd0f76a9c986000f75f36c836d51b269dbbc31b6db69dfa37768583d033e`

## Handoff

Review this exact private tree against CURRENT285 and Agent357. After both
reviews and the new Agent private consumer pin, Agent owns ONE actual357 native
pair, including unsafe partial-v1 refusal, current-version success, retry,
restart, undo/redo and parent-ownership restoration. Keep the two old strict
requirements unchanged until that actual paired proof justifies their update.
The harness may commit this tree; there is no remaining worker blocker.
