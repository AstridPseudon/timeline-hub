Completed the cumulative private repair from `7d30f3917`.

- Validates physical metadata ownership before importlib reads RECORD.
- Authenticates canonical pip wrappers, including relocated shell trampolines, and exact installer bookkeeping.
- Rechecks helper/lock pins during seeded Store reuse without a repeated wheelhouse argument.
- Validates relocation paths before target reads or metadata writes; preserves unchanged hashes.
- Updated README and manifest; retained the exact live baseline.

Validation:

- Required pytest command, plus `--timeout=45`: **84 passed**, one expected duplicate-ZIP warning. [JUnit evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-verifier-numpy-sol-0853/evidence/junit.xml)
- Scoped `ruff check --no-cache`: **PASS**.
- Parent/candidate `mypy --show-error-codes`: identical **9 known diagnostics; zero new**.
- Python compile, `bash -n`, JSON, manifest/helper pin, exact live-baseline comparison, and `git diff --check`: **PASS**.
- Four added controls reproduce failures against the inherited source. [Check evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-verifier-numpy-sol-0853/evidence/checks.txt)

Both exact pip shebang forms are supported because relocation preserves the form selected during installation. Ordinary unseeded reuse retains its existing checks without gaining original-wheel authority.

No source blocker remains. Failed candidate row attribution remains **UNKNOWN**; no actual child READY is claimed. Next: independent cumulative security review and the normal installer run.

Commit message `fix(ops): OPS-child-verifier-numpy-RECORD` and `DONE` written. No commit, installation, live mutation, or Farm request performed.