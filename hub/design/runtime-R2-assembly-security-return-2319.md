# R2r/P4 Security Re-review — FAIL

Reviewed exact candidate `7627c8318` against base `732c48c6f5…`.

Blocking finding: `RequestCommitPort._ancestor()` calls `reachable_document_input_pins()` after `TimelineCommitStore.history_entry()` completes its final freshness check. An injected callback mutated ancestor `timeline_commit_history.metadata_json` at that point, and `port.history_entry()` returned successfully instead of refusing.

Evidence: `provider-refusal.xml/.log`, independent witness script, at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-assembly-security-return-2319/evidence/`

Validation:

- Required security files: **235 passed**
- Neighbor suite: **192 passed**
- Corrected attacks: **14 passed**
- Finite N2/N4/N8 previews: **3 passed**
- Ruff/Pyright: **11/74 existing diagnostics; zero new**
- Compile and diff checks: passed
- Source hashes exact:
  - `timeline_commit_store.py`: `f67e5d76…2abb`
  - `test_timeline_history_assembly.py`: `f8c62bed…ab87`

No product edits, merge request, or home adoption performed. Full/core/browser suites were not run. Recommended next step: repair the post-authentication provider pin-read boundary, then repeat this independent review.