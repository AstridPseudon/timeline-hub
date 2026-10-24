## D76 report

- Migrated only `test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter_r4_original` to the authenticated `saved_source` fixture and real `timeline.duplicate` commit caller.
- Preserved all six original assertion predicates exactly; removed mocked `check()`, `Checkout.open`, and `publish` seams.
- Diff: 7 insertions, 18 deletions; no product changes.

Test command passed:

```text
5 passed in 3.90s
```

Controls included the modified original plus the four existing duplicate controls. XML: [duplicate.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D76-duplicate-fixture-1803/evidence/duplicate.xml) — 5 tests, 0 failures/errors, exit 0.

Static checks passed: Ruff, mypy, compileall, `git diff --check`.

Provenance:

- Agent head: `7b9e21889e2142c6b288723ff0d9eafec9c5db27`
- Runtime head: `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`
- Runtime schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- Imports resolved from this worktree and `/home/user/work/runtime`.

No product seam remains. Independent protected review and normal Agent merge are pending orchestrator action.

Proposed D76 log entry: `D76 setup-only duplicate fixture migration: authenticated media admission + current commit caller; original assertions unchanged; strict 5-test acceptance 5/5.`