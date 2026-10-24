# Report

FAIL — causal seam identified, no fix made.

- Completed [failure packet](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-image-live-0441/evidence/inverse-path-analysis.md>) with hashes and all witness dispositions.
- Actual accepted receipt: `txn-52c00df775974c21903e25873a36dda8`.
- Failure: Runtime 422 `validation_error / invalid_records`, “landing execution output differs from the prepared document.”
- Exact causal seam: authenticated `inverse_records` are selected and passed to outer `document_from_bundle`, but dropped through `commands.py:279`, `_doc_patch.py:113-117`, and `CommitPatch.after/finish`. This matches the reviewed 0443 repair; no Runtime fault attribution is claimed.
- PASS: App producer/handoff, acceptance/history, exact retry, foreign-selection refusal/no-write, changed-body refusal/no-write.
- NOT RUN: inverse acceptance/retry, post-undo history, reopen/readback, canonical restoration, private original/landing capture custody.
- Contract doc was absent at the requested path; PLAN §2 was used as fallback.

Checks:

- `git diff --check` — PASS.
- Worktree clean; no tests or live/browser reruns performed.
- Commit message written to the requested path; `DONE` marker created.