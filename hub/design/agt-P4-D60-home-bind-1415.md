## Report

- Added [tests/suites.conf.candidate](/home/user/work/wt/agt-P4-D60-home-bind-1415/tests/suites.conf.candidate) refreshing the existing `p4-current-becfe-http-3legs` row.
- Guards Agent home `5492fc8041…`, tree `9fce413c…`, ancestors `acf87bd992…` and `512f83d838…`.
- Guards Runtime `e68cf231…`, tree `a2cbedd1…`, all 15 canonical hashes, venv-agent, Node 20.19.4, and profile `819acf`.
- Preserved all three original selectors and confirmed their blobs match `47b744dfe9`.

Validation:

- Candidate syntax/serialization/source/module/client/env verifier: PASS.
- Candidate preflight + collection-only: `3 tests collected`.
- `git diff --check`: PASS.
- No test bodies, authenticated requests, service run, XML/log generation, or full suite run.

Existing core XML/TSV evidence was retained read-only; no 158-test rerun.

The shared central registry was not modified because this worker may write only inside its worktree. The orchestrator should apply the existing guarded CAS installer to this candidate, preserving UTC backup, mode `0600`, and outside-row byte identity.