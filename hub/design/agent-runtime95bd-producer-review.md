# Agent reciprocal review — Runtime final95bd normal pin

Date: 2026-10-20 UTC

## Verdict: APPROVE

Approved for the authorized normal consumer-pin step only. This review does
not publish Runtime `0.2.14`, mutate the public `0.2.13` tuple, activate a
consumer, or adopt an integration branch.

## Exact source and artifact identity

- Runtime checkout `/home/user/work/wt/rt-pin-95bd3c5f` is clean at commit
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- `generators/generate.py --check` passed and
  `scripts/artifact_manifest.py --check` passed on the immutable checkout.
- Independent byte/hash probe: all 76 manifest entries exist and match
  `contract/artifacts.json`; the computed manifest version is
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  Required identities also match exactly: full manifest
  `a902387c...a532d`, component manifest `1ad76db...895e5`, raw edit schema
  `6ba7b51e...768f2d`, health `dcaec423...4510e`, services
  `10614b9c...4018`, and commit bundle `6d707cb8...66e3`.
- Runtime `contract/schemas/edit-command.json` and Agent
  `astrid/core/timeline/schema/edit-command.schema.json` are byte-identical:
  55 definitions and SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
  The qualified handoff records the ordinary raw contract as 29 operations.
- Private-overlay normal generation was exercised without changing this
  worktree:

  ```text
  python scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
  python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
  → update succeeded; check passed
  ```

  The four generated Python client files in the overlay compare byte-for-byte
  with the Runtime producer sources.

## Cross-area contract review

- Health is `workspace.v1`, with required status/protocol/schema digest,
  runtime epoch/session/instance identity, and service observations requiring
  name/state/last-exit/restart-count. Services are declaration schema v1 with
  required name/argv/restart. Their exact hashes are recorded above.
- The OpenAPI contract contains the required normal `/v1` operations
  `commitTimeline`, `listTimelineCommits`, and `getProjectMediaSelection`.
  Candidate generated-client methods and the Agent wrappers are present and
  use those `/v1` paths.
- Agent Main source compatibility probe passed with the candidate Runtime on
  `PYTHONPATH`: Agent `astrid.services.service_declaration` parses through
  Runtime `services.parse_services`; `runtime_protocol.platform.durable_replace`
  imports and remains callable with signature `(source, destination)`; Agent
  document/atomic-I/O imports succeed.
- Candidate safety surfaces remain separate from the ordinary schema/artifact
  identity: retention/compaction, verified publication and baseline refusal,
  occupied projection refusal, headless overwrite refusal, process identity,
  service supervision, and durable publication guards are retained. The exact
  C4 historical-reuse test passed against this Agent source:

  ```text
  pytest -q -m integration tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse
  → 1 passed in 1.96s
  ```

## Public tuple and evidence boundaries

- `git show 2c4ac180...:contract/artifacts.json` remains
  `129abdbb...5497`; its `contract/manifest.json` remains
  `75dc4d08...f6d14`. `/home/user/work/runtime` is clean.
- This Agent worktree still points at public `0.2.13`: source commit
  `2c4ac180...`, producer version `sha256:6f000bc6...b1af56`; no pin or
  generated product files were changed here.
- Existing exact candidate evidence was not duplicated: the qualified
  handoff records full31902 on this exact Runtime tree as **5,988 passed, 26
  skipped, 15 xfailed, 12 warnings, exit 0**, plus the six-node Agent-aware
  run5889 passing 6. This is consistent with the independent
  `runtime-mainmerged014-paired-candidate.md` review.

## Tests run and limitations

- Runtime targeted local lane (contract, raw payload/bundle, routes,
  validation, headless, projection/legacy occupancy, publication, platform,
  replay policy, services, lifecycle, baseline, closure): **565 passed, 2
  skipped, 10 deselected**. Six release-identity cases could not create test
  commits because the sandbox signing/MCP hook is unavailable; three live
  socket/process cases were blocked by the sandbox with `EPERM`. They are not
  product failures.
- Additional retention/compaction, empty-shell/headless, occupancy, and
  closure lane: **109 passed**; two candidate-promotion HTTP cases were
  blocked at socket creation by the sandbox.
- Agent current-source compatibility overlay lane (candidate generated client,
  workspace client, response conformance, services, installer ABI, and stage-1
  parity): **58 passed, 1 deselected**. One unrelated existing Remotion lock
  assertion failed because the local lock lacks
  `node_modules/@banodoco/timeline-schema`; it is outside this Runtime
  contract and was not changed.

No product source, generated source, Runtime pin, publication marker, or
integration branch was modified by this review.

## Next step

Proceed with the orchestrator’s coordinated normal Agent/App consumer cohort
using the exact `95bd3c5f` producer checkout and normal updater/checker. Keep
public `0.2.13` and Runtime integration unchanged until that cohort is
accepted.
