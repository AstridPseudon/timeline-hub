# Agent ordinary014 staged normal-pin final review

## Verdict: APPROVE (normal consumer candidate only)

Approved staged pin `e86f44d04e0a5f183d82d4d1ac307951dd32c44e` (tree
`5b4ec03d6d3081f9a3b96676f10ca051c4e9775e`) on current source
`ee896821b502ee4e51211b19d064fa44915f5777` (tree
`aa0b15850d4b777b77f54faec189cf7e4c60a7b6`). The exact normal Runtime
producer is `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
`4b7dd0fe44be973c344bab3de568eaf0bdd28476`, from detached clean checkout
`/home/user/work/wt/rt-pin-a0dca169`.

The candidate is not a Runtime integration pin, public release, activation, or
App/browser qualification.

## Pin and byte proof

- Runtime package is unpublished `0.2.14`; schema digest is
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Producer artifact version is
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Producer `contract/artifacts.json` is 75 entries; all 75 source bytes match
  their committed manifest hashes (0 mismatches).
- All 15 locked Agent consumer files match their producer bytes and manifest
  hashes. `scripts/vendor_lock.py check runtime.lock.json --producer
  /home/user/work/wt/rt-pin-a0dca169` passed.
- The only staged paths are `astrid_runtime_client/__init__.py`,
  `astrid_runtime_client/contract_metadata.py`,
  `astrid_runtime_client/generated.py`,
  `astrid_runtime_client/timeline_commit_types.py`, and `runtime.lock.json`.
  `runtime.lock.json` names the exact full producer SHA.
- The seven new public DTO exports identity-match the DTO module and are in
  `__all__`: `AssembledTargetArgs`, `ClipAddMediaArgs`, `ClipAnchorArgs`,
  `OccurrenceCreateArgs`, `TimelineInitArgs`, `TextBindingSetArgs`, and
  `WordAnchor`.

## Evidence and preservation

Focused reviewer lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_vendor_lock.py tests/stage1/test_vendored_workspace_client_parity_luna.py tests/sdk/test_timeline_current_union_schema.py
63 passed in 137.57s
```

The producer qualification report records the exact-provider central lane as
`143 passed, 10 deselected`, covering init, occurrence birth, parent media,
text binding, word anchor, S2 move/undo/retry, P1 authority, F1 identity, and
normal CLI/Python/native frontend/session paths. Renderer-off save fences,
request/key/receipt preservation, reload/restart, guarded undo, and exact retry
assertions remain in that lane. The staged pin changes no P1, F1, Scene, or
assembled-media source/test path; those current-source bytes are inherited
unchanged from `ee896821`.

## Sealed-text evidence discrepancy

The two reviewed reports disagree about the exact source/artifact:

- `agent-sealed-text-ref-contract-fix.md` and the Agent schema identify the
  exact key `occurrence:occurrence-1/text-binding:voiceover_script::` and say
  the old current Runtime integration rejected it.
- `runtime-native-text-source-review.md` reports that the exact `a0dca169`
  candidate rejected the same key before provider execution.
- Direct inspection of the exact producer shows the text-binding branch in
  `runtime_protocol/schemas/timeline-commit-bundle.json` (`TargetKey`), and in
  `contract/schemas/edit-command.json`. The latter is byte-identical to the
  Agent schema at `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  the Runtime bundle is `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`.
- With `PYTHONPATH=/home/user/work/wt/rt-pin-a0dca169`, the installed Runtime
  validator accepted a `text-binding.set` command carrying that exact key in
  both `expect` and `authorship`.

Therefore the reported rejection cannot be reproduced from the committed
`a0dca169` source/artifact pair and indicates stale or mismatched source/artifact
selection in that run. No broad schema relaxation is recommended. Runtime
should reconcile the failed-run import/artifact provenance before reusing that
failure as independent native-text evidence; the existing narrow branch is
already present in the exact candidate.

No public adoption, integration bump, release, merge, push, full suite, or
browser journey was performed.
