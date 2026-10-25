# PASS (static protected review only) — recipe occurrence media

## Scope

- Candidate: `tl/agt-F-occurrence-recipe3-0112`, revision `6762f691d3f7d1f12237cffa639334a38f8f6edb`
- Candidate baseline: `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`
- Reviewed file only: `tests/editing_conformance/test_recipe_occurrence_media.py`
- Candidate file SHA-256: `1f3da43c999670ae7d99d3ddbd1bc51ca09db181f1363c986343df18a3dd70fd`
- Baseline file SHA-256: `74157921bd73f4ff364bc9b1ce81f2ce9d01d89cf372ffff23adb5528749deb7`

## Verdict

**PASS for the protected source/static review; not functional closure.** The two assigned target scenarios are routed through the genuine Runtime fixture/provider path, while the other 13 original test ASTs remain unchanged.

The candidate's genuine fixtures invoke the existing Runtime occurrence-media fixture wrapper, preserving managed-media bootstrap and registered-provider setup. The request builder carries the full C0 v2 shape (label, step metadata, command ordinals, patch/reads, atomic merge, rationale, and group id), and the target flows include preview, native capture, commit, exact inverse/redo, restart, idempotent retry, and retired-asset reservation checks. The same-alias path preserves the original opaque `unknown.keep` baseline value and exact payload assertions. The provider path reuses the production commit/provider functions and checks history stability across the identity-collision attempt and service reopen.

I found no unsupported direct SQL, fake accepted record, old publisher, or unsupported emitter allocation in the candidate delta. The unchanged tests retain the separate registry/opaque cases; this verdict does not claim that one field or one helper fixes those other paths.

## Structural evidence

- The target mapping is the parameterized add/swap provider scenario plus the same-alias scenario.
- The 13 other original test ASTs are unchanged.
- The helper/fixture additions are limited to wiring the genuine Runtime setup and preserving the original predicates; no behavior expectation was weakened or removed.
- No test, collection, helper, fixture, service, or browser execution was performed.

## Checks

- In-memory compile of baseline and candidate: passed.
- Scoped Ruff on baseline and candidate: passed.
- Scoped mypy under Python 3.13 with `--follow-imports=silent` and private cache: passed for baseline and candidate.
- `git diff --check`: passed.

This is a static PASS only. Incremental MAIN functional proof of bootstrap, managed media, native capture, registered provider, C0 behavior, restart/retry, undo/redo, and reservation remains owed; no pooled PASS was issued.
