# Runtime current production tuple (DRAFT)

Status: **DRAFT, not published.** Drafted 2026-10-20 from Runtime `tl/integration` @ `84be33c` (read-only). The published `design/runtime-current-tuple.md` replaces this after the regeneration in section 5. Every `TBD` names who fills it. Nothing here is a qualification; no test was run for this draft.

Decision it implements (orchestrator, 05:36Z): ONE current production tuple, published by Runtime. Historical tuples are listed in section 2 and are never relabelled.

## 1. Current tuple (pre-regeneration, what integration serves today)

| Field | Value at 84be33c | Source | Final value |
|---|---|---|---|
| Runtime server SHA | `84be33c` (`Merge tl/rt-m2-restore-route-headless-deny`) | `git rev-parse` | TBD: Runtime manager, at regen |
| PROTOCOL | `workspace.v1` | contract metadata | unchanged |
| CONTRACT_VERSION | `0.2.8` | `generators/release.json`, `packages/python/astrid_runtime_client/contract_metadata.py`, `packages/typescript/src/contract-metadata.ts` | TBD: Runtime manager; see 4.1 (0.2.8 already exists as a pre-regen candidate) |
| SCHEMA_DIGEST | `sha256:a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a` | contract metadata (python client and runtime_protocol copies agree) | TBD: regen |
| COMPONENT_MANIFEST_SHA256 | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` | contract metadata | unchanged since 0.2.2 |
| Python client version | `0.2.8` (`packages/python/pyproject.toml`) | pyproject | TBD: regen (render_package_versions) |
| TypeScript client version | `@astrid/runtime-client 0.2.8` (`packages/typescript/package.json`) | package.json | TBD: regen |
| Artifact manifest version | `sha256:4010d93be2a8bfc7cc051c383e165ff81835c3d12ba9a137279741b7883748a7` (`contract/artifacts.json` `version`) | artifacts.json | TBD: regen (`scripts/artifact_manifest.py`) |
| `contract/manifest.json` | `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14` | artifacts.json | TBD: regen |
| OpenAPI `contract/openapi/workspace-v1.yaml` | `sha256:578cf2336dcc9ff12f68738a91608fbc13f606964ae1bdc48219ea467f37a07d` | artifacts.json | TBD: regen (retired-ops removal) |
| `contract/schemas/edit-command.json` | `sha256:472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` (frozen "ordinary 12 ops" file) | artifacts.json | TBD: Agent manager posts exact SHA (see 4.2) |
| `contract/schemas/timeline-commit.json` | `sha256:7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8` | artifacts.json | TBD: regen |
| Operations in OpenAPI | 142 operationIds: 52 GET, 1 HEAD (`headObject`), 89 POST/PUT/PATCH/DELETE | Grep of OpenAPI | TBD: 133 expected after the 9 removals (section 4.1) |
| Artifact manifest `--check` | **not run here** (sandbox refused the command) | — | TBD: regen worker, before the tuple is published |

### 1.1 M1 safety fixes included (all on integration 84be33c)

| Fix | Commit(s) on integration | Behaviour | Test-side evidence |
|---|---|---|---|
| Occupied destination refused atomically | `d17e732` fix, merged `9f9b25c` | Projection destination held by an unrelated row: `reject("destination_occupied")` (`timeline_commit_store.py:575,588,625`) → refused (409 conflict, per the commit port), no partial write | permanent regression test (M1 record) |
| Null-speed first clip | `d79758d` fix, `6db1d88` test, merged `4bb1d0f` | Null clip speed defaults during inspection; retained reads do not rewrite images | M1 record: null speed (4bb1d0f7) |
| Headless deny (empty publication over hidden content) | `37ac0d6` (headless bootstrap guard), `0ab8217` (refuse empty publication over hidden headless content), merged `84be33c` | Authored headless shell is never overwritten by an empty default; document-content deny | App probe kept as permanent test (STATUS 06:25/07:32) |
| Shell adoption refuses timeline scope | `191392e` fix, merged `33b3ccc` | An empty shell carrying timeline-keyed rows (shots, references, dependency rows) is refused, not adopted | 26 pass (STATUS 06:28) |
| Composition-revisions publish route restored | `da5f44e`, merged in `84be33c` | `POST …/composition-revisions` answers again until App migrates (2026-10-20 sequencing decision) | 409 `stale_head` for the 37ac0d6 counterexample (STATUS 06:15) |
| Opaque item-reference remap | **Agent-side**, not in Runtime | — | Agent `a76c6537` + App `c8566f12d` (M1 record) |

Known open items on this tuple: D-c (publish route re-retirement waits for App AND Agent consumers), D-d (UTF-8 text first-use is KEPT in the ledger but refused on integration, RT02 open), D-b (`archiveTimeline` / `recoverTimeline` have no named replacement).

## 2. Historical tuples (frozen; never relabelled)

| Tuple | Runtime commit | CONTRACT_VERSION | SCHEMA_DIGEST | Status |
|---|---|---|---|---|
| M1 recorded (03:55Z) | `4bb1d0f` (`4bb1d0f7` in the plan) | `0.2.1` | `sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d` | Historical record; its contract is 0.2.1, not 0.2.8. Do not describe it as current. |
| Public10 pair | `6be9706` (`fix(runtime-client): export TrackSetArgs`, 2026-10-19 23:57Z) | `0.2.2` | `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` | **Frozen.** Runtime told Agent it may pin it for fc6c1f26 (05:45Z). Never relabelled. Floor snapshot `tests/fixtures/published-command-schemas/runtime-0.2.2.json` is historical only. |
| 0.2.3 floor | `4c145dc` (2026-10-20 02:15Z) | `0.2.3` | `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` | **Frozen.** Live compatibility floor: `runtime-0.2.3.json`, advanced only after an authorised publication. Never relabelled. |

Also not current: branch-only versions `0.2.4` (D13 guard, `bbf2eaa` cohort), `0.2.5` (itemref standalone), `0.2.6` (popup verified-media candidate). They were never on integration; do not reuse their numbers for new content.

## 3. Supported command registry (as shipped in `contract/schemas/edit-command.json`)

14 distinct `const` operation names in the shipped file (Grep). The R4 notes call the ordinary set "12 ops"; the two inverse-family names are `timeline.inverse` and `timeline.restore`.

| Family | Ops |
|---|---|
| Clip | `clip.add`, `clip.move`, `clip.set`, `clip.set-params`, `clip.trim`, `clip.split`, `clip.delete` |
| Track | `track.create`, `track.set` |
| Occurrence media | `occurrence.add-media`, `occurrence.swap-media` |
| Placement | `placement.move` |
| Inverse (restore machinery) | `timeline.inverse`, `timeline.restore` |

Items the regeneration adds (guarded auto-placement ops, selected-media and task-attempt fences, the four itemref patterns): TBD, Agent manager, see 4.2. Do not state this list as final until the Agent SHA is posted.

## 4. Pending changes into the next regeneration

### 4.1 Runtime side (Runtime manager)

| # | Change | Branch / state at drafting | Effect on tuple | Status |
|---|---|---|---|---|
| a | Remove 9 REMOVABLE retired operations from OpenAPI and generated clients; 410 handlers stay (D-a) | `tl/rt-m2-contract-retired-ops-removal` at `1f3e64d` (no commit on top at drafting; worker in flight) | OpenAPI 142 → 133 ops; both generated clients | Pending worker. Rows: `updateTimeline`; timeline-scoped `createShot`, `createReference`, `updateReference`, `archiveReference`, `recoverReference`; `updateShot`, `archiveShot`, `recoverShot` |
| a' | 17 WAITS retired ops stay in the contract until their consumers migrate | census `design/runtime-api-surface.md` | none | Not removed in this regen |
| b | D13 producer guard/proposal cohort | `tl/rt-m2-d13-forward` at `5a394fd`, HELD. Forward-merged on integration; 317 D13 tests pass; 4 generated-client tests fail until regeneration | Needs `python generators/generate.py`. Do NOT reapply 0.2.4 | HELD until regen |
| c | Verified-read family consolidated internally (one helper, one route table, shared 400/409 responses in the contract). Wire operations unchanged | `tl/rt-m2-verified-read-consolidate` at `1f3e64d` | Additive contract text only | Pending worker; wire names must not change |
| d | Read-envelope → canonical image conversion | Agent construction (02:42 decision); Runtime validates through the same projector | none until Agent posts | Blocked on Agent |

### 4.2 Agent side (Agent manager; SHA TBD)

| Item | Value |
|---|---|
| Agent canonical commit SHA whose schema is baked in | TBD: Agent manager (posted in `design/runtime-coordination.md`) |
| `edit-command.schema.json` sha256 (byte-identical copy in Runtime) | TBD: Agent manager |
| Superset-guard helper commit | TBD: Agent manager |
| Contents: guarded auto-placement ops; selected-media and task-attempt fences; four itemref patterns; 12 ordinary ops | TBD: Agent manager |
| Fallback if not posted | Runtime's stated fallback is Agent `tl/integration` HEAD at generation time, with the superset guard against 0.2.2 and 0.2.3. This draft recommends against the fallback: the tuple must name the exact SHA |

### 4.3 Version number (orchestrator decision)

`CONTRACT_VERSION` 0.2.8 already exists on integration as a pre-regeneration candidate (`pack-document-read` merge, App not yet paired). The regenerated contract changes `SCHEMA_DIGEST`, so keeping `0.2.8` would reuse a version label for different bytes. **Recommendation:** bump to the next free version. Number TBD: orchestrator (must not collide with the branch-only 0.2.4–0.2.6 labels).

## 5. Regeneration procedure (run from one regen worktree; interpreter `/home/user/work/venv-runtime/bin/python`; never reinstall the venv)

```
# inputs in place: 4.1 a+b (+c), 4.2 Agent schema byte-identical to contract/schemas/edit-command.json
# 1. set generators/release.json contract_version = <NEW, TBD orchestrator>
python generators/generate.py            # validate_command_schema (superset guard vs runtime-0.2.3.json), then rewrites:
                                         #   3 contract_metadata modules, TS contract-metadata.ts, package versions,
                                         #   packages/python/.../generated.py, packages/typescript/src/generated.ts,
                                         #   commit types/resources, client __init__.py
python scripts/artifact_manifest.py      # rewrites contract/artifacts.json and manifest version
python generators/generate.py --check    # must print nothing and exit 0
python scripts/artifact_manifest.py --check
python -m pytest -q tests/test_command_schema_compatibility.py tests/test_generated_client.py \
    tests/test_client_parity.py tests/test_artifact_manifest.py \
    tests/test_authored_json_key_parity.py tests/test_installed_wheel_source_parity.py
cd packages/typescript && npm test       # build + tsc --strict public-api + node --test
# full suite: ONLY through the central service (full-restore-integration; plain `full` lacks ASTRID_CHECKOUT). Once, after the last change.
```

Gates that must be green before publishing the tuple: `generators/command_schema_compatibility.py` superset guard (inside `generate.py`); `test_command_schema_compatibility.py` (incl. `test_frozen_fixture_digests`, the D13 guard test, and the historical regex-review test that expects exactly 5 errors on 0.2.2); `test_generated_client.py`; `test_client_parity.py`; artifact manifest `--check`. The 4 currently failing generated-client tests must pass after regeneration, not be edited.

Consumers: Agent's vendored `astrid_runtime_client/generated.py` and App's `src/integrations/runtime/generated.ts` change only through their own pin moves (TBD: Agent and App managers). This regen does not edit them.

## 6. Frozen fixtures (no change in this regen)

`tests/fixtures/published-command-schemas/`: `runtime-0.2.3.json` (floor, 1,330 lines), `runtime-0.2.2.json` (historical, 729), `withdrawn-10c.json` (negative oracle, 889), `producer-guard-1bffd.json` (D13 positive oracle, 1,510), `sources.json` (23). All are read by tests or the generator. None are in the artifact manifest. Trimming (~4.4k lines) is an owner decision, not part of this tuple.

## 7. Open TBD register

| Item | Owner | Needed for |
|---|---|---|
| Final Runtime server SHA | Runtime manager | publishing the tuple |
| New CONTRACT_VERSION (not 0.2.8) | Orchestrator | 4.3 |
| Agent canonical SHA, edit-command.json sha256, superset-guard commit, op list | Agent manager | 4.2, section 3 |
| Retired-ops removal commit (tl/rt-m2-contract-retired-ops-removal) merged | Runtime manager | 4.1 a |
| D13 cohort merged with regeneration | Runtime manager | 4.1 b |
| Artifact manifest `--check` result | Regen worker | section 1 |
| Final SCHEMA_DIGEST, artifact manifest version, manifest sha | Regen worker | section 1 |
| TS build/test result (`npm test`) | Regen worker | section 5 |
| App and Agent pin moves to the new tuple | App / Agent managers | consumers |
| Read-envelope conversion (Agent-side) | Agent manager | 4.1 d |
| Retired-op 9-row removal vs 17 WAITS, D-b, D-c, D-d | Orchestrator | scope of regen |
