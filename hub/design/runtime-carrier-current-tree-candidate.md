# Runtime RT08 current-tree candidate

Status: private, reviewable candidate only. No public pin, freeze, release,
merge, activation, or native-pair claim.

## Exact source

- Composed base: commit `1cac679992a24b5a28080e15cc76a37e3d060265`, tree
  `1c6059ce9068b6ae6432ba465f95282502f72fa0`, on current Runtime `7f6dd892`.
- Final source snapshot including this resume's audit-test change: central
  snapshot tree `2d9d740ef22eea3b9ec4899bb8e400251bd6d444`.
- Harness commit SHA is intentionally not asserted here; the harness commits
  the worktree after this worker exits.
- Resume delta: only `tests/test_door_transport.py`, forwarded from current
  `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`; its working-tree SHA-256 is
  `704ec6ae842e4dcb5c8bf577df2c54ff6678864ceb89045ce7b4c3e6db7d3f48` and
  it is byte-identical to that current-base file.

The 17-path allowlist is:

```text
contract/artifacts.json
contract/schemas/edit-command.json
generators/command_schema_compatibility.py
packages/python/astrid_runtime_client/contract_metadata.py
packages/python/astrid_runtime_client/generated.py
packages/typescript/src/contract-metadata.ts
runtime_protocol/contract_metadata.py
runtime_protocol/schemas/timeline-commit-bundle.json
runtime_protocol/timeline_commit_port.py
runtime_protocol/timeline_commit_store.py
runtime_protocol/timeline_materialization.py
tests/test_command_schema_compatibility.py
tests/test_door_transport.py
tests/test_timeline_materialization_authority_review.py
tests/test_timeline_materialization_continuation.py
tests/test_timeline_materialization_join.py
tests/test_timeline_projection_ownership.py
```

The allowlist contains the reviewed carrier sources (`timeline_commit_port.py`,
`timeline_commit_store.py`, `timeline_materialization.py`), four carrier
test files, seven private generated outputs, the two compatibility-proof
helper/test files, and the current door-audit test. A SHA-256 comparison of
all 414 tracked paths outside this allowlist against `16acbb6` reported zero
mismatches. No product-repository build output or untracked file remains.

## Source and artifact facts

- Exact Agent source is committed `3730d0bd51686a1692450359482205df64dcc839`,
  tree `3892a10bcffa9bf520b4c79591637cf3259d6724`, schema SHA-256
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
  The approved private source inventory is 48 definitions, 22 operations,
  and the final 13-operation v2 subset. Ordinary `310` / `55` / `29` source
  was not imported.
- Public floor fixture `tests/fixtures/published-command-schemas/agent-26ef2bbb.json`
  remains unchanged at SHA-256
  `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.
- Private generated schema/resource/client hashes are unchanged from the
  reviewed composition: schema `f80215f2…`, bundle
  `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`, and
  private artifact manifest `9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62`.
- Carrier source hashes: port
  `28968f683c064af54da4b767618880781a6ec66e80586d462b8b7e2b1f96ee86`, store
  `11252cf2cb3dc5c8fc83cb447d238cd3f7b64a4051ecd1b6086444555fa278a2`, and
  materialization
  `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb`.

## Evidence

Environment: `/home/user/work/venv-runtime/bin/python`, Runtime worktree
source via `PYTHONPATH=$PWD`, `PYTHONDONTWRITEBYTECODE=1`, private pytest
basetemps under `/tmp`.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-carrier-compose-finish-focused tests/test_timeline_materialization_authority_review.py tests/test_timeline_materialization_continuation.py tests/test_timeline_materialization_join.py tests/test_timeline_projection_ownership.py`
  — **195 passed, 19 deselected**.
- Explicit public-floor control:
  `... pytest ... tests/test_timeline_projection_ownership.py -k 'frozen_artifact or current_typed_item_creation_claim_is_accepted_and_reserved'`
  — **2 passed, 52 deselected**. The public negative and private/current
  positive remain strict; no blanket xfail was added.
- Central socket-capable targeted lane on exact snapshot tree
  `2d9d740e…`:
  `tests/test_door_transport.py` plus the nine current commit/safety/repair/
  shell/fresh-scope/CLI neighbor files — **209 passed, 11 deselected**.
- The predecessor exact-tree central neighbor lane was **193 passed, 11
  deselected**; the predecessor private-pair focused lane was **210 passed,
  3 deselected, 1 strict xfailed**. Those are recorded as predecessor
  evidence, not added to the post-fix count.
- Existing exact-tree compatibility/generator lane was already green before
  this audit-only change: **169 passed**. The normal generation checks were
  not rerun as a broad lane.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py`
  — passed; `generators/generate.py --check` — passed;
  `scripts/artifact_manifest.py --check` — passed; `git diff --check` — passed.

No full, broad, matrix, browser, live-socket, or native Agent/Runtime pair
was run. Earlier Agent live evidence was not native-carrier qualification and
is not claimed here. The exact `3730` native pair remains HELD pending the
Agent peer review. After the harness supplies the real commit SHA, the Runtime
manager should send the Agent PEER REQUEST with that SHA/tree and this report;
no pre-commit SHA or fake peer request is asserted by this worker.

