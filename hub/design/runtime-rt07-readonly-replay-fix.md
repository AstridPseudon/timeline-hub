# RT07 read-only replay and authorization seam

The retired `publish_timeline_render` service method retains only two
behaviours from the legacy route:

1. It looks up the existing `timeline_render_publications` checkpoint by the
   authoring task reached through the attempt, validates the task's project
   still exists, and returns the stored result only for an exact stored request
   hash and published checkpoint. This path does not read the live target/spec
   or perform document, CAS, task, history, or checkpoint writes, so an accepted
   retry remains replayable after cancellation, head movement, spec removal, or
   archival.
2. Prepared checkpoints are explicitly refused with the retired-route response
   rather than resumed by the removed writer. Fresh requests retain the
   existing attempt lease, two-child admission, same-project timeline, admitted
   target, immutable-spec, and tracked-head guards, then receive the visible
   retired-route refusal without creating a checkpoint.

No table, state, credential scope, compatibility provider, or writer was added.
The original fresh legacy publication positives remain draft-red until the
Agent current-014 native replacement proves semantic equivalence.
