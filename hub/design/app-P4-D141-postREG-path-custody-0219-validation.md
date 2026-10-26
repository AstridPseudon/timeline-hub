# D141 P4 affected-path and custody validation

## Finite verdict

`PASS_UNRELATED_TO_ACTUAL_P4_BODY`: the five-source-file App delta from `867cb2737af1b46dc608c7cd37c349e920fe9422` to `5fe3e4debec5fb030f772ca41f16c86cc80e6150` is not a code or data dependency of the registered Agent HTTP three-leg P4 execution at `agent-p4-current-becfe-http-3legs-1026011042-10086`.

This is a source/import/caller verdict only. It does not re-execute P4, parse the recorded XML, or turn the recorded metadata into a new GO. The App manager must still check actual XML bytes/custody before any cumulative verdict.

## Exact App delta

The frozen App comparison contains exactly five changed source files:

- `src/integrations/runtime/dataProvider.ts`: paired basis/display load and head consistency guard.
- `src/shared/lib/placement/placementService.ts`: prepared one-shot document mutation and store delegation.
- `src/tools/video-editor/data/DataProvider.ts`: paired provider type.
- `src/tools/video-editor/lib/shot-group-pack-commands.ts`: `duplicateShotGroup` prepared-mutation caller; `promotePrimaryVariant` remains on the prior path.
- `src/tools/video-editor/lib/shot-group-pack-commands.test.ts`: provider mock update.

The exact Git blob IDs and source coordinates are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P4-D141-postREG-path-custody-0219/evidence/source-map.json` and the exact candidate/tuple manifest is in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P4-D141-postREG-path-custody-0219/evidence/source-manifest.json`.

## Actual P4 path

The registered launcher at Agent commit `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, blob `f1bde17ea107a8b669cb6924fbdbd2f3979da988`, uses App commit/tree only in the four-way manifest guard. Its preflight imports Agent, Runtime, schema, and Composition dependencies; its body runs the three Python selectors with only the pinned Agent and Runtime roots on `PYTHONPATH`.

The three selectors import Agent SDK/fixtures and use the real Runtime daemon/provider/generated-client HTTP path. Runtime `server.py` routes canonical timeline commit requests into `service.py`, which enters `timeline_commit_execution.py` for provider commit, verification, replay, and outcome handling. None of these files is in the five-file App delta, and no changed App file is imported or spawned by this graph.

The “absence of an App import” check is not the sole basis for the result: the caller/dataflow census also checked changed placement/provider/shot-group callers, launcher subprocess arguments, manifest fields, schema/provider metadata, and Runtime route dependencies. There is no App subprocess, asset, schema, client, or dataflow edge into this registered P4 body.

## Recorded evidence and boundary

The correction receipt and independent review record the old four-way tuple as 3/3 PASS and preserve the old 0114 custody FAIL. The queued `19479` item remains queued and unstarted. The recorded XML path is not present in this sandbox, so the recorded XML hash is cited as metadata only and is not claimed as locally parsed.

The App delta is still affected for current-head browser/editor paths that reach the new placement or shot-group seams. Those paths need their own App reproof. This finite result does not qualify them and introduces no semantic policy.

## Read-only validation commands

- `git -C /home/user/banodoco/reigh-app diff --stat 867cb2737af1b46dc608c7cd37c349e920fe9422 5fe3e4debec5fb030f772ca41f16c86cc80e6150` — PASS; five files, 79 insertions, 11 deletions.
- `git -C /home/user/banodoco/reigh-app diff --check 867cb2737af1b46dc608c7cd37c349e920fe9422 5fe3e4debec5fb030f772ca41f16c86cc80e6150` — PASS, exit 0.
- `git -C /home/user/banodoco/reigh-app diff --name-only 867cb2737af1b46dc608c7cd37c349e920fe9422 5fe3e4debec5fb030f772ca41f16c86cc80e6150` — PASS; output is exactly the five files listed above.
- `git -C /home/user/banodoco/reigh-app ls-tree 867cb2737af1b46dc608c7cd37c349e920fe9422` and the equivalent `ls-tree` at `5fe3e4debec5fb030f772ca41f16c86cc80e6150` — PASS; exact changed-file blob IDs recorded in `source-map.json`.
- `sha256sum` on the candidate row and recorded correction/review/source/registration JSON — PASS; hashes recorded in `source-manifest.json`.
- `test -e /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-operational-return-0055/evidence/body-evidence/p4-d141c.xml` — expected absent in this sandbox; no XML parse was claimed.

No tests, browser runs, localhost/live sockets, TypeScript checks, lint, or collector/registry/kit actions were run; they are outside this read-only finite analysis and the task explicitly marks tsc/lint not applicable.
