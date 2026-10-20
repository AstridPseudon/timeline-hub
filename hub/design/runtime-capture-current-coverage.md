# Current capture coverage

Status: Agent verifier deletion remains HELD. Executable missing Runtime checks
are in rt-m3-current-capture-pair/tests/test_capture_candidate_actual.py.
No Runtime or Agent product edit has been made.

## Manager action requested

Please provide a central paired-source suite with the reviewed current Agent
source carrying BOTH the verified-source host and the complete saved filmstrip
expansion. Current Agent integration c456b3281497653cecf44f61acd6fa30565d83c8
has the optional projector and canonical-image conversion, but:

- astrid/core/rendering/verified_source.py is absent; GenericPackHost returns a
  plain dict without timeline_source.
- timeline_filmstrip.py::_open_current_input_closure reconstructs a reduced
  expansion and omits graph and outputs. It therefore does not equal the full
  startup-provider projection, even though managed_timeline.py already converts
  the GET envelopes onto canonical images.

Reviewed historical source tl/agt-m3-capture-projection-exact =
d977b59a6a2fc403c57ee76764dd3bd81523045c contains both missing pieces and the
approved canonical-image conversion. Its project_capture AST is IDENTICAL to
current integration (SHA256 ee459dc165f24980786240d35073a130673654f1f078e9cdd4a40908a0b48182).
The manager must choose the reviewed current composition; this worker has not
modified Agent or substituted the historical source for current qualification.

The proposed deletion is tl/agt-m2-capture-single-verifier =
c65619ed47517d3db9f47398bbf04c47f6dcf4ec.
Its project_capture AST differs (b7ce3e5aeb295a00da0425f2c79d5a2b8cbdb9ae7ce03484df1b66e4f443e61a).
Candidate-forward handoff: tl/agt-m3-capture-candidate-forward =
0add597d9ce8e4b5f6061b5b86ee92d761d4c7d7. Our Runtime tests forward the full
preview directly as ordinary task input; they do not qualify SDK invocation.

## Runtime verifier findings

Runtime _candidate_document checks preview kind, both digests, scope, base
identity, capture binding, retained document inputs and publication closure.
It does not compare the candidate's saved basis to the real saved closure or
prove publication derivation. Current Agent project_capture still does both.
There is no claimed present safety gap: the missing checks prevent deleting
the Agent checks, exactly as the orchestrator instructed at 09:26.

The new parameterized test calls the EXISTING Runtime verifier with a real
Runtime revision closure, bypassing only semantic projection so Agent's surviving
checks cannot conceal a missing Runtime check. It creates no alternative
verifier, projector, DTO, receipt or authority marker. All mutations preserve the
test's original expected refusal. Publication-derivation damage recomputes the
candidate digest and capture binding while retaining a different valid
publication, so it does not merely exercise a stale self-hash.

Final source tuple, complete mutation mapping and final test results are being
filled after the queued central runs:

- rt-m3-current-capture-pair-capture-legacy-integration-1020093215-643
- rt-m3-current-capture-pair-targeted-1020093216-24781

The first diagnostic run 1020092916-7547 was RED (24 failed / 43 passed /
25 deselected / 2 existing xfailed). Two JSON fixtures were corrected afterward.
That run also used the old legacy helper's archived Agent consumer, so its 18
legacy passes and 2 xfails are NOT current-pair qualification. The final legacy
helper reopens with current Agent and registers the real startup provider.
