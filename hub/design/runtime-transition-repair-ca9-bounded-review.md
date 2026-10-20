# Runtime transition repair `ca9` bounded review

## Disposition

**SOURCE ACK — bounded repair matches the current Main/Runtime contract.**

This ACK covers only the two NEW REPAIR findings from the earlier Runtime
`eb115` HOLD. It is not a sourcefreeze, generation, pin, activation, or public
carrier approval.

## Exact identities

- Cleanhandoff: `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`.
- Product repair: `5b3e41941b1263011f52f9f1291cbbc854563dbb`.
- Product repair tree: `705fc969ffcc2281d3b3e808e68e8a02467066bc`.
- Cleanhandoff product tree is unchanged; it only deletes the accidental
  `ORCH/design/agent-transition-eb115-peer-reconciliation.md` file.
- Schema Git blob: `95d7f4eb90a3afe8b3b6c554f31ac2cce4300d44`.
- Schema SHA-256: `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.

The three repaired Agent source files retain the handoff digests:

```text
_clip_scalar_commands.py       db72c5dbaed2eac46b9a5132dcbbc5533bcca904fdc725e9a5e821b9d6dbf8d6
_selected_param_authority.py   2747d3c64a5eebe9ee11c5c8fca5f23afaa13f6c9ef406a98eeaec572924bed8
commit.py                      d5faef1698d183017eb6a39710ca012e83d26469f88e1621f0214ab164c6ce88
```

## Repair reconciliation

### Incoming neighbor adjacency and duration fit

The repaired `_transition_set` now requires exactly one recorded
`transition.predecessor` on the destination clip's track. It applies the same
literal controls as current Main's `element-adapter.ts`:

- same-track predecessor end to destination start must satisfy
  `abs(end - start) < 0.001`;
- transition duration in frames must not exceed the shorter adjacent clip,
  with Main's `+0.0001` tolerance.

The implementation rejects gaps, cross-track predecessors, and oversized
transitions; it does not clamp or strip the transition. Runtime's canonical
incoming seam rule independently retains the positive incoming overlap and
shorter-neighbor fit in `runtime_protocol/visual_seam.py:363-391`. No playback
or compiler rule was changed, so existing readable playback behavior remains
outside this writer-side repair.

### Retained P1 authority for generic `clip.set`

For a selected project-pack transition, same-reference generic `clip.set` now
joins the existing retained selected-authority chain. The command must prove
the accepted first P1 source/snapshot and matching stable `(packId, id, kind)`
selection; a later P2 revision for the same stable reference is refused
atomically. Explicit `clip.set-element` remains the reselection operation and
was not converted into an implicit latest-pin path.

This matches the original selected-authority rules for forward records, inverse
consumption, rebase, ABA, and explicit reselection. No Runtime DTO, public pin,
generation path, new carrier, or opacity behavior was added.

## Preserved behavior checked during review

- Existing playback/compiler behavior is untouched, including gap and
  oversize data handling outside newly authored SET admission.
- `clear: ['transition']` remains transition-only and preserves unrelated
  `elementRef` / `element_ref`.
- `clear: ['transition', 'elementRef']` remains the explicit paired removal
  and keeps its stored transition/reference identity guard.
- The schema and the settled `clip.set` carrier remain unchanged.

## Executable evidence

To avoid changing the Agent worktree, commit `5b3e4194` was extracted into a
private temporary directory. Only the two new counterexample tests were run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/rt-transition-repair-probe.pgnpRN \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/rt-transition-repair-probe-tests-1 \
  /tmp/rt-transition-repair-probe.pgnpRN/tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  -k transition_set_enforces_main_adjacency_and_shortest_clip_fit
```

Result: **3 passed, 110 deselected**.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/rt-transition-repair-probe.pgnpRN \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  --basetemp=/tmp/rt-transition-repair-probe-tests-2 \
  /tmp/rt-transition-repair-probe.pgnpRN/tests/sdk/test_timeline_transition_schema.py \
  -k selected_transition_update_retains_first_pin_for_same_reference
```

Result: **1 passed, 2 deselected**. The temporary probe trees were removed
after the run.

The reported Agent lanes of 7 + 7 + 29 and 183 passing tests were not rerun;
neither was a full matrix, browser, socket, live Runtime, generation, pin, or
freeze operation.

## Next step

The Runtime side can record this bounded source ACK against the exact
`ca9f5f8e`/`705fc969`/`a70f…e1f4` identity. Any activation, publication, or
Runtime/App artifact qualification remains a separate orchestrator decision.
