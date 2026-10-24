## F9758 report

Prepared:

- [tests/suites.conf.candidate](/home/user/work/wt/agt-F-full-profile-candidate-1105/tests/suites.conf.candidate)
- [install manifest](/home/user/work/wt/agt-F-full-profile-candidate-1105/evidence/full9758-install-input.txt)
- [preflight facts](/home/user/work/wt/agt-F-full-profile-candidate-1105/evidence/full9758-preflight.json)

The candidate preserves `venv-agent`, Node `v20.19.4`, runtime projection/schema paths, and exact pytest arguments `-q -n 3`, replacing only the existing `agent full` row’s stale profile with `agent-remotion-v3-819acf-1110`. It preserves all 172 other rows byte-identically.

Evidence:

- Pre-registry SHA: `31cfddf…56133`
- Candidate row SHA: `0bdf88d…8dd81`
- Expected post-registry SHA: `18deaf1…9e07c`
- Qualified profile manifest: `ed4616c…9750e`
- Artifact SHA: `819acf6…40234`
- Lock SHA: `f4fc0a3…be18d`

Checks passed:

- `bash -n` and one-row/argv validation
- Registry hash, row-count, byte-parity checks
- Read-only source/import/profile/Node preflight
- JSON and diff checks
- Independent setup review: PASS

No installation, registry mutation, full suite, pytest body, source checkout, package acquisition, or runtime/profile modification was performed. Commit message and `DONE` marker are prepared.