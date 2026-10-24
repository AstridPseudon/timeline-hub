# Report

Both harness source hashes match the supplied SHAs and both branches are direct children of Agent `bb50a43c...`.

## Discovery harness — FAIL

- `tools/run-discovery-original-0603.py:392-395` compares `package-lock.json` against the Composition archive SHA `819acf...`; the actual pinned lock is `f4fc0a32...be18d`. Genuine candidates fail preflight.
- `preflight` and `run` behave identically; the body always runs after successful checks. There is no reviewed-harness/manager gate.
- Dirty Agent/Runtime source status is recorded but not rejected.
- Setup failures can mask durable `after.json` evidence due to possibly unbound `environment`/`command`.
- Positive: exact target/function/assertion hashes, 9 assertions, 10 support calls, transition invocation 6, exact selector, `--timeout=45`, no observer mutation.

First fix scope: correct the lock digest, separate body-free preflight from explicit reviewed execution, require clean source custody, and harden failure recording.

## Generic harness — FAIL

- Profile locks and Node20 are only recorded, not pinned to expected values.
- No `819acf` Composition archive verification; arbitrary `--profile-root` and `--node` overrides are accepted.
- Missing `node_modules` can pass preflight.
- `RECORD` rows/digests and canonical Agent/Runtime `direct_url.json` roots are not verified.
- Body/function/assertion hashes are self-derived; no independent expected hashes are enforced.
- Only the target test file’s cleanliness is checked, not the complete source tree.
- Positive: explicit reviewed harness SHA gate, exact cleanup/harvest/reopen selector, no overlay, one pytest node, timeout 30, JUnit and invocation/result evidence.

First fix scope: strictly pin profile/archive/executable/dependencies, validate full RECORD/direct URL provenance, add fixed body hashes, and require clean source custody.

## Verification

- `python3 -m py_compile ...`: PASS
- `ruff check ...`: PASS
- `git diff --check` for both candidate commits: PASS
- No body, preflight, build, install, host, probe, or full suite was run.
- Review evidence: `.../workers/agt-F-candidate-harness-review-0619/evidence/source-review.md`
- Worktree remains clean.