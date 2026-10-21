# Runtime PRIVATE017 exact ordered-counterpart review

Decision: **APPROVE** the exact private Runtime candidate `42a7203f49bb89f299ec854cfbf2b1444e815a7c` / tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` for reciprocal artifact review only. This is not approval for a Runtime final artifact release, consumer pin, activation, adoption, public release, or native/HTTP qualification.

## Exact identities

- Runtime candidate: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`, parent `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406` / tree `486fe045f66182b33520bea971d31add3f713ea9`.
- Agent source: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`, tree `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`, path `astrid/core/timeline/schema/edit-command.schema.json`.
- Agent source raw SHA-256: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Agent source canonical SHA-256: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
- Source shape: 65 definitions / 37 `EditCommand` clauses.
- Runtime package version: `0.2.17`.
- Runtime schema/health digest: `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
- Raw bundle: `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f`.
- Artifact manifest: 76 entries; file SHA-256 `0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`; version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.

## Delta review

The only semantic carrier change is the existing optional `AgentWrite.insertion_order` property: `array` with `string` items, not required, and still under a closed object. The same shape is present in the checked-in bundle and generated carriers. The source-created ordered namespace-prune record validates as `CommandRecord`; an ordinary `AgentWrite` with the key omitted validates; `null`, `['before', None]`, and `[1]` are refused.

Generated forms are normal: Python has `NotRequired[list[str]]`, and TypeScript has `insertion_order?: Array<string>`. There are no hand-written casts, type ignores, endpoint/store/DTO changes, or live Runtime callers. The candidate diff has no Runtime implementation path outside generated metadata/types and schemas. The public95 lineage remains unchanged: public `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` is an ancestor of `da77`; this candidate performs no public release or activation.

The five required da77 join/protection blobs match the accepted current source exactly:

| path | blob |
| --- | --- |
| `generators/command_schema_compatibility.py` | `62aca5e37a310aeaf6159bdfab43586cebb90599` |
| `tests/test_command_schema_compatibility.py` | `dba93418e347483af226f4ca8a9cbf45603cf091` |
| `tests/test_timeline_commit_type_generator.py` | `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e` |
| `tests/test_timeline_current_union_contract.py` | `1b49b0d55344c74d269e9362c4b6caada617fdf4` |
| `tests/test_timeline_owned_reference_integration.py` | `6af84532227f11ae315c5e8783c54dbec8702b13` |

The affected assertion conversion is one-to-one: `_ordinary_schema_bytes` removes only the new `insertion_order` property before rebuilding the frozen ordinary schema. The private 65/37 positive identity and original old-floor/ordinary-6ba negative compatibility assertions remain in place.

## Evidence

All commands used a private `git archive` extraction of the committed candidate; no Runtime worktree or shared dependency was modified.

```text
git diff --check da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406 42a7203f49bb89f299ec854cfbf2b1444e815a7c
=> passed

PYTHONPATH=<candidate> python3 generators/generate.py --check
=> passed

PYTHONPATH=<candidate> python3 scripts/artifact_manifest.py --check
=> contract/artifacts.json is current

/home/user/work/venv-agent/bin/python -m pytest -q \
  tests/test_timeline_current_union_contract.py \
  tests/test_timeline_commit_type_generator.py \
  tests/test_command_schema_compatibility.py \
  tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current \
  tests/test_client_release.py::test_language_packages_share_the_contract_release
=> 219 passed in 68.22s

tsc --noEmit --project packages/typescript/tsconfig.json
=> passed

Direct existing validator probe:
  source-created CommandRecord => accepted
  absent insertion_order => accepted
  null / mixed / non-string insertion_order => refused
```

No full, broad/unchanged Runtime, HTTP, browser, socket, native, renderer, private pin/body, generation, activation, adoption, or public release lane was run.
