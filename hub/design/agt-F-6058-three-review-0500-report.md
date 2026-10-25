# F-D86 review report

Reviewed three disjoint scopes against captured `tl/integration` base `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`.

- **A — ordinary sheet:** `PASS_SOURCE`. Candidate preserves all 7 tests, 150 assertions, 2 raises, and 21 named predicates. The added exact `media.admit` is consumed by production validation; `RuntimeService.close()` precedes detached preflight. No OwnerBusy bypass, fake history, manifest overwrite, or authority bypass found.
- **B — projection9:** `NOCANDIDATE / BLOCKED`. Current bootstrap creates `items: []`; the required `item-1` is unavailable through the genuine current route. Authentic legacy fixtures exist, but no current authenticated materialization seam was found. No fabricated fixture or collector added.
- **C — CLI trim3:** `NOCANDIDATE / LEGACY-ONLY DISPOSITION`. Original PNG/MIME and authored `from=1`, `to=6`, `hold=5`, `speed=2` conflict with the current native image guard. Exact three selectors and assertions remain retained; role-separated replacement coverage exists, but no faithful same-role route.

Static evidence:

- In-memory AST parse/compile: PASS.
- Ruff on all parent/candidate/current scoped files: PASS.
- Mypy on all scoped files: PASS.
- Exact scoped `git diff --check`: PASS.
- No pytest, collection, imports, services, or functional execution run per source-only constraints.

Evidence files:

- `A-ordinary-sheet.verdict.md`
- `B-projection9.verdict.md`
- `C-cli-trim3.verdict.md`

Worktree remains clean. Commit message and empty `DONE` marker created.