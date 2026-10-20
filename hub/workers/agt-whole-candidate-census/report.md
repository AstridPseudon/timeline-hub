The census is written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-whole-candidate-writer-census.md`, and the DONE file is created. The worktree is unchanged, and I did not edit the ledger.

## Most important finding

The "held" status in the 06:59Z INBOX does not match the code. Runtime already refuses the route. `runtime_protocol/service.py:2598-2600` routes `publish_parent_composition` through `_require_timeline_command()`, which raises `RetiredRouteError` (`service.py:1604-1611`). That means every production caller of `publish_authoring_candidate` fails against the current Runtime tip. Only the stub-writer tests pass.

I could not confirm this by running tests, because the sandbox denied pytest. This comes from reading the code. The two Runtime-backed tests, `test_authoring_bundle.py:1035` and `test_authoring_media.py:270`, should fail at the tip. The Runtime owner and the orchestrator need to reconcile this.

## Summary of the census

- **Single-command edits, convert first:** `update-element` maps to `clip.set-element`, which the INBOX already approved. `replace-parent-media` maps to one media-swap command. The swap needs an explicit shared-shot versus this-occurrence intent.
- **Producer case:** voiceover sync (`sync_draft_voiceover` → `TargetBoundAuthoringBundle.publish`) is the clean "producer proposes, requester commits" example.
- **Partial:** `timelines publish` (the whole-document Checkout path) can only move to commands once cut-sheet, restructure and narration edits are command-backed or refused. `TimelineSession` already commits EditCommands for moves and undo, so the target path exists.
- **Approval and promote:** no production callers. Delete `promote_approved…` and rewrite `approve…` to bind the proposal digest.
- **Adjacent broken callers:** `create_empty` (behind `timelines create`), `reference_realm.py` and `shot_composition_migration.py` also call the retired route. They must migrate before the Runtime route can be deleted.

## Other outputs

- **Line counts:** about 506 lines are removable without touching the Checkout path, and about 355 more are contingent on it. Total is about 860 before replacement code. This is an estimate.
- **Tests:** about 45 functions touch the writer path, and roughly 9 more stub it. Re-pointing and strict-xfail handling are in the doc.
- **Ledger rows:** ten proposed rows, WC1–WC10, are in the doc as text only.

## Corrections to the brief

- `promote_approved_authoring_candidate` is at `authoring_bundle.py:1538`, not ~1605.
- `publish_authoring_candidate` is at `:1587`, not ~1640.

## Not verified

- Whether the Runtime-backed tests fail at the tip (§0.2 of the doc).
- The line-count estimates, which are from file spans and not measured after conversion.

No full* suite was requested.
