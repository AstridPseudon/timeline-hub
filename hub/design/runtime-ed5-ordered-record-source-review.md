# Runtime reciprocal review — Agent ed5 ordered-record carrier

Date: 2026-10-21 UTC

## Verdict

**APPROVE — Agent source/schema compatibility only.** Agent commit
`ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`, tree
`f4a632e4f627499e0b15d8477db9aaab78ebb3d2`, is the correct successor to
frozen Agent `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
`e2c08fbe9b21a3082db7bcf62d9677babfc15e98`, for the existing recorder,
state-setter and inverse semantics. This does not approve a Runtime pin,
version allocation, release, adoption, or native/HTTP qualification.

## Exact schema result

The candidate raw schema SHA-256 is
`6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`;
canonical SHA-256 is
`9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
It has 65 definitions and 37 `EditCommand` clauses. Against frozen10226,
the schema diff is exactly one optional property on `$defs.AgentWrite`:

```json
"insertion_order": {"type": "array", "items": {"type": "string"}}
```

The four existing required fields remain required and
`additionalProperties: false` remains closed. Removing that property
reconstructs frozen canonical `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`.
The Agent worker's independent six-test evidence also passed the ordinary
floor reconstruction and source behavior checks.

## Source carrier binding

The candidate's existing code is lossless and needs no new recorder path:

- `_project_data_commands.py:116-124` takes the Python `config.app` key order
  and supplies it only when pruning an empty namespace.
- `_recording.py:137-157` copies the optional iterable into the record only
  when non-`None`; ordinary absent-key writes omit the property.
- `_command_state.py:391,552-565` uses the recorded order to restore the
  namespace mapping around the restored key.
- `inverse.py:31,100-102,488,496-497` forwards the same field through the
  staged and normal inverse paths.

The independent source evidence records the exact source-created carrier,
JSON reload, inverse, and redo restoring
`["before", "com.example.compiler-canary", "after"]`; absent-key removal
remains compatible. Schema validation rejects `null`, arrays containing
`null`, and arrays containing non-strings. Trusted inverse probes reject a
missing target/order mismatch with `history_unavailable`. No command argument,
metadata alias, endpoint, second writer, or side channel is introduced.

## Runtime generator consequence

Current b92 still has the ordinary 55-definition/29-clause schema and its
four-field `AgentWrite`; it explicitly refuses the real source record at
`writes[1]` because the closed carrier does not know `insertion_order`.
There is no `RecordedWrite` symbol in b92 or da77: the generated Python
Runtime/client and TypeScript projections are all named `AgentWrite`, and
`CommandRecord.writes` points to that type.

The reviewed da77 generator path can emit the successor without hand edits:
`timeline_commit_types.render()` naturally maps the schema to
`NotRequired[list[str]]` in both Python modules and
`insertion_order?: Array<string>` in TypeScript; the resource renderer carries
the same schema into `timeline-commit-bundle.json`. A private overlay render
with the ed5 schema passed generation and `--check`; the generated Python
schema probe and `tsc` syntax check passed.

The exact prerequisite before the next private generation is to carry the
approved da77 five-blob join onto b92/current guards and update the next
private source pin from frozen10226 to ed5 (commit/tree/raw schema above).
The five preserved paths/blobs are:

1. `generators/command_schema_compatibility.py` —
   `62aca5e37a310aeaf6159bdfab43586cebb90599`;
2. `tests/test_command_schema_compatibility.py` —
   `dba93418e347483af226f4ca8a9cbf45603cf091`;
3. `tests/test_timeline_commit_type_generator.py` —
   `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e`;
4. `tests/test_timeline_current_union_contract.py` —
   `e6511aedc8740484f48df583a29029237d8b719e`;
5. `tests/test_timeline_owned_reference_integration.py` —
   `6af84532227f11ae315c5e8783c54dbec8702b13`.

The direct b92 candidate-generation probe fails only at the old
`TrackSetArgs.clear` const-to-enum compatibility check. The da77
`--agent-command-schema` path also correctly refuses ed5 while its immutable
pin still names10226. These are the required next-version pin/join steps, not
an Agent carrier defect. Preserve current published95/all76 and leave
da77/016 immutable HOLD.

After that agreement, the normal command is:

```text
python -B generators/generate.py --agent-command-schema <exact-ed5-agent-schema>
python -B scripts/artifact_manifest.py
python -B generators/generate.py --agent-command-schema <exact-ed5-agent-schema> --check
python -B scripts/artifact_manifest.py --check
```

This review did not run that command in the assigned Runtime worktree and did
not allocate a version or pin.

## Evidence boundary

Current b92 targeted Runtime checks: 5 passed. Private da77-overlay
generation, generator `--check`, generated carrier probe, and TypeScript
`tsc --noEmit --strict --target ES2022` all passed. No full, native, HTTP,
socket, browser, renderer, install, release, public pin, or remote merge was
run.
