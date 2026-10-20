# Agent WC5 known voiceover intent preservation

## HOLD

Candidate commit `fabac58180e4f964e3afc47e8ce0fa9a17096ff7`, tree
`be93973cae36ffa607772e6e073209cc510e467d`.

The bounded known-new-child route has the expected existing D13 proposal
shape and `TimelineSession` durable-outbox authority. It branches before
capture, leaves existing-clip regeneration on `TargetBound.publish`, and does
not introduce a public proposal wrapper/API.

Approval is held for two concrete reasons:

1. The old coordinator positive was converted. Baseline
   `test_coordinator_publishes_once_with_provenance` used readable existing
   audio, `ripple`, and real `bound.publish`; candidate lines 341-351 instead
   use a no-audio fixture, `preserve`, and `enable_known_requester`, which
   monkeypatches both capture and proposal commit. The old RIPPLE Main positive
   is therefore no longer asserted unchanged.
2. The candidate's known-child proof is synthetic. Normal
   `generation.generate_speech` output contains WAV/manifest/word rows but not
   the exact five-field project media selection or Runtime producer pin.
   `draft_voiceover_proposal.py:223-263` only propagates those fields when
   already present. The missing seam is to consume the real settled managed
   output association, use Runtime's existing project media-selection read to
   retrieve `{asset,generation_id,variant_id,object_id,catalog_digest}`, and
   carry the actual Runtime producer pin plus the frozen UTF-8 descriptor into
   native capture. No invented fields, fallback after capture, or new wrapper
   is authorized.

The direct Agent candidate test passed 27 cases, but no live/end-to-end proof
was run. A separate Runtime report's 188 passing producer-neighbor tests does
not prove this Agent path. `TargetBound.publish` remains held until all
callers migrate and the missing real producer/outbox proof is supplied.
