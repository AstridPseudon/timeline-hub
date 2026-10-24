## Report

Recorded bounded evidence at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-OPS-schema-input-0918/evidence/schema-distribution-input-0918.txt`

Findings:

- `banodoco-timeline-schema` version `0.0.2`.
- Installed at `/home/user/work/venv-agent/lib/python3.13/site-packages`.
- VCS source: `github.com/banodoco/ArtAgents.git`, subdirectory `packages/timeline-schema/python`, commit/pin `242f9c4306bf3b501222cb041a9eb246ef47bc85`.
- METADATA SHA-256: `49fd34e5afe868b39ef9c7131f8093ca98017f0129faab5aa86bd5a80e2eba0e`.
- RECORD SHA-256: `50be781bec3546ca9995ce2f0aaa1284fa68198735866c0f00a601bb3ce9c3a1`.
- All nonblank RECORD hashes match installed files.
- Passing interpreter: Python `3.13.16`; schema import resolves from the installed package.
- Production `banodoco_schema` imports and re-exports the external schema types/materializer.
- `requirements/proof.lock` does not contain the distribution; `pyproject.toml` declares it only in the dev extra, using the same pin via `astrid-agent`.
- Original wheel/archive hash and durable source/artifact custody: **UNKNOWN**. Installed RECORD is not treated as original-wheel authority.

Tests/checks:

- Import-origin and identity probe: PASS.
- RECORD verification: PASS.
- `git diff --check HEAD`: PASS.
- No product tests, lint, typecheck, install, download, network, or full suite run per task scope.
- No worktree/product files changed. Commit message written to the requested path; `DONE` marker created.

Recommended next step: Runtime’s normal maker should authenticate and retain the approved schema source/artifact input before lifting the held preflight.