## Report

Completed a read-only handback. No product/test/store/generated/schema/pin changes.

Exact three IDs are numeric9 rows 93–95:

- `before=2 → after=2.0`
- `before=1 → after=True`
- `before=True → after=1`

All target `occurrence:occurrence-1/clip:clip-1`, and all fail at the authenticated inverse effect-image guard.

Findings:

- Producer: Agent `clip.set-params` writes `params.x`; inverse construction is in `_commit_patch.finish` / `inverse.py`.
- Verifier seam: Runtime `timeline_commit_auth.py:1737-1739`; surfaced via `service.py:2518`.
- Source does not prove producer or verifier fault. Runtime store remains D94-owned.
- These are distinct from the inverse-four word/restore/clip-delete findings.
- Missing proof: accepted source records, rejected PreparedCommit, ordered stage native/effect ranges, `commit.effect` bindings, complete before/after closure images, and submitted-vs-produced command pair.

Evidence: [source-handback.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-numeric-three-source-0358/evidence/source-handback.md)

Checks:

- In-memory AST compile: PASS.
- Runtime Ruff: PASS.
- Runtime scoped mypy: PASS.
- `git diff --check HEAD`: PASS.
- Agent Ruff: existing baseline findings only; no fixes applied.
- No pytest, collection, service, browser, build, or functional PASS run.

`commit-msg` and `DONE` created.