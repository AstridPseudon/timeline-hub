## D91 report

Read-only diagnosis complete; no product, test, schema, generated, pin, or ledger files changed.

Findings:

- Original-third failure is a real finite-interval mismatch, not a Runtime guard cause.
  - Fixture source: `occurrence-3 → shot-3 → film-shot-revision-3 → film-internal-3 → clip-3`.
  - Original clip: `at=0`, `hold=1.8`.
  - D91 moves `occurrence-3/clip-3` to local `3.5`, producing `[3.5, 5.3)`.
  - Host patch changes physical parent `occurrence-3` from `1800ms` to `2000ms`, so its local bound is `[0, 2.0)`.
  - First refusal: `astrid/sdk/timeline/validation.py:252`, on alias `shot-placement-96f3...`, `clip-3`.
  - Runtime `service.py:2518` only reports the failure location.
  - Owner/action: D91 fixture/source authoring. The protected `2000ms` host does not make the requested child-local move valid; no Runtime relaxation is justified.

- Authored-first failure is a same-batch alias/materialization seam.
  - `occurrence.place-shared` creates `repeated-third` via `ctx.create_entity` (`native_occurrence_shared.py:324`); local staging confirms the record exists.
  - The later physical `doc.patch` enumerates that shared source’s owners and calls `State.get` on `occurrence:repeated-third/shot`.
  - `State.shot_item_map` (`_command_state.py:341-346`) rebuilds the immutable `_runtime_document` baseline, whose placements contain only `occurrence-1/2/3`; the precise missing record is baseline placement `occurrence_id="repeated-third"`.
  - Failure occurs at `one(..., identity='repeated-third')` before `item_id_map` validation. No wrong physical ID is proven.
  - Alias allocation/materialization is otherwise traceable through `_authoring_shot_id`, `_copy_shot_for_placement`, `source_mapping.shots[*].item_id_map`, and the materializer. This is a logical alias versus immutable-baseline lookup mismatch.
  - Owner/action: Agent SDK `_command_state.py` / batch materialization seam, or D91 setup batching at `test_commit_runtime_shared_inverse.py:92-147`. The passing shared-item path commits placement first, then rebuilds the canonical bundle before payload patching.

Evidence observed from 0427: exact central command `pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`; result `5 failed, 5 errors`. I did not rerun pytest per the read-only brief.

Static verification:

- AST parse of 8 relevant source/test files: passed.
- `git diff --check`: passed.
- Worktree remains clean.
- Commit message and `DONE` marker created.