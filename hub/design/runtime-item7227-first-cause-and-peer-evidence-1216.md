# Runtime RT08 item7227: first cause and peer scope

Classification: **fixture-ordering false positive, not a product save failure**.

The cached result
`rt-m2-rt08-item-global-witness-source-1148-private017-agent4b7-integration-1021120712-7227`
fails before the door starts. The test directly requests the `agent` fixture;
its setup installs the `evaluate_closure` tripwires first. The test body then
calls `publish_source_items` at
`tests/test_timeline_projection_occupancy.py:427`, whose helper calls legacy
`publish_parent_composition` at line 99. The first production frames are
`runtime_protocol/service.py:452` (`_durable_mutation`) and
`:3076` (`publish_parent_composition`), followed by the test guard at
`tests/test_timeline_commit_integration.py:72`. There is no `/v1` frame.

The `/v1` acceptance chain is `server._timeline_commit` ->
`RuntimeService.commit_timeline` -> `_execute_timeline_commit` ->
`CommitExecutionCoordinator.execute` -> provider commit; static source review
finds no evaluator call in that chain.

Recommended source-only repair: use the existing `shared_editing` ordering
pattern, or a narrowly scoped fixture modeled on it—publish the source before
`request.getfixturevalue("agent")`, then install/register the provider. Keep
the tripwire for all actual commits.

Peer handoff `handoff-agent-to-runtime-rt08-global-item-proof-1200.md` records
Agent `e736332f14a07601659285d5fffc4f81a1ef2a44` / review1130 as accepted
bounded direct-Service evidence. It proves source item identity and one-entry
physical item mapping, reload, and own-slot placement/inverse. It does not
prove refusal of an item identity already occupied by an unrelated global
shot. That same-project/global item-occupancy refusal, atomically preserving
DB/head/history/closure, remains the Runtime gap. Do not repeat the passing
Agent proof.

Next step: correct ordering, then run only the existing test7227 selector. A
guard hit after `/v1` is reached would be a new genuine counterexample; the
cached result is not.
