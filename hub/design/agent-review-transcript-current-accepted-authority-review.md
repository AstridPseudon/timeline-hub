# Transcript accepted-authority review

Date: 2026-10-21  
Reviewed Agent tree: `53c2c6f95` (`tl/agt-m2-gate1-transcript-accepted-reload-proof`)  
Reviewed Runtime: `3dcae1836a609363135d07ee435ce9beea975504`  

## Verdict

**APPROVE SOURCE, with a hard distinction between the bounded direct-service
witness and native qualification.** The Agent source is safe to compose for the
settled fail-closed transcript contract. The accepted-history test must not be
cited as normal HTTP/native App qualification or as proof of the normal trusted
bootstrap-genesis boundary.

## What was verified

- The exact newly authored `transcript.associate` command is accepted by all
  three relevant validators, without schema/provider replacement:
  Agent `validate_command`, Runtime3dca public `CommitRequest` validation, and
  frozen Runtime3dca `EditCommand` validation. The current Agent schema digest
  is `21e65ec27c247a5868172913b6b5f89b1024e894437d3c8ce0d2368a8d5534cb`;
  frozen Runtime's 6ba digest is
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
  Runtime's old schema does not enumerate this operation, but its closed
  command envelope permits the operation and the normal Agent provider gives
  it meaning. The official Runtime provider factory also loads successfully as
  `RuntimeCommitService astrid-v1`.
- `astrid/sdk/timeline/native_transcript_association.py:274-391` reads and
  writes the actual App/Main carrier at `parent.config.bundle`, using the
  persisted wire names `transcriptReferences` and `itemsBySchemaRef`. The
  legacy parent-level carrier is rejected by `_source_paths`; no second
  authority is introduced.
- Replacement records the new and prior exact `DocumentPin` dependencies in
  the expected order (`:467-469`). The accepted witness checks both pins in the
  dependency manifest and history record (`test_gate1_transcript_accepted_reload.py:167-186`),
  then exercises guarded inverse, restart, and redo (`:188-205`). Source-item
  order and unrelated opaque fields are preserved by the retained/projected
  split and copy-on-change reconciliation.
- The b39 reconciliation covers the real assetless caption shape: ownership is
  proven by the selected asset's media occurrence, then the App fingerprint is
  applied to the old/new source identity. Reviews require exact schema,
  source-item identity, and unique ownership. Shared ownership and destination
  collisions fail atomically in the Agent operation; positive text/style/timing,
  review-state, and opaque-field preservation are covered by the targeted
  Agent fixture.
- App source and claimed App tests were inspected at
  `reigh-app/src/tools/video-editor/data/typed/reconcileTranscriptReferences.ts:61-146`
  and `importTranscriptIdentity.test.tsx:210-322`. The positive assetless and
  ambiguous-ownership cases align. The App helper leaves a pre-existing
  collision unresolved (`:114`, `:139`), while the settled Agent b39 contract
  refuses it atomically (`native_transcript_association.py:349-350,379`). This
  is a deliberate fail-closed policy difference, not an overwrite or data-loss
  path; it should remain an explicit composition decision if byte-for-byte App
  collision behavior is later required.

## Evidence boundary / no overclaim

`tests/editing_conformance/test_gate1_transcript_accepted_reload.py:56-208`
is honest about being bounded, but it is not native qualification:

- it constructs a parent fixture and publishes it through direct
  `RuntimeService.publish_parent_composition` (`:80-108`) rather than starting
  from the normal daemon-loaded provider and trusted bootstrap fixture;
- it registers the official provider manually (`:108`, `:157`, `:190`, `:202`)
  and calls `RuntimeService.commit_timeline` directly (`:132-135`), not the
  authenticated `/v1/.../commit` route;
- its accepted-state inspection uses the private
  `service._timeline_commits()[0].revision_closure` reader (`:117-120`). It is
  useful evidence that accepted history, pins, restart, inverse, and redo are
  internally retained, but it is not a public read-authority proof.

Therefore the exact command is proven admissible through the public/frozen
schemas and the real provider, and the direct service witness proves the
accepted-history data-safety behavior. A normal daemon/HTTP/native App cohort
with the real serialized caption/review bundle and public reload/read remains
unverified. No handcrafted accepted row or validator monkeypatch was used in
the reviewed test; the parent seed and private closure reader are the explicit
limits above.

## Commands run

All were targeted; no full or live/browser suite was requested.

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3dcae183 PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_film_transcript_association.py tests/editing_conformance/test_gate1_transcript_accepted_reload.py
=> 11 passed in 2.21s

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3dcae183 PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_film_transcript_association_spike.py tests/sdk/test_timeline_current_union_schema.py
=> 42 passed in 148.28s

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3dcae183 PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 /home/user/work/venv-agent/bin/python -P -c 'from tests.editing_conformance.test_recipe_film_transcript_association import _bundle; from astrid.sdk.timeline.native_transcript_association import capture_transcript_association; from astrid.sdk.timeline.commands import validate_command; from runtime_protocol.timeline_commit_port import validate_request; from runtime_protocol.timeline_commit_validation import validate_commit_value; b,p=_bundle(); c=capture_transcript_association(b,"asset-a",document=p); body={"api_version":1,"project_id":"p","timeline_id":"t","base_revision_id":"r","base_publication_id":"u","commands":[c]}; validate_command(c); validate_request(body); validate_commit_value(c,"EditCommand"); print("agent_provider_validate=pass runtime_public_CommitRequest_validate=pass runtime_frozen_EditCommand_validate=pass")'
=> agent_provider_validate=pass runtime_public_CommitRequest_validate=pass runtime_frozen_EditCommand_validate=pass

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3dcae183 PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 /home/user/work/venv-agent/bin/python -P -c 'from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider; p=load_timeline_commit_provider("astrid"); print(type(p).__name__, p.provider_id)'
=> RuntimeCommitService astrid-v1

git diff --check
=> passed; worktree remains clean
```

App Vitest was not run: `/home/user/work/app/node_modules/.bin/vitest` is not
available, and shared dependencies were not modified. No product, schema, pin,
generation, freeze, or activation files were changed.

## Recommended next step

Keep the source approval and label the current Agent test as a direct-service
accepted-history witness only. Before claiming native qualification, add the
smallest normal-daemon `/v1` test using the trusted bootstrap fixture, real App
serialized `parent.config.bundle` caption/review leaves, authenticated public
reload, and the same two-pin restart/inverse/redo assertions. Preserve the
existing App positive and ambiguity behavior; resolve the noted collision-policy
difference explicitly rather than silently changing either side.
