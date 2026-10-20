# Runtime current production tuple

**DRAFT-READY: PUBLISHED unless the retired-ops regen merges first**

Published 2026-10-20 ~08:00Z by Runtime (worker `rt-m2-tuple-fill`), from Runtime `tl/integration` @ `9f59dd4577e063749056f8c76f73dd156feb54a7` (tree `52acbf1cae4b7cc0eb32535d73d08fcc316a7ed0`). Every value below was read from that commit; the artifact checks in section 1.1 ran on that exact tree and passed. This replaces the 84be33c DRAFT that stood at this path. Historical tuples in section 4 are frozen and never relabelled.

Rule: a pin is an exact commit SHA. Pins move only by the commands in section 6.

---

## 1. Current tuple (served by integration now)

| Field | Value |
|---|---|
| Runtime server SHA | `9f59dd4577e063749056f8c76f73dd156feb54a7` (`Merge tl/rt-m3-capture-verifier-trim`, 2026-10-20 07:53:09Z) |
| Runtime server tree | `52acbf1cae4b7cc0eb32535d73d08fcc316a7ed0` |
| Previous integration head | `ef731cb` (07:46:41Z). `ef731cb..9f59dd4` touches only `runtime_protocol/{capture_validation,snapshot_refs,store}.py`. No contract, generator, package or fixture file changed, so every contract value below is the same at `ef731cb` |
| PROTOCOL | `workspace.v1` |
| CONTRACT_VERSION | `0.2.8` (`generators/release.json`, `packages/python/astrid_runtime_client/contract_metadata.py`, `packages/typescript/src/contract-metadata.ts`) |
| SCHEMA_DIGEST | `sha256:a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a` (python and TypeScript metadata agree) |
| COMPONENT_MANIFEST_SHA256 | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Python client | `astrid-runtime-client 0.2.8` (`packages/python/pyproject.toml`) |
| TypeScript client | `@astrid/runtime-client 0.2.8` (`packages/typescript/package.json`) |
| Artifact manifest (`contract/artifacts.json` `version`) | `sha256:4010d93be2a8bfc7cc051c383e165ff81835c3d12ba9a137279741b7883748a7` (producer `astrid-runtime`) |
| `contract/manifest.json` | `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14` |
| `contract/openapi/workspace-v1.yaml` | `sha256:578cf2336dcc9ff12f68738a91608fbc13f606964ae1bdc48219ea467f37a07d` |
| `contract/schemas/edit-command.json` | `sha256:472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| `contract/schemas/timeline-commit.json` | `sha256:7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8` |
| Operations | **142** `operationId`s, all unique. Methods: 52 GET, 1 HEAD (`headObject`), 78 POST, 8 PATCH, 2 PUT, 1 DELETE (89 mutating). `OPERATIONS` in the generated metadata is the same set of 142 |
| Read family | The four verified reads, one helper and one route table since `b63153b` (wire unchanged): `getProjectMediaSelection`, `getProjectVerifiedMedia`, `getProjectVerifiedDocumentObject`, `getProjectVerifiedDocument` |
| Command registry | 14 operations in `contract/schemas/edit-command.json` (section 3) |

### 1.1 Artifact checks on this tuple

Run through the central test service (outside the sandbox), target `integration:runtime`, suite `targeted`, tree `52acbf1cae4b7cc0eb32535d73d08fcc316a7ed0`:

```
bin/request-test integration:runtime targeted --files "tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py tests/test_generated_client.py tests/test_client_parity.py tests/test_authored_json_key_parity.py tests/test_installed_wheel_source_parity.py tests/test_typescript_generator.py"
bin/wait-test runtime-targeted-1020075430-12652
```

Command the service ran: `/home/user/work/venv-runtime/bin/python -m pytest -q <the same files>`.
Result: **PASS, exit 0, 126 passed, 0 failed, 0 skipped** (log: `orch/tests/runtime-targeted-1020075430-12652/log.txt`).

What those files cover (the `--check` commands run inside them):

| Check | Where it runs | Result |
|---|---|---|
| `scripts/artifact_manifest.py --check` (`artifact_manifest.check() == []`) | `tests/test_artifact_manifest.py` | PASS |
| `generators/generate.py --check` (subprocess, `check=True`, incl. the superset guard) | `tests/test_generated_client.py`, `tests/test_command_schema_compatibility.py` | PASS |
| Command schema compatibility (frozen fixture digests, D13 guard test, historical 0.2.2 review expects 5 errors) | `tests/test_command_schema_compatibility.py` | PASS |
| Python client parity | `tests/test_client_parity.py` | PASS |
| Authored JSON key parity; installed wheel source parity | `tests/test_authored_json_key_parity.py`, `tests/test_installed_wheel_source_parity.py` | PASS |
| TypeScript generator `--check` | `tests/test_typescript_generator.py` | PASS |
| `cd packages/typescript && npm test` (build, `tsc --strict` public API, `node --test`) | not run: no `suites.conf` entry runs npm for Runtime, and this worker may not add one | **NOT RUN.** Pending. Runtime manager to run through a named suite |

No check failed.

---

## 2. M1 safety fixes on this tuple

All are ancestors of `9f59dd4`.

| Fix | Commit (full SHA) | Merged into integration by | Behaviour | Evidence |
|---|---|---|---|---|
| Occupied destination refused atomically | `d17e73238c72c1bca1901f45b7c069729aff92a5` | `9f9b25c000485e919f30f1411831fe2d5a3c1316` | Projection destination held by an unrelated row refused as `destination_occupied`; no partial write | Permanent regression test (M1 record) |
| Null-speed first clip | `d79758d8601c8ff40f4754c70b11312a93338aaf`, test `6db1d88c6c08fe8784ae323ce496573dc3bca4f5` | `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` | Null clip speed defaults during inspection; retained reads do not rewrite images | M1 record (4bb1d0f7) |
| Headless deny: empty publication over hidden content | `0ab8217def904a21ce9a487323bdfc70f409afde`; bootstrap guard in `37ac0d6117f73e9472cd9e019c1a23c267ff2985` | `84be33cf5422f2df49d8b0e069982d9616cfebb3` | Authored headless shell never overwritten by an empty default | App probe kept as permanent test (per STATUS 06:25/07:32; not re-run in this worker) |
| Shell adoption refuses timeline scope | `191392e16431156f8f1db0b472a44cf4b415197f` | `33b3ccc08e436e5e815102a9cec5a29583e0028c` | Empty shell carrying timeline-keyed rows is refused, not adopted | Per STATUS 06:28: 26 pass (not re-run here) |
| Composition-revisions publish route restored | `da5f44ed383551ee434bcaf4e380bf669ab458b5` | inside `84be33c` | `POST …/composition-revisions` answers until App migrates (sequencing decision 2026-10-20) | 409 `stale_head` for the 37ac0d6 counterexample (per STATUS 06:15) |
| Opaque item-reference remap | Agent-side, not in Runtime | — | — | Agent `a76c6537`, App `c8566f12d` (M1 record) |

Known open items on this tuple: D-c (publish-route re-retirement waits for App AND Agent consumers); D-d (UTF-8 text first-use kept in the ledger, refused on integration, RT02 open); D-b (`archiveTimeline` and `recoverTimeline` have no named replacement).

Also on integration since the last tuple: `b981ce6` exact UTF-8 text selection (merged `ef731cb`), `b63153b` verified-read consolidation (merged `03c68f7`), `df9512e` history-API audit tests (merged `0f924a8`). None changes the contract.

---

## 3. Command registry (`contract/schemas/edit-command.json`, 14 operations)

| Family | Operations |
|---|---|
| Clip | `clip.add`, `clip.move`, `clip.set`, `clip.set-params`, `clip.trim`, `clip.split`, `clip.delete` |
| Track | `track.create`, `track.set` |
| Occurrence media | `occurrence.add-media`, `occurrence.swap-media` |
| Placement | `placement.move` |
| Inverse (restore machinery) | `timeline.inverse`, `timeline.restore` |

The R4 notes call the ordinary set "12 ops" (the 14 above minus the two inverse names). The Agent-side guarded auto-placement ops, selected-media and task-attempt fences, and the four itemref patterns are **not** in this file; they arrive only with the next regeneration (section 5).

---

## 4. Historical tuples (frozen; never relabelled)

| Tuple | Runtime commit | CONTRACT_VERSION | SCHEMA_DIGEST | Status |
|---|---|---|---|---|
| M1 recorded (03:55Z) | `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` | `0.2.1` | `sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d` | Historical. Its contract is 0.2.1, not 0.2.8. Verified in its `contract_metadata.py` |
| Public10 pair | `6be970633cc82ab412428151e6bf42f3e7fc3081` (`fix(runtime-client): export TrackSetArgs`) | `0.2.2` | `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` | **Frozen.** Agent's lock currently pins this commit. Verified in its `contract_metadata.py` |
| 0.2.3 compatibility floor | `4c145dc62192f0e942e3ee3922a11488aefe9b41` | `0.2.3` | `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` | **Frozen.** Live compatibility floor (`runtime-0.2.3.json`). Verified in its `contract_metadata.py` |

Branch-only versions `0.2.4` (D13 producer guard), `0.2.5` (itemref standalone) and `0.2.6` (popup verified-media candidate) never reached integration. Do not reuse their numbers for new content.

---

## 5. Not on this tuple (the rows that move the pin next)

### Next tuple (pending): retired-ops removal 142->133, D13, Agent schema

Pins will move once more after this tuple. Consumers should not treat `9f59dd4` as final.

| # | Change | State at 08:00Z | Effect on the next tuple |
|---|---|---|---|
| a | Remove 9 removable retired operations from OpenAPI and both generated clients (410 handlers stay) | Branch `tl/rt-m2-contract-retired-ops-removal` tip `1f3e64d` is an ancestor of integration. **No removal commit is merged.** Worker not finished | OpenAPI 142 -> 133 |
| a' | 17 WAITS retired operations stay until their consumers migrate | — | None in this regen |
| b | D13 producer guard and proposal cohort | `tl/rt-m2-d13-forward` tip `5a394fd` is **not** an ancestor of integration (this corrects the earlier draft, which said forward-merged). HELD | Regeneration needed; do not reapply 0.2.4 |
| c | Verified-read family consolidation | Merged as `b63153b` (wire unchanged) | None |
| d | Read-envelope to canonical image conversion | Agent-side, blocked on Agent | Pending Agent post |
| e | Agent canonical schema: guarded auto-placement ops, fences, four itemref patterns; `edit-command.json` byte-identical copy | Agent manager has not posted an SHA | Adds ops to section 3; `CONTRACT_VERSION` must move to a new free number, because `SCHEMA_DIGEST` changes (not 0.2.8, not 0.2.4–0.2.6) |

The regeneration is run from one worktree with `/home/user/work/venv-runtime/bin/python` (never reinstall the venv): `generators/generate.py`, `scripts/artifact_manifest.py`, then the same targeted files above plus `npm test`, and a full suite once through the central service.

---

## 6. Pin instructions

Pins are exact SHAs. Do not pin a branch or "HEAD at generation time".

**Agent** (`/home/user/work/agent`, Agent manager):
1. In `runtime.lock.json`, set `"source_commit"` to `9f59dd4577e063749056f8c76f73dd156feb54a7`. It is currently `6be970633cc82ab412428151e6bf42f3e7fc3081`.
2. Provide a git checkout whose `HEAD` is exactly that SHA (a detached worktree of the Runtime repo is fine). `vendor_lock.py update` refuses unless `HEAD` equals `source_commit`.
3. `python scripts/vendor_lock.py update runtime.lock.json --producer <that checkout>`
4. `python scripts/vendor_lock.py check runtime.lock.json --producer <that checkout>`

**App** (`/home/user/work/app`, App manager):
1. In `runtime.lock.json`, set `"source_commit"` to `9f59dd4577e063749056f8c76f73dd156feb54a7`. It is currently `182a7dd8446456162a452a25c8493256c5da29fe`.
2. `node scripts/vendor-lock.mjs update runtime.lock.json --producer <checkout at that SHA>`
3. `node scripts/vendor-lock.mjs check runtime.lock.json --producer <checkout at that SHA>`

App's lock covers the conformance fixtures listed in its `files` map. App's TypeScript client `src/integrations/runtime/generated.ts` changes only through its own pin move; App manager to confirm the vendoring path for that file. Runtime did not verify App's side in this worker.

Neither consumer pins a branch. Runtime itself makes no edits to either repo.

---

## 7. Open items register

| Item | Owner | Blocks |
|---|---|---|
| `npm test` for `packages/typescript` on this tuple | Runtime manager (named suite) | section 1.1 row |
| Retired-ops removal (a) merged | Runtime manager | next tuple |
| D13 cohort (b) merged with regeneration | Runtime manager | next tuple |
| Agent canonical SHA, `edit-command.json` sha256, superset-guard commit, op list | Agent manager | next tuple |
| New `CONTRACT_VERSION` number | Orchestrator | next tuple |
| Agent and App pin moves to `9f59dd4` | Agent and App managers | consumers |
| D-b, D-c, D-d | Orchestrator | scope |
