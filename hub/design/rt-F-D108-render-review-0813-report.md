## FAIL — D108/D77 candidate review

Reviewed the exact author report, preparation JSON, retained manifest/patches, and a byte-identical private candidate copy.

Checks passed:

- Candidate compile and Ruff.
- `bash -n scripts/check-before-push`.
- `git diff --check`; worktree remains clean.
- Manifest, four durable patch, wrapper, and candidate source hashes.
- `/dev/null` manifest refusal: exit 2.
- `/usr/bin/ffmpeg` wrapper substitution refusal: exit 2.

Findings:

1. The candidate is fail-open. `EXPECTED_DIGESTS` is only reported, never compared to actual binaries. Profile input is checked only for regular-file presence; bindings only for seven-key shape. Private fake profile, fake carrier, and fake Node produced `READY` with exit 0.

2. The recipe is not complete/current: defaults point to historical `f4ed` and `agent-remotion-f4ed-0013`, forbidden by D108b. The generated command also depends on undefined `$PY`, `$PROFILE`, `$SITE`, `$REMOTION`, `$NODE`, etc. Manifest applied trees are not compared with the actual installed graph; recorded Runtime `c91626f.../16264479...` differs from retained applied Runtime tree `a522511...`.

3. Normal route confirmed: `InstallerCore → Backend.stage → source/venv/pip install → npm ci → service_declaration → profile.json`; `generic_host --service → run_pack_host_foreground → ensure_pack_host`. `Backend.stage` does not generate the D13 seven-key carrier. That carrier must come from an authentic installed profile/wheel/source deployment, not fabricated JSON.

`NOTRUN` remains `NOTRUN`; no install, service, renderer, browser, ZIP, or full suite was run. C0 contract sections 1 and 4 remain unchanged.

Smallest lawful next step: Agent installer/staging owner must provide an exact applied-Agent deployment and authentic seven-key carrier, excluding the 0013 near-match; then strengthen the candidate to validate all hashes, profile fields, referenced paths, wheel/source identity, and applied-tree identity before reporting `READY`.

Evidence: [review checks](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-review-0813/evidence/review-checks.txt>), [refusal controls](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-review-0813/evidence/refusal-controls.txt>), [fail-open finding](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-review-0813/evidence/substituted-tool-finding.txt>).