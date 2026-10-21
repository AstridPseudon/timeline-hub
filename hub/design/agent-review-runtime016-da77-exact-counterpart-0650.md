# Agent reciprocal review — Runtime PRIVATE016 exact counterpart

## Verdict

**HOLD — concrete cross-area contract mismatch.** The exact Runtime tuple and
all five final-join blobs are internally consistent, but it does not carry the
existing Agent `AgentWrite.insertion_order` field required by the frozen Agent
source's ordered project-data inverse path. Do not create the normal private
Agent pin from this tuple until the carrier is resolved and the exact Runtime
counterpart is re-reviewed.

This is not a public release, adoption, activation, native, or full-suite
decision. No source or shared integration worktree was modified.

## Exact tuple reviewed

- Runtime: `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406`, tree
  `486fe045f66182b33520bea971d31add3f713ea9`.
- Runtime base: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- Frozen Agent: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`.
- Agent schema raw: `sha256:9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`;
  canonical: `sha256:322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`;
  65 definitions / 37 closed clauses.
- Runtime version: `0.2.16`.
- Runtime health/schema: `sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd`.
- Raw bundle: `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9`.
- Artifact manifest: `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5`, 76 artifacts.

## Checks that passed

The exact five final-join blobs matched the handoff:

| path | blob |
| --- | --- |
| `generators/command_schema_compatibility.py` | `62aca5e37a310aeaf6159bdfab43586cebb90599` |
| `tests/test_command_schema_compatibility.py` | `dba93418e347483af226f4ca8a9cbf45603cf091` |
| `tests/test_timeline_commit_type_generator.py` | `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e` |
| `tests/test_timeline_current_union_contract.py` | `e6511aedc8740484f48df583a29029237d8b719e` |
| `tests/test_timeline_owned_reference_integration.py` | `6af84532227f11ae315c5e8783c54dbec8702b13` |

The final tree differs from `8610056a330563d4f80be06f19ad4b21076117ea` in
exactly those five paths. The raw schema matches the frozen Agent schema and
has 65/37; the version, health digest, raw bundle, manifest version, and 76
artifact count match the handoff.

Commands:

- Six bounded Runtime tests (typed bool/number/null const-enum behavior,
  conflicting const, Python canonical-Args exports, malformed/unpinned source
  refusal, exact schema inventory, public union imports): **6 passed**.
- `generators/generate.py --check`: **passed**.
- `generators/generate.py --check --agent-command-schema` using the exact
  Agent 10226 schema extracted read-only: **passed**.
- `scripts/artifact_manifest.py --check`: **current**.
- Runtime commit `git diff --check`: **passed**.

The bounded tests used the read-only `/home/user/work/venv-agent` because the
documented `/home/user/work/venv-runtime` was absent. No broad 217/old44/186,
native, socket, browser, or full suite was run.

## Blocking mismatch

At frozen Agent 10226:

- `astrid/sdk/timeline/_recording.py` emits `write["insertion_order"]` when
  a container is cleared with an ordering guard.
- `astrid/sdk/timeline/inverse.py` reads `write.get('insertion_order')` when
  restoring the ordered container.

The exact frozen Agent schema's `$defs.AgentWrite` has only `ref`, `path`,
`before`, and `after`; it has `additionalProperties: false`. The exact Runtime
candidate reproduces that four-field shape in all checked representations:

- `contract/schemas/edit-command.json` — no `insertion_order`;
- `runtime_protocol/schemas/timeline-commit-bundle.json` — no
  `insertion_order`;
- `runtime_protocol/timeline_commit_types.py` — no `insertion_order`;
- `packages/python/astrid_runtime_client/timeline_commit_types.py` — no
  `insertion_order`;
- `packages/typescript/src/timeline-commit-types.ts` — no `insertion_order`.

Thus the Agent producer/inverse carrier and the Runtime generated
AgentWrite/bundle carrier are not the same contract. A future ordered
`project-data.write` namespace-prune record cannot be represented faithfully
through this generated Runtime boundary: accepting the Agent record requires
the extra field, while dropping it loses the order needed by inverse/reload.

## Recommended next step

Resolve the settled carrier mismatch in the owning Agent/schema/Runtime
generation work, then produce a new exact Runtime artifact tuple and repeat
only this bounded reciprocal review. Keep public/ordinary safety controls and
all five reviewed final-join blobs unchanged; do not hand-edit generated types
or authorize the normal private pin from `da77e2dd`.
