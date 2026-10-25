# FAIL — canonical placement review

Candidate `a4df15cc...` differs from clean base `1e34f8eac5` in exactly two files.

Findings:

- `three-products.p2-elements-assets.spec.ts:815-820` requires a new projected shot revision and child revision.
- The unchanged assertion at `:1117` still requires `after.shot_revisions` to equal the original revisions. This contradicts the candidate’s own accepted path and will fail when `shot_revision_id` changes.
- Strict mutation probing found the helper accepts fabricated shot payloads, extra child fields, extra shot records, changed existing child rows, and a wrong child owner. This fails C0 §2’s verified physical/owner/closure and complete-field requirements.

Checks:

- Required Node tests: 126/126 passed — `123 + 1 + 2`.
- Three serialized TypeScript projects: passed.
- Scoped ESLint: passed with zero warnings.
- `git diff --check`: passed.
- Independent 11-mutation probe: 5 invalid mutations incorrectly accepted.
- No browser, service, build, full suite, install, or product fix run.

The candidate was not applied or merged. The review worktree is restored clean at `1e34f8eac5`. `DONE` and the review commit-message file were created.