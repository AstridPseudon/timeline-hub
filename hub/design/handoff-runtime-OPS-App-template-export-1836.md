# Runtime OPS-App template export 1836

Status: approved registration pair exported and verified. No P1 body, benchmark build, package install, queue request, or product/runtime source change was performed.

## Authentic sources and provenance

- Suite row source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`, exact `agent remotion-env-nodes` row 56, including its source LF delimiter.
- Environment source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion.env`.
- Environment custody comparison: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-runtime-request-custody-1343/evidence/agent-remotion.env` is byte-identical.
- The ORCH snapshot is not a Git worktree, so it has no Git revision. The approved Runtime validator used for the check is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-runtime`, SHA-256 `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`. Runtime stayed at clean `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

## Exported artifacts

- `handoff-runtime-OPS-App-template-export-1836-suite-row.txt`: regular 708-byte file, exact validator row payload (the source `suites.conf` LF delimiter is excluded exactly as `make-runtime` does before hashing); file SHA-256 `ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`.
- `handoff-runtime-OPS-App-template-export-1836-agent-remotion.env`: regular 523-byte file, SHA-256 `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`.

Both files are below 50 MB and are not symlinks. No whitespace, quoting, or line content was normalized. The env contains only PATH and three Astrid path variables; the credential-marker scan found no credential variable names.

## Validation evidence

- `cmp -s exported-suite-row <(sed -n '56p' ORCH/tests/suites.conf | tr -d '\n')` — PASS; direct source line comparison including LF was also PASS before extracting the validator payload.
- `cmp -s exported-agent-remotion.env ORCH/tests/agent-remotion.env` — PASS.
- `cmp -s exported-agent-remotion.env workers/rt-OPS-runtime-request-custody-1343/evidence/agent-remotion.env` — PASS.
- Read-only key/call-shape parse — PASS: key `agent/remotion-env-nodes`; `env -i` registration; preserved `python -m pytest -q -n 2` call.
- `bash -n handoff-runtime-OPS-App-template-export-1836-agent-remotion.env` — PASS.
- Current `make-runtime` approved-template validation ran in a private scratch ORCH/work root with `remotion-env-nodes`, exact Agent source `78738040d72ce74c42ddf7731221aecb06f9246d`, and Runtime source `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. It printed `registration_template=remotion-env-nodes identity=validated`, then refused before build/publish only because the private run intentionally supplied no Node toolchain. No runtime destination was created.
- `git diff --check` and `git status --porcelain=v1 --untracked-files=all` in the Runtime worktree — PASS; clean.

Readiness: the authentic pair is ready for App import unchanged. The actual seven-argument production request, P1 runner, benchmark, install, and full evidence remain unperformed as required.
