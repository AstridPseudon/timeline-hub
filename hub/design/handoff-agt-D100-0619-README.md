# R1/G3 D100 clean join — F-D86

This is a source-only handback on the captured normal Agent base. It imports
only the four reviewed blobs named in the task and preserves all other tracked
bytes. Product status remains HELD. The 26 new controls are selected for
changed-source MAIN proof; this packet does not claim behavioral GREEN, cure
the original TEN, or require an unchanged-TEN repeat.

## Exact join

- `astrid/sdk/timeline/capture.py`: exact blob from `7f6e9db743`, review0610PASS.
- `astrid/sdk/timeline/_command_state.py`: exact product blob `09cbeed` from `d3b5cfef76`, review0513PASS; unchanged in the 0604/0614 reviews.
- `tests/sdk/test_capture_move_exact_time.py`: the actual tracked timing-test path from `git show d3b5cfef76` (the prompt shorthand omits `move_`); exact held blob.
- `tests/sdk/test_sequential_shared_item_provenance.py`: exact `fb9a47c2fc` blob, review0614PASS.

The source trace remains `capture_move → _capture → commands.execute → registered
clip.move/capture.move`. No policy, authority, route, schema, runtime, helper,
fixture, or generated-file change was introduced.

## New controls and boundaries

`handoff-agt-D100-0619-new-controls.txt` contains the exact 26 selectors: 4
new exact-time selectors and 22 new shared-item selectors. Membership was
checked from the reviewed test AST and cross-checked one-for-one against the
existing 7351 old-RED / 30890 candidate packet.

The original TEN remains excluded and untouched: 10 IDs, all 29 assertions,
with inverse/materialization and historical-text-binding findings kept
distinct. No original-TEN cure is claimed. The corrected private baseline
fixtures remain the genuine old-RED/new-GREEN comparison identity.

## Static verification

- In-memory AST parse/compile, exact blob hashes, AST predicates and call trace: PASS.
- Candidate Ruff: PASS.
- Parent Ruff for existing production files: PASS.
- Candidate mypy for both production files: PASS.
- Parent mypy: PASS in prior reviewed static evidence; private baseline temp tests were not rerun.
- `git diff --check`: PASS.
- No pytest, collection, imports, helper/fixture/function execution, probes,
  services, browsers, render, installs, or full suites were run.

See `handoff-agt-D100-0619-source-hashes.tsv` and the worker evidence for the
absolute source identities and exact command scope. A changed-source MAIN proof
is the next required step; behavioral status is otherwise unverified.

