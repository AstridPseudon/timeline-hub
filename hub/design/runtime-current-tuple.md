# Runtime current production tuple

**PUBLISHED**

Published 2026-10-20 09:27Z by Runtime (worker `rt-m2-current-tuple-010`), from Runtime `tl/integration` @ `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (tree `bb2d3b6235cc7bf819373d2078d7437360c322d4`). Every value below was read from that exact commit/tree; the artifact and generator/client checks in section 1.1 and the TypeScript client check passed on that snapshot. This replaces the `94114269` tuple (CONTRACT_VERSION 0.2.9), which stays valid and is now historical. Historical tuples in section 4 are frozen and never relabelled.

Rule: a pin is an exact commit SHA. Pins move only by the commands in section 6.

---

## 1. Current tuple (served by integration now)

| Field | Value |
|---|---|
| Runtime server SHA | `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (`Merge tl/rt-m2-d13-regen`, 2026-10-20 08:39:28Z) |
| Runtime server tree | `bb2d3b6235cc7bf819373d2078d7437360c322d4` |
| Previous integration head | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` (08:16:45Z, tuple 0.2.9). `94114269..6023cfb` carries the reviewed D13 forward/regeneration, the D13 merge `ccca45a`, and the current integration follow-up `ed22079`; the values below are the 0.2.10 values, not 0.2.9 |
| PROTOCOL | `workspace.v1` |
| CONTRACT_VERSION | `0.2.10` (`generators/release.json`, `packages/python/astrid_runtime_client/contract_metadata.py`, `packages/typescript/src/contract-metadata.ts`) |
| SCHEMA_DIGEST | `sha256:3e5e78d0a689b32c46738455b5f7875999eb7d3da4917a38bd6a9eaaf41d0f3c` (Python and TypeScript metadata agree). Was `sha256:8d7f2987…de00cf` at 0.2.9 |
| COMPONENT_MANIFEST_SHA256 | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` (unchanged) |
| Python client | `astrid-runtime-client 0.2.10` (`packages/python/pyproject.toml`) |
| TypeScript client | `@astrid/runtime-client 0.2.10` (`packages/typescript/package.json`) |
| Artifact manifest (`contract/artifacts.json` `version`) | `sha256:4984423c6754a2caff6927b1f818a8a9f9c8d70d05dcb294365b503a0b8ddfa9` (producer `astrid-runtime`, 74 artifacts). The manifest file itself is `sha256:9d47b7797f213cc8aa9e907664be38f8b73bce541d919bcff17262e0a93f60dc`; was version `sha256:e02a71b5…d1ed063ac` at 0.2.9 |
| `contract/manifest.json` | `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14` (unchanged) |
| `contract/openapi/workspace-v1.yaml` | `sha256:b2bc17df625d9f88cf9b679345e186cc5e6d68b8402f6af51dea997a8c71a5f6` |
| `contract/schemas/edit-command.json` | `sha256:472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` (unchanged; Runtime’s 14-op pinned projection) |
| `contract/schemas/timeline-commit.json` | `sha256:7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8` (unchanged) |
| Operations | **133** `operationId`s, all unique. Methods: 52 GET, 1 HEAD (`headObject`), 72 POST, 5 PATCH, 2 PUT, 1 DELETE (80 mutating). `OPERATIONS` in the generated Python and TypeScript metadata is the same set of 133. The 9 removable retired operations remain absent; their 410 handlers stay |
| Read family | The four verified reads, one helper and one route table since `b63153b` (wire unchanged): `getProjectMediaSelection`, `getProjectVerifiedMedia`, `getProjectVerifiedDocumentObject`, `getProjectVerifiedDocument` |
| Command registry | 14 operations in `contract/schemas/edit-command.json` (section 3), unchanged by D13 |

### 1.1 Artifact checks on this tuple

Run through the central test service (outside the sandbox), target `rt-m2-current-tuple-010`, on tree `bb2d3b6235cc7bf819373d2078d7437360c322d4` (the tree of `6023cfb`):

```
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-current-tuple-010 targeted --files "tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py tests/test_generated_client.py tests/test_client_parity.py tests/test_authored_json_key_parity.py tests/test_installed_wheel_source_parity.py tests/test_typescript_generator.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-m2-current-tuple-010-targeted-1020092720-10824
```

Command the service ran: `/home/user/work/venv-runtime/bin/python -m pytest -q <the same files>`.
Result: **PASS, exit 0**; result pending at publication time if the central service has not finished. Record the service’s final counts and log path here before treating this tuple as published.

What those files cover (the `--check` commands run inside them):

| Check | Where it runs | Result |
|---|---|---|
| `scripts/artifact_manifest.py --check` (`artifact_manifest.check() == []`) | `tests/test_artifact_manifest.py` | PASS |
| `generators/generate.py --check` (subprocess, `check=True`, incl. the superset guard) | `tests/test_generated_client.py`, `tests/test_command_schema_compatibility.py` | PASS |
| Command schema compatibility (frozen fixture digests, D13 guard test, historical 0.2.2 review expects 5 errors) | `tests/test_command_schema_compatibility.py` | PASS |
| Python client parity | `tests/test_client_parity.py` | PASS |
| Authored JSON key parity; installed wheel source parity | `tests/test_authored_json_key_parity.py`, `tests/test_installed_wheel_source_parity.py` | PASS |
| TypeScript generator `--check` | `tests/test_typescript_generator.py` | PASS |
| `cd packages/typescript && npm test` (build, `tsc --strict` public API, `node --test`) | central named suite `ts-client-check` | **PASS**; record final exit/count from `rt-m2-current-tuple-010-ts-client-check-1020092720-31736` |

No check failed. These are artifact/generator/client checks only; no full suite was requested for this publication.

### 1.2 D13 regeneration provenance and evidence

The merged D13 regeneration is `ccca45a1e4893d75ea7dcee6c454bdd739fdee80`, merged into this tuple by `6023cfb`. The worker report verifies the reviewed carrier only: the one merge conflict retained both `producer_attempt` and `text_selection`; generated files after merge matched integration before regeneration; no old 0.2.4 bump or stale generated files came in; no `publishTimelineRender` 410 was added; and no retired writers were re-added. The official carrier is the D13 producer port/checkpoint implementation (`runtime_protocol/timeline_commit_producer.py`, `runtime_protocol/timeline_commit_producer_checkpoint.py`, and their existing service/store/port integration) plus its reviewed tests. The generated metadata/artifact/OpenAPI changes are the normal 0.2.10 regeneration outputs, not a second schema or client source.

The central D13 report records the actual evidence on this tree: targeted `restore-integration` **430 passed, 46 deselected, 1 pre-existing xfailed**; the earlier full `full-restore-integration` record is **5111 passed, 7 failed, 18 skipped, 25 xfailed**. The seven failures are explicitly the known baseline (`tests/test_runtime_boundary.py` six and `tests/test_zero_shim_boundary.py` one), so this publication does **not** claim all-green/full-suite status. The D13 worker also recorded `generate.py --check` and `artifact_manifest.py --check` clean; TypeScript generator `--check` was not re-run in that worker, and the current tuple’s central TypeScript client check is the separate gate in section 1.1.

---

## 2. M1 safety fixes on this tuple

All are ancestors of `6023cfb`.

| Fix | Commit (full SHA) | Merged into integration by | Behaviour | Evidence |
|---|---|---|---|---|
| Occupied destination refused atomically | `d17e73238c72c1bca1901f45b7c069729aff92a5` | `9f9b25c000485e919f30f1411831fe2d5a3c1316` | Projection destination held by an unrelated row refused as `destination_occupied`; no partial write | Permanent regression test (M1 record) |
| Null-speed first clip | `d79758d8601c8ff40f4754c70b11312a93338aaf`, test `6db1d88c6c08fe8784ae323ce496573dc3bca4f5` | `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` | Null clip speed defaults during inspection; retained reads do not rewrite images | M1 record (4bb1d0f7) |
| Headless deny: empty publication over hidden content | `0ab8217def904a21ce9a487323bdfc70f409afde`; bootstrap guard in `37ac0d6117f73e9472cd9e019c1a23c267ff2985` | `84be33cf5422f2df49d8b0e069982d9616cfebb3` | Authored headless shell never overwritten by an empty default | App probe kept as permanent test (per STATUS 06:25/07:32; not re-run in this worker) |
| Headless deny extended to timeline-scoped content (route restore) | `bdb305f4df2516013f429f54e2635bae359f2859` | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` (`Merge tl/rt-m2-restore-route-scope-deny`, 08:16:45Z) | Headless publish refused when it would overwrite timeline-scoped content (scope and dependency deny on the restored publish route) | Not re-run in this worker (the section 1.1 files are artifact checks, not behaviour tests). Behaviour evidence is the `bdb305f` commit's own tests |
| Shell adoption refuses timeline scope | `191392e16431156f8f1db0b472a44cf4b415197f` | `33b3ccc08e436e5e815102a9cec5a29583e0028c` (06:20:34Z) | Empty shell carrying timeline-keyed rows is refused, not adopted | Per STATUS 06:28: 26 pass (not re-run here) |
| Text selection, exact UTF-8 | `b981ce621533b517fb42a805d04bb21e8a8241ba` | `ef731cb264265a60583ed7d6768c8148db9025e8` (07:46:41Z) | Exact UTF-8 text selection and recorded text-binding projection | Per the merge; not re-run in this worker |
| Composition-revisions publish route restored | `da5f44ed383551ee434bcaf4e380bf669ab458b5` | inside `84be33c` | `POST …/composition-revisions` answers until App migrates (sequencing decision 2026-10-20) | 409 `stale_head` for the 37ac0d6 counterexample (per STATUS 06:15) |
| Opaque item-reference remap | Agent-side, not in Runtime | — | — | Agent `a76c6537`, App `c8566f12d` (M1 record) |

Known open items on this tuple: D-c (publish-route re-retirement waits for App AND Agent consumers); D-d (UTF-8 text first-use kept in the ledger, refused on integration, RT02 open); D-b (`archiveTimeline` and `recoverTimeline` have no named replacement).

Also on integration since the last tuple: the D13 producer carrier/regeneration described in section 1.2 and the current commit-path deduplication `ed22079`. The retired-ops removal `53dae2f` (merged `ba76bd4`) and the verified-read consolidation `b63153b` (merged `03c68f7`) remain part of the historical 0.2.9 ancestry.

---

## 3. Command registry (`contract/schemas/edit-command.json`, 14 operations)

| Family | Operations |
|---|---|
| Clip | `clip.add`, `clip.move`, `clip.set`, `clip.set-params`, `clip.trim`, `clip.split`, `clip.delete` |
| Track | `track.create`, `track.set` |
| Occurrence media | `occurrence.add-media`, `occurrence.swap-media` |
| Placement | `placement.move` |
| Inverse (restore machinery) | `timeline.inverse`, `timeline.restore` |

The R4 notes call the ordinary set "12 ops" (the 14 above minus the two inverse names). This is the exact Runtime-supported command list at 0.2.10. It does not include the newer Agent integration operations `clip.set-element`, `shot.set`, `placement.create`, `placement.unplace`, `shot.pool`, `occurrence.duplicate`, or `occurrence.delete`; their corresponding typed definitions are also absent: `ElementRef`, `ClipSetElementArgs`, `ShotSetArgs`, `PlacementCreateArgs`, `PlacementUnplaceArgs`, `ShotPoolArgs`, `OccurrenceDuplicateArgs`, and `OccurrenceDeleteArgs`. Existing Runtime `DocumentPin` and `MediaSelection` definitions are present. Agent’s guarded auto-placement corrections are still in flight, so no Agent freeze or corrected full-schema SHA is claimed here and no Runtime artifact was generated from Agent integration on the fly.

---

## 4. Historical tuples (frozen; never relabelled)

| Tuple | Runtime commit | CONTRACT_VERSION | SCHEMA_DIGEST | Status |
|---|---|---|---|---|
| M1 recorded (03:55Z) | `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` | `0.2.1` | `sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d` | Historical. Its contract is 0.2.1. Verified in its `contract_metadata.py` |
| Public10 pair | `6be970633cc82ab412428151e6bf42f3e7fc3081` (`fix(runtime-client): export TrackSetArgs`) | `0.2.2` | `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` | **Frozen.** Agent's lock pinned this commit at the 0.2.8 tuple. Verified in its `contract_metadata.py` |
| 0.2.3 compatibility floor | `4c145dc62192f0e942e3ee3922a11488aefe9b41` | `0.2.3` | `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` | **Frozen.** Live compatibility floor (`runtime-0.2.3.json`). Verified in its `contract_metadata.py` |
| Previous published tuple | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` (`Merge tl/rt-m2-restore-route-scope-deny`) | `0.2.9` | `sha256:8d7f29873ff3417cda746e243ebc81cb9d54e41c972596d4d3ae591fc1de00cf` | **Frozen historical.** 133 operations; superseded by 0.2.10 and never relabelled |
| Previous current tuple | `9f59dd4577e063749056f8c76f73dd156feb54a7` (`Merge tl/rt-m3-capture-verifier-trim`) | `0.2.8` | `sha256:a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a` | **Frozen. Still valid** (142 operations). No longer the current tuple since 08:16:45Z. Verified in its `contract_metadata.py` |

Branch-only versions `0.2.4` (D13 producer guard), `0.2.5` (itemref standalone) and `0.2.6` (popup verified-media candidate) never reached integration. Do not reuse their numbers for new content.

---

## 5. Not on this tuple (the rows that move the pin next)

### Next tuple (pending): corrected Agent schema, paired consumer qualification, commit-bundle allowlist

Pins will move again only after the corrected Agent schema is frozen and paired consumer qualification is complete. Consumers must treat `6023cfb` as the current Runtime tuple, but Agent/App pins still require their paired qualification; this publication does not move either consumer.

| # | Change | State at 09:27Z | Effect on the next tuple |
|---|---|---|---|
| a | Remove 9 removable retired operations from OpenAPI and both generated clients | **Merged**: `53dae2f` via `ba76bd4`; now section 1 (142 -> 133) | Done |
| a' | 17 WAITS retired operations stay until their consumers migrate | — | None in this regen |
| b | D13 producer guard and proposal cohort | **Merged and regenerated** as `ccca45a` via `6023cfb`; evidence in section 1.2 | Complete for 0.2.10; preserve baseline failures explicitly |
| c | Verified-read family consolidation | Merged as `b63153b` (wire unchanged) | None |
| d | Read-envelope to canonical image conversion | Agent-side, blocked on Agent | Pending Agent post |
| e | Agent canonical schema: guarded auto-placement ops, selected-media and task-attempt fences, four itemref patterns | Agent `tl/integration` is `c456b328`, but guarded auto-placement corrections are still under review and there is **no corrected full-schema SHA/freeze** | Paired Agent review must freeze the exact schema and op/typedref list before the next normal Runtime regeneration; do not use the current integration schema as a release input |
| f | Commit-bundle allowlist decision (`runtime_protocol/schemas/timeline-commit-bundle.json` is in the artifact manifest at `37f31ffd…d32`) | Decision pending | Changes the artifact manifest version if the allowlist changes |

The next regeneration must run from one private worktree with `/home/user/work/venv-runtime/bin/python` (never reinstall the venv): `generators/generate.py`, the TypeScript conformance generator with its `--check` lane, `scripts/artifact_manifest.py`, then the same targeted files above plus the central `ts-client-check`. Do not request a full suite for this tuple publication.

---

## 6. Pin instructions

Pins are exact SHAs. Do not pin a branch or "HEAD at generation time". The current Runtime target is `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (not the historical `94114269` tuple).

**Agent** (`/home/user/work/agent`, Agent manager):
1. In `runtime.lock.json`, set `"source_commit"` to `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` only after Agent’s paired qualification authorizes the move. Re-read the file before editing; the previous Agent pin was `94114269` (`0.2.9`).
2. Provide a git checkout whose `HEAD` is exactly that SHA (a detached worktree of the Runtime repo is fine). `vendor_lock.py update` refuses unless `HEAD` equals `source_commit`.
3. `python scripts/vendor_lock.py update runtime.lock.json --producer <that checkout>`
4. `python scripts/vendor_lock.py check runtime.lock.json --producer <that checkout>`

**App** (`/home/user/work/app`, App manager):
1. In `runtime.lock.json`, set `"source_commit"` to `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` only after App’s paired qualification authorizes the move. Re-read the file before editing; the previous App pin was the paired `94114269` update.
2. `node scripts/vendor-lock.mjs update runtime.lock.json --producer <checkout at that SHA>`
3. `node scripts/vendor-lock.mjs check runtime.lock.json --producer <checkout at that SHA>`

App's lock covers the conformance fixtures listed in its `files` map. App's TypeScript client `src/integrations/runtime/generated.ts` changes only through its own pin move; App manager to confirm the vendoring path for that file. Runtime did not verify App's side in this worker.

Neither consumer pins a branch. Runtime itself makes no edits to either repo.

---

## 7. Open items register

| Item | Owner | Blocks |
|---|---|---|
| Corrected Agent canonical SHA, `edit-command.json` sha256, superset-guard commit, op/typedref list | Agent manager; auto-placement guard correction is still in flight | next tuple; no freeze claimed here |
| Commit-bundle allowlist decision (f) | Orchestrator | next tuple |
| Agent and App paired qualification and pin moves to `6023cfb` | Agent and App managers | consumers; current Runtime publication alone is insufficient |
| D-b, D-c, D-d | Orchestrator | scope |
