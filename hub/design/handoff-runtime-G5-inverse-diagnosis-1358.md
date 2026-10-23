# G5 inverse boundary diagnosis — Runtime859 / Agent91ac

## Result

The one bounded, instrumented invocation reached the original inverse body on
the approved current pair and exposed a concrete refusal. It did **not** reach
the historical 503 mapping:

```text
CommitRejected: inverse stage write differs from its sequential input
```

The refusal is raised while Runtime validates the Agent provider's prepared
inverse record. The exact Runtime boundary is:

```text
runtime_protocol/timeline_commit_auth.py:1398 validate
runtime_protocol/timeline_commit_auth.py:958 _inverse_stage_boundaries
runtime_protocol/timeline_commit_store.py:1120 accept
runtime_protocol/timeline_commit_port.py:622 RequestCommitPort.accept
astrid/sdk/timeline/commit.py:1181 RuntimeCommitService.commit -> port.accept
```

The exception is a `runtime_protocol.timeline_commit.CommitRejected` with the
message above. Runtime's `reject("invalid_records", ..., status=422)` gives the
structured `validation_error` / `invalid_records` refusal. The coordinator
re-raises it after the durable lookup; the service converts it to the public
structured failure. The Agent bridge turns that refusal into `CommitConflict`
because its details status is `refused`. This is current-pair evidence, not a
claim that the prior Runtime3b 503 had the same cause.

## Exact mismatch and owner boundary

The inverse request was accepted by the normal Agent `TimelineSession.undo`
caller and carried the exact full-v2 shape:

```json
{"base_revision_id":"authoring-parent-revision-caa332ccab292835ea80593b7a68c576fd0ae6f75c1953ccec15ff6b207551b0",
 "base_publication_id":"txn-17252a1958a443a2878f1cb4ed4d9631",
 "commands":[{"op":"timeline.inverse","args":{"publications":["txn-17252a1958a443a2878f1cb4ed4d9631"]}}],
 "label":"Undo timeline edit","merge":"fields","dry_run":false}
```

The captured prepared inverse record has one `inverse.stage` binding with
`native_write_range: [0, 10]` and `effect_range: [0, 9]`. Its first native write
is `ref=parent`, `path=["config"]`:

- prepared write `before` digest: `e6d3e22782252ab1f325c0013214ad30cd9669bcae8b7502321717371fbff4a9`;
- prepared write `after` digest: `3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115`;
- accepted restructure canonical parent-config digest: `3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115`.

Thus the prepared inverse's first native write carries the flat pre-restructure
config as `before` and the accepted split config as `after`. Runtime starts the
inverse stage from the accepted split image and requires the first write's
`before` state to equal that sequential input. The check fails before any
receipt can be accepted. This points to the Agent inverse-stage record/image
orientation for the restructure inverse as the next repair owner; do not patch
or waive Runtime's validator here. Hand this exact packet/input to the active
Agent inverse-stage owner (Runtime1304 coordination path) rather than creating
a parallel product patch.

## Seam evidence

The observer wrapped only in-process scratch objects and flushed each seam
before/after/exception event. For the inverse attempt:

- `coordinator.execute`: entered, then raised the same `CommitRejected`;
- `provider.commit`: entered, then raised the same `CommitRejected` from
  `port.accept`;
- `port.accept`: entered, then raised at Runtime store validation;
- `port._prepared`: returned the complete prepared candidate;
- `port.close`: completed without exception;
- `port.verify_outcome`: was not reached for the refused inverse;
- no provider, port verification, close, or coordinator lookup exception was
  hidden behind a 503.

The earlier forward setup publication reached accepted `port.accept`,
`port.verify_outcome`, `port.close`, and coordinator completion. The test then
failed at the first inverse call, so no undo/redo or later overlap refusal
qualification is claimed.

## Identity and evidence

- Runtime commit: `8592822fd11275540f596562f43c715676f2bc0f`; tree
  `ed9856f43a4e44a058bf2230badea2c4c7080050`.
- Agent checkout: `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`; tree
  `ac1251cdc911b99d690d303cdd777fe14643bdb1`.
- Original inverse test body: 6798 bytes, SHA-256
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
- Runtime and Agent worktrees were clean before and after the run.
- Loaded-origin/source hashes, request, prepared input, history, canonical
  before/after data, exceptions, and seam events are in the flat packet:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-G5-inverse-diagnosis-1358/evidence/g5-inverse-boundary-packet.json`
- Packet manifest, SHA-256, credential scan, and JSON round-trip:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-G5-inverse-diagnosis-1358/evidence/g5-inverse-boundary-manifest.json`
- Packet SHA-256: `01ccdec35f2a8f3e72e99541092f99ec20bda2de036adc6fe77d7f773157aaeb`.

## Commands and results

Read-only setup:

```text
pytest --collect-only ...::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
1 test collected in 0.77s

body-hash preflight
c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d MATCH
```

The exact one-run command used the required Agent checkout and Runtime859
worktree, disabled pytest cache/bytecode, loaded the scratch observer, and was
bounded with `timeout --foreground 90s`. Result: **exit 1 in 11.48s**, failing
at the original inverse success assertion with the concrete refusal above.

Observer checks:

- `python -m py_compile /tmp/w-ced43f274f/g5_observer.py`: passed.
- Initial `/root/.local/bin/ruff check --no-cache` found four scratch-only style
  findings (BLE001 x2, PIE810, B010); no repository code was changed and this
  does not affect the captured causal result.
- Packet credential scan: clean.
- Packet canonical JSON round-trip: equal.

No Runtime, Agent, test, contract, schema, generated, client, pin, config, or
Git files were changed. No second inverse invocation was made.
