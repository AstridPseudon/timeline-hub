# D20 shared-placement strict review

**Decision: PASS**

Reviewed `tl/agt-D20-shared-placement-sol-1305` at `aa72cb489` against base
`f6116e1b658514021cbbf08d5a6f16a240523f1a`, the settled PLAN, C0 §§1–5,
`agent-D20-old-shared-writer-fact-1254.md`, and
`agent-D20-shared-placement-interface-1305.md`.

## Findings

No correctness or security finding requiring a change.

- `occurrence.place-shared` is registered on the existing semantic carrier. Its
  arguments are closed to `occurrence_id` and `on`; physical shot/revision,
  source document, media and aliases are not caller inputs.
- The handler requires an explicit occurrence in the destination parent,
  records the complete occurrence selection, reads the selected source and its
  source closure, and binds `shared.source` only after resolving that
  authenticated closure. The source must still be unchanged published input.
- The created row appends to the existing occurrence order, retains the exact
  physical shot/internal/media/registry/opaque closure, and changes only the
  new occurrence identity, placement start and existing derived identity
  fields. Public evidence compared original rows, config, clips, registry,
  dependency manifest, shot revisions and internal revisions exactly.
- Occupied/retired IDs, foreign or missing source occurrences, foreign timeline,
  forged arguments, stale source edits, changed membership/order, malformed
  timing, and forged captured claims all refused without a write in the review
  probes. The public stale refusal was `dependency_changed`.
- Inverse alias normalization is restricted to `AcceptedRecords` containing an
  authenticated accepted `shared.source` binding. It derives source roots from
  accepted history/capture and does not accept a caller-supplied binding grant.
  The bounded source edit/delete guard regression was not reintroduced.
- The public request/reply retained the full v2 envelope and fields: exact base
  pair, commands, label, steps, merge, reads, dry-run, source, rationale and
  group ID; accepted/preview replies included canonical data, records,
  bindings, effects, dependencies, history and undo metadata. Exact retry and
  retry after Runtime reopen returned the original result without another
  write.

## Evidence

Exact author lane plus nearest guards:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa D20_EVIDENCE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D20-shared-placement-review-1320/evidence /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_occurrence_shared_d20.py tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_occurrence_delete.py --tb=short
```

Result: **110 passed in 27.04s**.

Additional bounded provider probes (13 cases):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python /tmp/d20-review-1320/review_extra.py
```

Result: **PASS**; all tamper and same-batch-source-edit cases refused with no
head or entry mutation.

Static checks:

```text
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/d20-review-1320/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/d20-review-1320/mypy-full make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python
git diff --check
```

Results: Ruff **2149 current / 2149 baseline**; mypy **1912 current / 1912
baseline**; diff check **0**. A targeted mypy pass over the three changed
source files also passed.

The public evidence file records actual origins: Agent code from this review
worktree and Runtime from `/home/user/work/wt/rt-pin-3b926efa`, commit
`3b926efab2eed122d374540baee297d4cdcec62a`.

## Limits and next steps

No full suite, browser/P2 tour, HTTP server tour, native14/58, P1/P4, or D17
matrix was run, as explicitly excluded by the brief. The known whole-undo
failure in `test_commit_runtime_occurrence_fork.py` was not rerun or credited;
the author documented that it reproduces identically on the untouched base.
Proof may now migrate the original popup fixture to this public command, while
retaining its behavioral assertions.
