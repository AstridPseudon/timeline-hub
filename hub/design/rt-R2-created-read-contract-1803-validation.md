# R2 same-command created-child read contract assessment

## Result

`CONTRACT_SOURCE_DISTINCTION`; no Runtime implementation was authorized.

C0's settled rule is boundary-specific:

- request reads use batch input;
- step reads use the sequential input immediately before the step's first command;
- command operands/changes use that command's sequential input;
- a later command may consume a created root only through an authenticated intermediate image;
- earlier steps are not intervening publications, but this is a conflict/undo rule, not an authorization to resolve a current command's child alias against its own staged write.

C0 does not define an authenticated post-creation boundary inside one semantic command, nor does it state a blanket “exclude own writes” exception for captured child reads. The current source therefore has a precise applicability seam but no proved contract defect: `validate` seeds the first command input from the source closure, `validate_step` resolves captured reads against that command boundary, and `site` rejects an occurrence child alias when the occurrence is absent there. Later command inputs are separately projected through `command_output`/`_project_created_child`.

## Source trace

1. `runtime_protocol/timeline_commit_store.py:1522-1536` calls `timeline_commit_auth.validate` after prepared records and canonical output are available.
2. `runtime_protocol/timeline_commit_auth.py:2891-2915` initializes the first command input to `boundary` and constructs later command inputs with `command_output`.
3. `runtime_protocol/timeline_commit_auth.py:393-426` selects `command_boundary` for each record and calls `native_site` for each captured read. The generic created exception at `:398` only permits an exact created ref whose observed state is absent.
4. `runtime_protocol/timeline_commit_auth.py:100-172` resolves occurrence aliases. At `:150-156`, occurrence child aliases require exactly one occurrence row in the supplied boundary.
5. `runtime_protocol/timeline_commit_auth.py:1896-1910,2189-2209` projects authenticated created child images for the following command, not for reads internal to the creating command.
6. `runtime_protocol/timeline_commit_auth.py:490-558,2951-2961` authenticates physical bindings against their assigned command/effect/materialization boundary; there is no same-command child alias exception.

## Contract comparison

- C0 §1 lines 112-142: captured semantic reads are dependencies; step reads are evaluated after preceding steps and can consume a prior step's output; omitted reads do not waive captured dependencies.
- C0 §2 lines 314-322: each command operand/change resolves at its sequential input; a future creation cannot satisfy an earlier lookup.
- C0 §2 lines 356-365: semantic creation establishes roots and “subsequent patches in the same batch” may address them.
- C0 §2 lines 391-430: effects may describe created roots and managed links, but those are authenticated provider output and intermediate staging values, not caller-enlarged roots.
- C0 §3 lines 614-661: read declarations use their original evaluation boundary; earlier steps are not intervening publications and later step outputs are available to later reads.
- C0 §5 lines 1593-1642: undo uses persisted physical bindings and scans later reads/dependencies; it does not establish a new same-command read boundary.
- C0c lines 2825-2835: providers must expose intermediate images before a “subsequent qualified operand” uses them, or refuse unsupported input.

The competing interpretations are therefore explicit and bounded: (A) the current command's child capture is an input read and must be authenticated at the pre-command boundary, in which case refusal is permitted; or (B) same-command child access is a required semantic behavior, in which case C0 needs an orchestrator-approved intra-command post-creation boundary/binding rule. C0 does not select B.

## Owner and conservation

Smallest proved source owner: `validate_step -> native_site -> site` in Runtime authenticated closure validation. No writer, alias expansion, new root, ghost ownership, guard, test, fixture, record collector, or provider correction was added.

Actual `records.commands`, `records.steps`, failing ordinal, stage pair, physical binding, closure pair, continuation, and historical-root facts remain `EXACTMISSING`; none were fabricated.

## Checks

- `python3.11` AST parse and compile-in-memory of the five cited Runtime Python files: PASS.
- AST callgraph extraction for `validate`, `validate_step`, `native_site`, `site`, `command_output`, `_project_created_child`, `step_output`, and store `_validate`: PASS.
- Static source predicates for first-command boundary, later-command projection, command-boundary read validation, exact created-ref exemption, and C0 wording: PASS after normalized whitespace matching.
- JSON parse of the cited App applicability facts, App review facts, and prior Runtime applicability artifact: PASS (3).
- `git -C /home/user/work/wt/rt-pin-ab1e4f61 diff --no-index --quiet runtime_protocol/timeline_commit_auth.py /home/user/work/wt/rt-R2-created-read-contract-1803/runtime_protocol/timeline_commit_auth.py`: PASS (exit 0; identical auth source).
- `git diff --check`: PASS (exit 0).
- `git status --short`: PASS (clean before evidence output).
- `git rev-parse HEAD HEAD^{tree}`: PASS (`e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`, `d5cb9335a03bf4764548e379ce180a66bf966910`).
- `git hash-object contract/commit-v2.md runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py`: PASS (`257024df...`, `75c290ed...`, `f9cf50c1...`).

No pytest, provider/body run, service/socket/browser suite, full suite, P4, tour, acquisition, collector, or D130 SWAP/WAL/recovery check was run.
