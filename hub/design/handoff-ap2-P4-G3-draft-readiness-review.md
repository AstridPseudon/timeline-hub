# Handoff: P4 G3 draft-readiness independent review

Result: **PASS** on the draft report’s accuracy and ownership mapping; this does not claim P4 or H3 completion.

Base `b0a169a51a88c0f71e69cee894316a2450549856` is clean and unchanged by this review. The emitter is executable for structural translation: one scalar edit produces one guarded `set`; an existing empty note map produces ten ordered absent-value changes in one `doc.patch` command. The command registry and local executor still reject `doc.patch` as `unsupported operation`, which is the intentional R1 seam.

Corrected API mapping: ten independent steps are not an absent G2 API. `Timeline.command()` creates one step per command, and `TimelineSession.commit_many()`/`submit()` already preserve arbitrary command/step lists in one request. After R1 generic admission, ten separate `doc.patch` commands and ten steps can use that existing shape. However, G3’s default bundle emitter currently returns one command for ten changes, so G3 still owns the helper/front-door wiring (or equivalent command splitting) needed to meet the full P4 ten-note/per-step-undo case. Do not reduce that requirement to ten changes in one step.

The remaining minimal gaps are accurately assigned: R1 for generic patch validation/execution/guards; G2/G3 for submission and CLI/sheet wiring; R2 plus Runtime R2r for guarded per-step undo and authoritative step history. Existing seven facade nodes pass, but use generated/fake transport and therefore are not Runtime/provider acceptance. Generic conflict/re-run, accepted ten-note commit, per-step undo, and authoritative show/history remain unexecuted.

Evidence logs: `/tmp/p4-g3-review-targeted.log`, `/tmp/p4-g3-review-emitter-boundary.log`, `/tmp/p4-g3-review-ruff.log`, `/tmp/p4-g3-review-mypy.log`, `/tmp/p4-g3-review-diffcheck.log`.
