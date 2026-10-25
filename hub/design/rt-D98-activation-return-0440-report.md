## D98 report

- Prepared a private process-startup activation seam using `sitecustomize`; it wraps the real module-global `validate_claims(request, records)` and restores it at teardown.
- Observer source remains unchanged: SHA-256 `4f8c5929…4988fdc`.
- Private evidence: [activation-handback.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D98-activation-return-0440/evidence/activation-handback.json).

Checks:

- Python compile: PASS
- `bash -n activation_recipe.sh`: PASS
- Offline delegation, exception preservation, privacy, binding, and restoration: PASS
- Parsed positive control: exit 17 exactly once
- Poison control: exit 1 zero times
- No original, pytest collection, fixture, service, browser, or build execution
- Runtime worktree remains clean; no production/protected files changed

Selected IDs preserved: occurrence ordinal 1, placement ordinal 59, recipe ordinal 141.

D82 classification: `UNKNOWN`; no genuine refusal was run, so no field mismatch or owner is inferred.

Commit message written and `DONE` marker created.