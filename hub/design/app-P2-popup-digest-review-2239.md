## Result: PASS

Applied the exact digest correction to [three-products.p2-popup.spec.ts](/home/user/work/wt/app-P2-popup-digest-review-2239/tests/e2e/local/three-products.p2-popup.spec.ts).

- Captures the original response body.
- Recomputes `document_digest` using pinned Runtime Python canonicalization.
- Preserves all request, receipt, canonical-document, reload, undo, and guard assertions.
- No other repository files changed.

Checks passed:

- All three required TypeScript checks.
- Scoped ESLint (`--max-warnings=0`).
- `git diff --check`.

Hashes:

- Proposal SHA: `fa30b382…de52f6` verified.
- Source SHA: `4292d0b5…7d1de9` → `f7dedc84…f237b6`.
- Target blob: `e8eef3daefd841017a81e1eb3cad37fda357183f`.
- Expected app tree: `6fab0e5eae1e9d008afbd3115798698245d6986c`.
- Base head: `bceb0350326f22beefdde5c5ba275412bb09b419`.

The supplied patch had invalid hunk counts, so literal `git apply --check` failed; the exact intended content was applied with `apply_patch` without modification.

Unverified: browser/service ADD replay and mutation-refusal control were not rerun per the no-browser review rule; retained author evidence reports them passing. The shared deletion ledger was not edited because it is outside this worktree and protected by workspace rules; manager should record the D83/D82 ledger line with the retained hashes.

Commit message and `DONE` marker created.