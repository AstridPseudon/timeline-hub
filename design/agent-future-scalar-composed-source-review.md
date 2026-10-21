# Agent future scalar composed-source review

Date: 2026-10-21 UTC

## Verdict

**HOLD — concrete schema-join counterexamples.** The handler-side raw
presence, opaque-sibling, owner/source-guard, and inverse controls are sound
for the exercised cases, but the composed schema is not the exact union of
the approved sources. Do not approve this composition as-is.

Live callers changed: **NONE**. This is source-only review evidence; it does
not authorize generation, pin, native, activation, Runtime/App consumer work,
or a public release.

## Exact reviewed source

Candidate Agent commit/tree:

```text
6d8182d5cd9c164ad64db1a2ed62f052a3f61934
a4e5a21ad532671426d98ce894ea863c54c1fe4a
```

The four candidate files are the exact join at these blobs:

```text
astrid/core/timeline/schema/edit-command.schema.json
  a927857bb76801bd0c05ddd6dc0f7c16564db048
astrid/sdk/timeline/_clip_scalar_commands.py
  f65575859ec06b0cba066c46f768e55fec73047d
astrid/sdk/timeline/_command_state.py
  1a3d2c74077710c693dfde1f3799c2854b79b45b
tests/sdk/test_timeline_materialization_schema_union.py
  cff50eb7f5b16e03c014852214176c95a23156ed
```

The frozen10226 floor is commit `10226a7f08a739ba3e41f8e91de6971eed63aa9d`,
tree `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`, with canonical reconstructed
schema hash `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`.
The reviewed donor identities are:

| source | commit | tree |
| --- | --- | --- |
| caption39dd | `39dd47c67351cc6d1a3f0a0fb39c495b680e9b54` | `4b250c136557ced7c4ecff9e647acf8a63f85d69` |
| positionf2 | `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e` | `8c5674a5e329ab8dc5dcb4711251268a61b81847` |
| standalone effects097 | `097c68a9fe3641183372657b5f71cbdcb0a5b326` | `55da544815c3ef9cc33942b549e097d77294d3a0` |
| coupled fade5ad | `5ad1c517086d78448ac3d44dc75abfee59debd23` | `f85f760592c8187bc4116a9d164ca1341fe8b109` |

Frozen016, public014, and C13 were not changed.

## Counterexamples in the actual join

1. `ClipSetArgs.clear` at
   `astrid/core/timeline/schema/edit-command.schema.json:2974-2989`
   contains `hold`, `asset`, `transition`, `opacity`, the two effects leaves,
   `entrance`, and `exit`, but omits every approved positionf2 clear leaf:
   `x`, `y`, `width`, `height`, `cropTop`, `cropBottom`, `cropLeft`, and
   `cropRight`. The values setters are present at lines 2865-2895, so this is
   a set/clear asymmetry, not an intentional exclusion. A valid positionf2
   command `{values: {}, clear: ["x"]}` is accepted by the frozen positionf2
   schema but rejected by the candidate schema. Raw presence cannot be
   explicitly cleared through the composed public command.

2. The coupled fade5ad `values` schema contains two nested `allOf` guards:
   `entrance` requires `effects.fade_in`, and `exit` requires
   `effects.fade_out`. The candidate `values` object at
   `astrid/core/timeline/schema/edit-command.schema.json:2810-2972` has no
   nested `allOf`. Consequently the candidate schema accepts an unpaired
   `{values: {entrance: {type: "fade", duration: 1}}, clear: []}` and the
   corresponding unpaired `exit`; fade5ad rejects both. The handler later
   refuses these at `_effect_values` lines 217-224, but that does not preserve
   the approved closed schema/source semantics or early validation boundary.

The floor test added at
`tests/sdk/test_timeline_materialization_schema_union.py:266-271` still passes,
because stripping all future scalar keys also strips the missing position
clears and the omitted nested fade guards. It therefore proves the floor but
does not prove exact donor-union completeness.

## Source behavior controls

The candidate handler at
`astrid/sdk/timeline/_clip_scalar_commands.py:206-316` passed compact direct
controls for:

- text updates retaining an opaque text sibling and exact inverse;
- position set from present-null/absent state and exact inverse;
- standalone effects and coupled fade updates retaining opaque effects
  siblings and exact inverse;
- generated refresh retaining an opaque `app` sibling and exact inverse;
- refusing managedBy injection on an established generated row;
- occurrence targeting recording `scalar.owner`, `scalar.target`, source-shot
  identity reads, and the selected media registry reads.

These controls do not cure the two schema counterexamples above.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_materialization_schema_union.py::test_reviewed_scalar_successors_strip_to_exact_complete_10226_source \
  tests/sdk/test_timeline_materialization_schema_union.py::test_literal_three_union_reconstructs_each_reviewed_source_floor \
  tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden
3 passed in 2.12s
```

An inline `jsonschema.Draft202012Validator` comparison independently produced
`candidate reject / positionf2 accept` for `clear: ["x"]` and
`candidate accept / fade5ad reject` for each unpaired entrance and exit.
No full suite was requested or run. No source repair was made in this review.

Recommended next step: repair the composition join by carrying forward all
eight position/crop clear enum entries and the two fade5ad nested `values`
pairing guards, then rerun this bounded review against the new commit/tree.
