# Runtime PRIVATE016 independent source/artifact/release-guard review

## Verdict

**HOLD** for exact Runtime commit `8610056a330563d4f80be06f19ad4b21076117ea`,
tree `0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`.

The joined b92 source ports and the normally generated artifact tuple are
internally consistent, but the new schema compatibility release guard is not
sound. It accepts a real narrowing when an old boolean singleton is replaced
by a numeric enum member because Python membership conflates `False == 0` and
`True == 1`; JSON Schema does not. This blocks approval even though the actual
PRIVATE016 TrackSet conversion uses strings.

## Exact identities checked

- Runtime base: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- Candidate: `8610056a330563d4f80be06f19ad4b21076117ea`, tree
  `0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`.
- Agent source: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`.
- Agent schema: raw `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`,
  canonical `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`,
  65 definitions / 37 closed clauses.
- Candidate version: `0.2.16`.
- Health/schema digest: `sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd`.
- Raw bundle: `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9`.
- Artifact manifest: `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5`,
  76 artifacts.
- Live production callers: **NONE**. The only callers found for the new
  materialization/raw/projection helpers are their focused tests.

## Source and artifact review

The candidate contains only the reported RT08 materialization, f53 raw-media
custody, 449 reference-projection, generator-support, generated-artifact and
focused-test paths. The changed-path set is exactly the candidate report's
allowlist; all other b92 paths are byte-identical.

The joined source retains the current guards and authority boundaries:

- materialization is a read-only project/timeline/content/shot/internal/item
  closure join with source and owner bindings, provenance, inverse handling,
  and no created IDs;
- raw capture is command-declared, managed-project-owned, single-CAS,
  regular-file/size/full-SHA/stable-descriptor checked, declaration- and
  acceptance-revalidated, and ledger-first on retry;
- reference projection uses only the namespaced parent carrier, source role,
  equal media/content digest and exactly one manifest member, with global
  occupancy, prior-carrier/live-row ownership, and transactionally coupled
  closure/publication/head/version updates;
- current transcript/rational/Speech, selected/base-only, catalog/C4,
  headless/global-item, occupancy and exact-ledger controls remain present.

The candidate's generated schema is byte-identical to the frozen Agent raw
schema; the embedded bundle schema is exact; all 76 artifact digests match the
manifest; package roots expose the old and new `*Args` without `*Variant`
Args; and no generated/source-authority drift was found. The original
owned-raw native behavior remains unqualified until a matched Agent pin and
normal pair are authorized.

## Blocking finding: unsound const-to-enum compatibility

`generators/command_schema_compatibility.py:100` and `:106` use Python `in`:

```python
a in new["enum"]
old["const"] in b
```

That accepts both of these invalid release-guard conversions:

```text
old: {"type": "boolean", "const": false}  -> new: {"enum": [0]}
old: {"type": "boolean", "const": true}   -> new: {"enum": [1]}
```

The executed probe showed, for each case:

```text
old_accepts=True, new_accepts=False, compatibility_checker_accepts=True
```

The same checker also accepted `false const -> enum [0, 1]` and `true const
-> enum [1, 2]`. Its existing null-vs-absence and dropped-singleton probes
rejected as expected, and a genuine string singleton widening
`"label" -> ["label", "muted"]` passed. The defect is specifically the
JSON boolean/number distinction being lost by Python equality.

Minimal repair: replace both membership checks with one JSON-Schema-aware
singleton-membership helper that recursively distinguishes booleans from
numbers (while preserving the intended singleton widening), and add the two
boolean-to-number negative cases to the compatibility tests. Do not weaken the
existing strict negatives and do not blanket-remove the const rule.

## Excluded old assertions

These were exclusions, not passes, and must not become permanent skips or
xfails:

1. `tests/test_timeline_commit_type_generator.py::test_track_label_union_imports_and_retains_field_types` (two module parameters),
   excluded by `-k 'not track_label_union'`; it asserts the old label-only
   generated TrackSet shape.
2. `tests/test_timeline_commit_type_generator.py::test_typescript_track_label_positive_and_negative_fixtures`, excluded by
   `-k 'not typescript_track_label'`; it asserts the old label-only TypeScript
   fixture shape.
3. `tests/test_timeline_current_union_contract.py::test_exact_frozen_schema_and_operation_inventory_are_packaged`, excluded by
   `-k 'not exact_frozen_schema_and_operation_inventory_are_packaged'`; it
   asserts the ordinary 6ba / 55-definition / 29-clause schema and therefore
   cannot qualify a private 65/37 candidate.

The old label language itself remains covered; no assertion was edited or
weakened. The candidate's recorded focused lanes were `287 passed, 4
deselected` and `136 passed, 3 deselected`; the central recorded socket lane
was `76 passed in 17.48s`. Those are reused evidence, not a new full/native
qualification.

## Commands run

- Exact Agent schema extracted with `git show
  10226a7f08a739ba3e41f8e91de6971eed63aa9d:astrid/core/timeline/schema/edit-command.schema.json`
  into a private temporary directory; `generators/generate.py --check
  --agent-command-schema <that file>`: **exit 0**.
- Independent 76-artifact SHA-256 recomputation: **0 mismatches**, manifest
  version matched.
- Narrow JSON Schema/checker planted-negative probe for `false -> [0]` and
  `true -> [1]`: **checker incorrectly accepted both**; this is the HOLD.
- `git diff --check b92d3e7a05eec65c142294ef4873edd059e9b31d..HEAD`: **passed**.

No product/test fix, install, full suite, socket/browser/render/native run,
pin, release, adoption, activation, merge or push was performed.
