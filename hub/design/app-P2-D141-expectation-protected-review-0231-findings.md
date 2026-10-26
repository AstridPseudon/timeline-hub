# D141d protected review findings

## FAIL — D141d-SCOPE-001 (blocking)

The only changed file is the permitted spec, but the changed code is not
gesture-local. The patch changes the shared `assertNativeHistoryEntry` helper
at lines 748–780 and therefore changes the shared `assertUndoHistoryEntry`
path as well. Those helpers are used by the element-edit and registerAsset
gestures as well as automatic child placement (calls at lines 1129, 1145,
1216, and 1308). The brief permits only the automatic-child-placement
gesture's `expected.records` expectation; every shared helper and every other
gesture must remain exact.

The candidate adds a conditional materialization branch that reads the target
history entry, accepts the no-materialization case unchanged, and otherwise
constructs two bindings. Regardless of whether its semantic shape is
plausible, this is a shared-helper change and fails the protected scope gate.

No author validation commands were run after this finding, per the instruction
to report FAIL immediately when scope fails. The candidate was not edited.
