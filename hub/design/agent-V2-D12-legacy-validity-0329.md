# Agent V2 D12 legacy validity repair

Base: `e24f91385434f7702747eeffc051f1ce6cf44056` (`tl/agt-V2-source-clean-0220`).

The defect was final timing validation treating every legacy `app.astrid.on`/`until` declaration as newly required to resolve. The unchanged R4 P1 documents intentionally preserve an authored but unresolvable `old-anchor`; unrelated edits therefore failed before this repair.

The repair carries the authoritative base/replay bundle into `validate_candidate_timing`. It computes a reference basis for each legacy declaration from the clip timing/reference shape, pinned source documents, relevant sibling clips, and child placement/source context. Only a declaration that existed in the baseline with the same authored value and an identical reference basis is marked as an unchanged legacy declaration. The existing compiler/evaluator receives those exact rows as a narrow internal policy and ignores only those rows for resolution. Candidate authored data is not stripped or normalized, and no source mapping or fixture is rewritten.

Consequences:

- untouched base-unresolvable declarations survive unchanged and do not block unrelated edits;
- new declarations and changed declarations remain compiler-guarded;
- removal/movement of a referenced target changes the reference basis, so the formerly tolerated declaration is compiler-guarded and rejected;
- structural, parameter, media/reference, authority, history, and existing timing/compiler checks remain active.

Acceptance coverage adds create, modify, and invalidate-by-target-change 422/atomic tests, plus explicit unchanged-legacy retention. Targeted validation completed with 95 passing tests; Ruff, private mypy, no-growth checks, structure/cycle checks, and diff check all passed. Full/browser/live-socket suites were intentionally left to the central test service.
