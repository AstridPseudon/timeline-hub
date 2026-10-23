# R2r nested inherited-range source assessment (15:50Z)

Packet independently verified: 4,790,931 bytes, SHA-256 3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09. Retained source extracted with its exact embedded text; no Agent edits or public redo.

Exact owner: runtime_protocol/timeline_commit_auth.py::_inverse_stage_history and _inverse_stage_ranges. Existing private interface receives store-authenticated immediate undo publication entries; _inverse_stage_history currently derives one expected stage from immediate undo-0, ignoring its two accepted inverse.stage partitions. Immediate source txn-75285c95600949c8b1267a71f8e71a9d retains ordered native [0,1]/[1,3] and effect [0,5]/[5,9] ranges. A projection of those actual accepted ranges into reverse execution order under immediate identity produces two bindings; unchanged Runtime rejects with `inverse stage provenance does not match authenticated history`. Durable auth-only counterexample: workers/rt-R2r-nested-range-1543/evidence/auth-counterexample.json; causal baseline log baseline-causal.txt. This diagnostic has placeholder effect sites and is not full validate acceptance evidence.

Proposed private change: subdivide only the authenticated immediate source inverse step using its accepted inherited ranges, retaining immediate publication/step/command identity, exact reverse native order and range partition. Existing boundary authentication still validates native before/after, owner/pin/digest, effects and complete output. Source history entries are sealed accepted store facts; do not use caller-provided original history or change public identity. Assess whether recursive history lookup is necessary before touching any plumbing. No edits to atomic scope or accepted historical sequential verifier.

Compiler competing-media refusal occurs earlier and remains separately unresolved. Source qualification cannot establish public redo PASS. Agent needs to emit both internally authenticated ranges under one outward immediate identity; no public two-step alternative.

## Private Agent handoff (15:56Z)

One outward command/step remains required. For retained immediate txn-75285c95600949c8b1267a71f8e71a9d / undo-0 / ordinals [0], emit TWO inverse.stage bindings with that SAME immediate publication/step/command identity, in order: native [0,2], effects [0,4]; native [2,3], effects [4,9]. Native captures reverse each accepted source slice and exchange before/after exactly. Canonical effects reverse each accepted source slice and exchange observed before/after exactly; no regenerated identity guesses. Commit.effect bindings use the current request's attribution and authenticate each intermediate boundary. The current Agent inverse_stages still yields one flattened group; Agent representation work is required. No Agent edits made here.

Runtime candidate now passes complete auth.validate on a projection of actual retained SQL/history-native/effect facts. This is an auth-only counterexample, not production provider PreparedCommit or a public redo call. Source compiled competing-media refusal remains unchanged. No extra store/port/plumbing needed: history_entry -> _verify_accepted already authenticates source ancestry, receipt, native/effect records and inherited targets recursively. Current changes are confined to inverse-stage helpers; atomic scope and accepted-historical sequential verifier are untouched.

## Final source qualification

Complete report: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-R2r-nested-range-1543-report.md

241 tests pass; explicit integration 56 pass/185 deselected. Ruff 0/0; scoped Pyright 6/6 original test diagnostics, 0 added/removed. Retained auth-only oldRED/newGREEN, frozen77 and original AST checks pass. One source-only candidate, independent review pending; Agent representation and compiler cause remain separate.
