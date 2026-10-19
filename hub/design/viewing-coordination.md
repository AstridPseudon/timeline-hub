# Viewing M0 coordination

vw-m0-build repairs Composition build/test in its own worktree (network/heavy slot requested; dependency install not shared with App). vw-m0-inventory drafts viewing.md from current integration code and frozen R4 as a parts bin. Composition integration remains c82eb7c until review/merge. No M1/M3 work before Checkpoint A approval.

The initial code check confirms current App TimelineRenderer has independent Sequence/duration/transition math; playerEvaluation.ts is R4-only. Agent main has no scene_answers.py. Preserve main runtime/element-host and chapters-as-shots infrastructure while replacing viewer math. Visualize pixel verification is retained; Agent _timing_evaluators is compiler materialization and is not a duplicate viewer.

For Agent/Runtime/App contract review: viewing needs an immutable evaluated revision identity bound to the actual loaded snapshot, including linked shot revisions where present. Label local drafts/optimistic previews as local, and preserve the last evaluated revision when a newer commit is pending or preview is unavailable. Provider/compiler versions alone do not identify the evaluated document. Concrete seam proposal and package-consumption design follow in viewing.md; no change to cross-manager contracts has been approved here.

Save/dry-run/retry/inverse must run without Composition or the renderer. The pure scene evaluator can return unknown geometry/coverage, and actual Player/export pixels and PCM must still be compared with a planted mismatch negative control. No current parity pass claimed.
