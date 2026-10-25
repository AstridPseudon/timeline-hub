# Report

## Verdict

**PASS — conditional protected setup review.** This is not a live acceptance claim. The orchestrator must approve the shared-seed scope.

The exact patch is mechanically valid and preserves the protected placement request/body/oracle behavior. If scope must be placement-only, this exact patch would fail scope review because `seedThreeProducts` is shared by all callers.

## Findings

- Patch SHA matches `6378b5b4…e4a`.
- Base source hash matches `92f1261b…956`.
- Derived proposed source hash matches `84563009…6809`.
- `git apply --check` passes.
- Only five line pairs change: occurrence duration, full-cover plate hold, two expected values, and the explanatory comment.
- All 21 native seed assertions remain structurally intact.
- All protected files and waits remain byte-identical.
- Placement remains exactly:
  - pointer `4.5s`, hold `5s`;
  - siblings `[3,6)` and `[6,9)`;
  - snapped interval `[9,14)`;
  - proposed host `[0,14)`, therefore boundary-valid.
- Agent guard audit confirms strict `occurrence_boundary` enforcement, translation-only occurrence requirements, FPS equality, absent source-window requirement, and final half-open interval validation are unchanged.
- Nested coverage is sufficient:
  - plate changes from `[0,12)` to `[0,14)`;
  - Agent clips remain `[3,6)` and `[6,9)`;
  - image assets have no intrinsic duration;
  - parent video remains 12s but is used only in `[0,3)`;
  - no hidden source window or timing map is introduced.

## Scope collateral

`seedThreeProducts` is used by multiple P2, P3, Agent-linked, integration, and auxiliary journeys. No caller contains a direct shared-fixture assertion requiring 12s, though the popup setup intentionally places a shared occurrence at `12s`, and unrelated P1/media fixtures independently use 12s.

Therefore the global setup correction is acceptable only with explicit orchestrator approval. Otherwise, a placement-only parameter or dedicated fixture would be required; I did not author an alternate patch.

## Verification

Commands run:

- `git apply --check <proposal>` — passed.
- `git apply --numstat <proposal>` — `5 additions, 5 deletions`.
- SHA-256 checks for proposal, source, protected files, and Agent provider files — matched supplied evidence.
- Read-only caller/source/guard audits — completed.

No product or test changes were applied. No browser, service, build, or acceptance suite was run per the review-only brief.

`DONE` and the required commit message were created.