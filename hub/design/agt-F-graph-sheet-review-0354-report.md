# F-D86 review report

Repository remained unchanged. Evidence: [graph-verdict.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-graph-sheet-review-0354/evidence/graph-verdict.md) and [sheet-verdict.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-graph-sheet-review-0354/evidence/sheet-verdict.md).

## PASS_SOURCE — GRAPH

Candidate stack: `6be6a4af289f` + `7b10080a3aa0`.

- Final blob: `9215b5a6277d54a50ede11c44ab2a9a146a56768`
- SHA-256: `658a877438a046925d6a1b9e8f83037038739d5894b01c3fb8ff520454bf9235`
- Real Runtime path confirmed: `RuntimeService.commit_timeline → coordinator → registered Agent provider → RequestCommitPort → TimelineCommitStore`.
- Prior `DetachedRealm`/`DetachedPort.accept` synthetic acceptance is removed.
- Root graph, opaque values, both root checks, collision/refusal, inverse/redo, ABA, and no-write predicates remain.
- Stack diff contains only `tests/sdk/test_timeline_commit_graph_roots.py`; no independent outside-file delta.

## FAIL_SOURCE — SHEET13

Candidate: `f29bc274f5`.

- Final blob: `a6a3118e79fcef640c29526d76b1f7d4e1322a5a`
- SHA-256: `225c423722353a42d378c9120c913f7ca197e687f62cc307635fa782677b7221`

Findings:

1. Media fidelity is not preserved. `tiny_cut_parent` maps source `P` to `idea-1.png/image/png`, although the original fixture uses `P` on the audio `vo` track. `seed_shared_occurrence_parent` only detects audio through registry entries, missing `audio_bindings`; it also defaults video/duration-bearing inputs to image/png. Affected source IDs include `P`, `Q`, `R`, `OLD`, and `AUDIO`.

2. The four emitter findings remain unaddressed. The new canonical reload assertion checks equality but does not change the destination `emit_document_commands` call or its closure-membership/provenance guard.

Nine media selectors and four emitter selectors remain exactly retained; all ten test ASTs and 17 selectors are conserved.

## Checks

- In-memory compile/AST inspection: PASS.
- Ruff parent/candidate: PASS.
- Mypy parent/candidate shadow-file checks: PASS.
- `git diff --check`: PASS.
- No pytest, collection, helper/function execution, service, browser, build, render, or functional qualification run.

Recommended next step: repair faithful media role/MIME/duration mapping and the emitter setup, then obtain a fresh protected review.