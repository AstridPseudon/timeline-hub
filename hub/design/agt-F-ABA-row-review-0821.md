# F-ABA review — FAIL

- Reviewed staged candidate: 4,564 bytes; SHA-256 `290bd2bf…`.
- `bash -n tests/suites.conf.candidate`: PASS.
- Candidate source parsed; 18 guard assertions.
- Target managed-row body contains all 59 assertions.
- Original test blob remains `e55be12f…`.
- Runtime pins match:
  - commit `becfe6db…`
  - tree `7edc08e3…`
  - auth blob `979225ab…`
  - `a0dca…` source fixture commit exists.
- `git diff --check`: PASS.
- No product, candidate, registry, or original files changed.

Blocking issue: the candidate asserts Agent tree `4ce9de…`, but current `HEAD` tree is `53a852…` because `tests/suites.conf.candidate` itself is committed. `4ce9de…` is exactly `HEAD^`’s tree, so the candidate cannot reach integration execution as committed.

The supported source path is otherwise coherent: integration collection preloads `runtime_protocol` from the pinned becfe checkout; `tests.helpers.runtime` preserves first-use imports; the production publish caller reaches Runtime’s HTTP commit route and store authentication. However, actual body execution was not run per the explicit no-preflight/newrealm/full-run restrictions. The candidate also lacks a Runtime worktree-cleanliness guard.

Recommended fix: resolve the self-tree assertion strategy, and add an explicit cleanliness or loaded-auth-file hash guard before re-review.