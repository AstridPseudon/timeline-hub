# Runtime PRIVATE016 schema-test conversion review

## Verdict

**APPROVE**, for the exact two-file test conversion at Runtime commit
`09d0e40283925ec64cd986c9ad8699406afdd9d3`, tree
`4289291d158702a27ac5d89e94bc4ce2becf63b1`, relative to parent
`8610056a330563d4f80be06f19ad4b21076117ea`, tree
`0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`.

This is approval of the one-to-one schema-test conversion only. It does not
approve the generated candidate, the compatibility guard, source-join repair,
pin, publication, adoption, or native/consumer qualification. The typed guard
repair is separately reviewed and is not repeated here.

The current corrected source-join branch is `b59d22b607cbb12bb941cdcf0812b0446e5b77f1`
(tree `671532c57c04ff9b9a9c232f29753fc46d82f423`). It still has the old test
blobs. When that source is combined, this verdict applies only if the two
converted blobs are exactly:

| file | required blob |
| --- | --- |
| `tests/test_timeline_commit_type_generator.py` | `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e` |
| `tests/test_timeline_current_union_contract.py` | `e6511aedc8740484f48df583a29029237d8b719e` |

## Scope and identity

The diff from `8610056a` to `09d0e40` contains exactly these two modified
test files: `tests/test_timeline_commit_type_generator.py` and
`tests/test_timeline_current_union_contract.py`. No product, generator,
schema, generated artifact, manifest, version, pin, or fixture file changed.

The reviewed private schema identity is raw
`9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`, canonical
`322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`, with 65
definitions and 37 closed `EditCommand` clauses. The ordinary floor is raw
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, with 55
definitions and 29 clauses.

## Assertion mapping

### Exact schema and operation inventory

The old `test_exact_frozen_schema_and_operation_inventory_are_packaged` raw
6ba assertion is converted to the exact private raw and canonical digests,
65/37 counts, the private operation inventory, and exact schema equality with
the embedded bundle. The helper `_ordinary_schema_bytes` removes the ten
private definitions, three private union expansions, private fields and
private clauses, restores the ordinary TrackSet/ClipSet/ShotSet leaves, and
serializes the result. Its digest is asserted to be exactly the old ordinary
6ba digest; the reconstructed schema is also reasserted at 55 definitions and
29 clauses. This is an exact reconstruction check, not an alternate fixture
snapshot.

The ordinary operation cases and `NEW_OPERATIONS` remain in the expected
inventory; the eight private operations are added explicitly. Bundle embedding
remains an exact equality assertion.

### Generated Python TrackSet union

Both old module parameters remain. The shared outer `values` and `clear`
fields remain required, label remains a `str`, and the old label set and label
clear constructions remain exact. The private `muted: bool` member has direct
set (`False`) and clear constructions, and the generated `clear` annotations
are checked to agree between branches.

The generated private shape is correctly recorded: because the current schema
uses non-exclusive `anyOf` presence rules, generated Python has optional
`label` and `muted` members in both branches. The old label-only required-member
assertion is not falsely retained against that generated shape; authoritative
nonempty semantics are preserved by schema validation and the converted
negative tests below.

### Generated TypeScript fixture

The original fixture content is read and compiled against the current checked-in
generated TypeScript file through a private temporary source. No alternative
generated output or manual fixture snapshot is used. All old label positives
remain: ordinary label, empty string, Unicode, clear, and set+clear overlap.
All old malformed/closed negatives remain: missing shared fields, empty edit,
null/wrong label, malformed clear, null clear, extra value, and extra argument.

The old empty-edit negative is strengthened with a local `NonEmptyTrackSetArgs`
intersection because the generated TypeScript shape cannot express JSON Schema
`minProperties`/`minItems`; the runtime schema negative remains authoritative.
Private positives cover muted set, muted clear, and set+clear overlap. Private
negatives cover wrong muted type/null and unknown clear. The settled nonexclusive
`anyOf` means overlap is intentionally positive, and the conversion preserves
that behavior.

### Runtime schema neighbors

The converted union-contract test directly accepts old label set, label clear,
and label overlap, plus muted false set, muted clear, and muted overlap. It
directly refuses empty values/clear, string or null muted values, unknown value
keys, unknown clear keys, and null clear. Existing all-operation closed-key,
number/boolean, target, presence, and recorder assertions remain untouched.

No skip, xfail, or test exclusion was added. No old assertion was deleted or
weakened; the only replacement is the necessary exact private generated-shape
assertion described above.

## Evidence

Reused the conversion worker's direct compact run on the exact conversion:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-private016-neighbor-pytest3 [selected changed tests and neighbors]
21 passed in 6.9s
```

The recorded `git diff --check` passed. No full suite, socket, browser,
render, native, install, generation, pin, publication, adoption, or release
run was performed or is claimed. The separate compatibility/source candidate
hold remains outside this assertion-conversion verdict.

## Next steps

Combine the corrected source join with the two exact converted blobs listed
above, then let the separate compatibility/source reviews determine whether
the resulting candidate can proceed. Do not treat this test-conversion
approval as generated-candidate or release approval.
