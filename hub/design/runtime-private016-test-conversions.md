# Runtime private016 exact-shape test conversion

## Scope and identity

This is a test-only conversion on Runtime `8610056a330563d4f80be06f19ad4b21076117ea`,
tree `0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`. The product, generator, schema,
manifest, generated, version, pin, and artifact files are unchanged. The private
Agent source is the reviewed 1022 line: raw schema SHA-256
`9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`, canonical
SHA-256 `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`,
65 definitions and 37 closed clauses. The ordinary floor remains raw
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, 55
definitions and 29 clauses.

## One-to-one assertion mapping

| Existing test ID | Old assertion | Private016 conversion and retained proof |
| --- | --- | --- |
| `tests/test_timeline_current_union_contract.py::test_exact_frozen_schema_and_operation_inventory_are_packaged` | Exact ordinary raw 6ba digest; 55 definitions; 29 `EditCommand` clauses; operation inventory; bundle embeds the schema. | Assert exact private raw `9cb959…`, canonical `322733…`, 65 definitions, 37 clauses, private operation inventory, and exact bundle embedding. A compact `_ordinary_schema_bytes` helper strips only the ten private definitions/operations, removes the private branches and fields, restores the old TrackSet/ClipSet/ShotSet leaves, and takes the first retained branch of each private version union. Its serialized bytes re-hash exactly to ordinary6ba, then reassert 55/29. |
| `tests/test_timeline_commit_type_generator.py::test_track_label_union_imports_and_retains_field_types[runtime_protocol.timeline_commit_types]` and `...[astrid_runtime_client.timeline_commit_types]` | Both outer union branches require `values` and `clear`; set branch requires `label`; clear branch permits optional `label`; label is `str`; label set and clear construct correctly. | Retain required outer `values`/`clear`, retain label `str`, and add private `muted: bool` plus literal clear support for `label` and `muted`. The current 65/37 `anyOf` has optional value members in both generated branches, so the assertion records that generated Python shape exactly while preserving label set/clear and adding muted set/clear constructions. Schema-level nonempty enforcement is tested separately below. |
| `tests/test_timeline_commit_type_generator.py::test_typescript_track_label_positive_and_negative_fixtures` | Compile old label set/clear positives and all old malformed/closed negatives. | Compile the same fixture content in a private temp source, add muted set/clear/overlap positives and wrong-type/unknown-clear negatives, and retain the old `noChange` negative through a local `NonEmptyTrackSetArgs` intersection because generated TypeScript cannot encode JSON Schema `minProperties`/`minItems`. The runtime schema test below remains the authoritative nonempty proof; the original fixture remains unmodified. |

## Added private016 schema neighbors

`test_track_set_preserves_old_label_and_adds_private_muted_shapes` proves label
set, label clear, label set+clear overlap, muted false set, muted clear, and a
muted set+clear overlap. Overlap is intentionally positive: the settled schema
uses non-exclusive `anyOf` presence rules, so it must not be converted into an
unsupported refusal.

`test_track_set_refuses_empty_wrong_typed_null_and_unknown_shapes` preserves
nonempty semantics and adds refusal neighbors for string/null muted values,
unknown value and clear keys, and null clear. Existing closed-argument and
unknown-operation cases remain untouched.

## Verification boundary

The exact changed tests plus direct generator/schema neighbors passed locally:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-private016-neighbor-pytest3 [selected changed tests and neighbors]
21 passed in 6.9s
```

No broad 287/136 lane, full suite, socket, browser, render, install, native,
generation, pin, or publication run was performed. The independent review's
const-to-enum boolean/number soundness HOLD is outside this task and remains
unmodified.
