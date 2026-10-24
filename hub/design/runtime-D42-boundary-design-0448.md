**Design result: the required stable production boundary is missing.** A production-only capsule could safely cold-miss unsupported implementations, but it cannot satisfy the unchanged warm-counter acceptance tests. No product or test files changed.

Inspected exact base `6c6bb37501582a4b56409abc5cc71a0893cdb697`, PLAN, audit 0403, and author reports 0403/0423. Their **184 passed / 9 failed** result is prior evidence; I did not rerun it.

**Concrete boundary and code seams**

Keep memoization confined to [TimelineCommitStore._verify_replay](/home/user/work/wt/rt-R-D42-boundary-design-sol-0448/runtime_protocol/timeline_commit_store.py:398). Preserve everything before that call, including fresh authority, database/history, event-prefix, closure, source, ownership, CAS and inverse-history authentication.

The reusable operation must remain exactly the current cold block:

1. Validate captured context and prepared commit.
2. Run `auth.validate_sequential_capture`, including its nested original-execution validation; otherwise enforce `sequential_proof_required`.
3. Run `auth.validate` against the authenticated landing inputs.

Memo entries should contain only successful verification, keyed by immutable bytes representing the **complete existing input tuple** at lines 409–412, plus a genuinely stable implementation version. Preserve raw JSON strings, so whitespace changes remain misses. Retain bounded, store-local LRU behavior and detached caller returns.

The necessary interface is:

```python
inputs = freeze_exact_fresh_inputs(existing_input_tuple)
capsule = acquire_supported_production_validation()

if capsule is None:
    run_existing_cold_validation()
    return                       # neither lookup nor insert

if memo.contains((capsule.version, inputs)):
    return

run_existing_cold_validation()
if capsule.still_valid():
    memo.insert((capsule.version, inputs))
```

**`acquire_supported_production_validation` is the missing primitive**, not an implementable helper supplied by today’s code. Its version must cover actual execution dependencies and remain valid throughout lookup/validation/insertion. A before/after snapshot alone cannot establish that guarantee against intervening mutation and restoration. The existing SQLite mutex protects store operations; it does not govern arbitrary Python implementation mutations.

**Why immutable schema bytes do not complete the capsule**

The schema boundary is [_schema_resources / _validator](/home/user/work/wt/rt-R-D42-boundary-design-sol-0448/runtime_protocol/timeline_commit_validation.py:51). It exposes cached mutable schema dictionaries and validator instances.

One permitted private feasibility probe established:

```text
auth.validate: no closure
schema.evolve: captures mutable list evolve_fields
schema.__attrs_post_init__: captures methodcaller, function, Specification
active resolver registry is declared registry: False
validator.schema type: dict
```

Thus, rejecting every non-immutable closure also excludes the current production validator. Accepting these captured objects by identity merely recreates the trust gap.

A valid production capsule must cover:

- Auth helpers, recursive equality, imported helper aliases and their effective globals.
- Defaults, closure cells, callable/class state and nested dependencies actually executed.
- Schema contents, keyword/type dispatch, validator methods and initialization state.
- The **active** resolver’s registry/base/dynamic scope and retrieval behavior, not merely `validator._registry`.

A frozen dataclass, mapping proxy, source/schema digest, manual version constant, or captured original function reference does not establish this. Rebuilding validators from immutable schema bytes would also bypass mutations to the current cached validator, violating the resolver refusal control.

No existing mutation-controlled owner or trustworthy invalidation generation covers those dependencies. Claiming one would require the same expanding object inspection the brief rejects, or an additional execution/mutation boundary outside this task’s constraints.

**Acceptance contradiction**

A strict production-only capsule would cold-validate arbitrary wrappers on every read. That safely observes all nine implementation mutations, but fails existing assertions:

| Existing expectation | Conflict |
|---|---|
| `setup_read` replaces `auth.validate` with a closure containing a mutable counter list | Every ordinary cache test uses an unsupported implementation |
| Closure and direct-global attack tests require a warm hit before mutation | Unsupported-state cold-miss fails their preliminary counters |
| `test_helper_defaults_change_reverifies` requires reuse after installing default `{}` | Requires memo eligibility with a mutable default |
| Schema/validator version tests require reuse through replacement lambdas | Requires eligibility outside the original production capsule |

This is evidence against treating “sealed production only” as an acceptance-preserving patch. **The authority/refusal tests remain required; no acceptance waiver is implied.**

A faithful additional observation method would leave production functions untouched and use `sys.setprofile` to count calls by retained code-object identity. Measure `auth.validate`, `validate_commit_value` and the concrete schema validator’s `validate`: an ordinary cold replay invokes auth once, a sequential replay twice; an identical warm read must add zero replay/schema executions. This resolves instrumentation of the production performance measurement, but does **not** resolve the existing arbitrary-wrapper acceptance requirements. No tests were changed.

**Verification and disposition**

Commands run:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -` — one inline closure/resolver feasibility inspection; exit **0**, results above.
- `git diff --exit-code a6843aa9322d354a8db2576a43dd202244608d65 HEAD -- runtime_protocol` — exit **0**; production source unchanged.
- `git diff --check` — passed.
- `git status --porcelain` — clean.

No suites, attacks, HTTP, providers, benchmarks or full runs executed. Lint/types N/A. Commit message and `DONE` written.

The design investigation is complete; implementation remains unresolved. Before another patch, the orchestrator needs a substantiated stable dependency boundary and an explicit reconciliation of wrapper warm-hit acceptance. Production `a684` remains unsafe and held; eventual use requires clean security review. All C0v2 behavior and fresh checks remain unchanged. **D42 remains non-blocking under D45; P2/P3 and Farm follow-through must not wait.**