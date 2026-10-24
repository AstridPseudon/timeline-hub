## Result

- Source/result: **PASS**
- Producer custody/adoption: **FAIL** — Agent and App consumers are stale.
- Runtime HEAD/tree: `becfe6db...` / `7edc08e3...`; upstream `795379a...` is ancestral.
- Worktree remained clean; no source, test, generated, client, pin, or consumer changes.

## Evidence

- Retained run: **409 passed, 0 failures, 0 errors, 0 skips**, 101.45s.
- JUnit `/tmp/w-903992ea74/freeze-integrated.xml` is absent; it was not reconstructed.
- Retained log SHA256: `66a8ee75778e4f626d1ba12b672a2fb638cce46fa73c6759641e777903bd0fa7`.
- Generator, artifact-manifest, and diff checks passed per retained evidence.
- `tsc --noEmit` was reused from exact reviewed generated-byte identity.

Evidence:

- [artifact-manifest.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-FREEZE-result-review-0727/evidence/artifact-manifest.json)
- [producer-custody.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-FREEZE-result-review-0727/evidence/producer-custody.json)

Agent’s read-only vendor check failed: pinned source `45c3a7...` and manifest `100eb4...`; frozen Runtime is `becfe6db...` / manifest `650857...`. Agent metadata and generated client hashes differ; App TypeScript generated files also differ.

Next step: re-vendor Agent/App from the frozen Runtime using their documented vendor paths and commands, then rerun consumer qualification.