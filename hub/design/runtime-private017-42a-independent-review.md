# Runtime PRIVATE017 exact artifact review

Date: 2026-10-21 UTC

## Verdict

**APPROVE** for the exact committed private artifact counterpart:

- Runtime commit `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Direct parent/preservation base `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406`,
  tree `486fe045f66182b33520bea971d31add3f713ea9`.
- Current safety `b92d3e7a05eec65c142294ef4873edd059e9b31d` is an ancestor of the
  candidate; the candidate is not a current-safety rewrite.

This approves exact artifact identity and source/carrier compatibility only. It
does not approve a consumer pin, public release, adoption, merge, activation,
native execution, HTTP qualification, or any live caller change.

## Exact tuple

| item | verified identity |
| --- | --- |
| Runtime package | `0.2.17` |
| Agent source commit/tree | `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` / `f4a632e4f627499e0b15d8477db9aaab78ebb3d2` |
| Agent source | `astrid/core/timeline/schema/edit-command.schema.json` |
| Agent raw schema | `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16` |
| Agent canonical schema | `sha256:9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6` |
| Schema inventory | 65 definitions / 37 `EditCommand` clauses |
| Runtime health/schema digest | `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd` |
| Runtime raw bundle | `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f` |
| Artifact manifest | 76 entries; version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0` |
| Component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |

The carrier is the existing `CommandRecord.writes: AgentWrite` shape with the
optional `insertion_order: array<string>`. It is omitted for ordinary writes,
absent-key-compatible, and never null. Generated Python exposes
`NotRequired[list[str]]`; generated TypeScript exposes `insertion_order?:
Array<string>`.

## Preservation and artifact origin

- All 76 candidate artifact hashes match `contract/artifacts.json`; the manifest
  version recomputes exactly.
- 65 of 76 artifact bytes are exact da77 origin bytes. The only 11 differing
  entries are the command schema, release/version metadata, generated Python and
  TypeScript carrier/metadata outputs, and the generated Runtime bundle schema.
- The candidate has exactly 16 changed files over da77, all in the explicit
  allowlist; outside-allowlist changes: **0**.
- The four required unchanged da77 join blobs remain exact:
  `generators/command_schema_compatibility.py`,
  `tests/test_command_schema_compatibility.py`,
  `tests/test_timeline_commit_type_generator.py`, and
  `tests/test_timeline_owned_reference_integration.py`.
- `tests/test_timeline_current_union_contract.py` differs only by the two new
  private raw/canonical digests and one `AgentWrite.insertion_order` removal in
  the ordinary-6ba reconstruction helper. After normalizing those required
  changes, its body is exact da77; test definition count is unchanged (24), with
  no added/removed skip, xfail, or expected-failure marker. The focused run
  collected and passed all 76 cases, including the exact ordinary 6ba digest and
  all prior positive/negative validation assertions.
- Published014/95 remains immutable at Runtime
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, with 76 artifacts. All old016
  final-join refs remain at da77/tree `486fe…`; no historical artifact was
  mutated.
- No live caller changed. Acceptance, materialization, raw/reference,
  transcript, BASE-media, launcher, catalog, and Speech guard families remain
  inherited from the da77 join outside the allowlist.

## Carrier evidence

The source-shaped ordered `CommandRecord` validates through the reproduced
Runtime bundle. The legacy record with the optional key absent also validates;
`null`, arrays containing `null`, and arrays containing a non-string are refused.
The Python generated `AgentWrite` typing probe and a strict TypeScript
`AgentWrite`/`CommandRecord` assignment both pass. The original Agent inverse /
order semantic proof is source-unchanged and is reused from the author evidence:
serialization/reload, exact ordered namespace restoration, inverse, redo, and
absent-key compatibility.

## Commands and limits

Independent commands/results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python generators/generate.py --check
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
PASS: contract/artifacts.json is current

git diff --check da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406 42a7203f49bb89f299ec854cfbf2b1444e815a7c
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_current_union_contract.py
76 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py tests/test_command_schema_compatibility.py tests/test_timeline_owned_reference_integration.py
141 passed, 1 deselected

tsc --noEmit --strict --module NodeNext --target ES2022 /tmp/private017-agentwrite-typecheck.mts
PASS (temporary probe removed)
```

The generation worker's unchanged evidence is reused rather than repeated:
252 focused Runtime tests, 6 raw-capture regression tests, and 1 Agent ordered
semantic test passed. Broad 217/252 lanes, full suite, native, HTTP, browser,
renderer, and install lanes were not rerun, as required. This review therefore
does not claim those qualification boundaries.
