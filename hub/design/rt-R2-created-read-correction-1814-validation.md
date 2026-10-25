# R2 corrected created-read source/contract assessment

## Result

`CORRECTED_SOURCE_CONTRACT_ASSESSMENT`; no product change.

The original `rt-R2-created-read-contract-1803` assessment remains `FAIL` for
its contract interpretation. This packet corrects only that report. C0 already
defines each public command operand/change at its sequential input
(`contract/commit-v2.md:314-322`), permits subsequent patches in the same batch
to address roots created by semantic commands (`:356-367`), and C0c speaks of a
subsequent qualified *operand*, not only a subsequent command
(`:2825-2837`). The public sequential contract is therefore not undefined at
the same-command operand level, and the current source refusal alone does not
justify an amendment or an orchestrator-permission wait.

The narrower source limitation survives. Raw post-handler observations remain
provider recorder facts. App 1753's corrected distinction is that
`Recording.read` observes staged `self.state` into `record['reads']`, while
`finish(capture=True)` projects public command guards from `command_input`
(`astrid/sdk/timeline/_recording.py:93-99,246-255`). Those are not the same
thing. Current Runtime authenticates captured reads through
`validate -> validate_step -> native_site -> site`: the first command uses the
source boundary, and the existing created-child projection supplies a later
authenticated command boundary. Runtime has no authenticated intra-handler
boundary for accepting an arbitrary raw read made after the handler's own
write. C0 public visibility does not authorize broadening Runtime guard/trust
semantics.

No same-message/same-cause or historical-cause claim is made. No accepted,
stage, physical, or ordinal record is reconstructed.

## Reused source and owner limits

- Runtime store reaches authenticated validation at
  `runtime_protocol/timeline_commit_store.py:1491-1539`.
- Runtime command-read validation and its narrow exact-created-root exception
  are at `runtime_protocol/timeline_commit_auth.py:393-442`.
- Occurrence child alias resolution is at
  `runtime_protocol/timeline_commit_auth.py:150-172`.
- The authenticated later-command projection is at
  `runtime_protocol/timeline_commit_auth.py:1896-1910,2189-2209`.
- Binding authentication is at
  `runtime_protocol/timeline_commit_auth.py:490-558,2951-2965`.

The smallest proved seam is source-only:
`validate -> validate_step -> native_site -> site`. Runtime authenticated
closure validation owns the observed refusal. The Agent producer's current
limit is the lack of an authenticated intra-command read ordinal/intermediate
closure record, while its public guards remain `command_input` projections.
Neither fact authorizes a Runtime guard, alias, root, ownership, recorder, or
trust expansion. The actual production caller is the graph `doc.patch` path
and its recorded command reads; the held SWAP path is independent and excluded.

Actual `records.commands`, `records.steps`, failing read/path/state, exact
command ordinal, intra-command boundary, undo/redo phase, stage range,
per-ordinal closure images, physical bindings, continuations, paired receipts,
and historical-root provenance remain `EXACTMISSING`.

## Checks

The following bounded checks were run after writing this packet:

- `python3.11` AST parse and compile-in-memory of the two cited Runtime Python
  files plus the three pinned Agent recorder/graph source files: PASS (5
  files; Agent source read via the frozen commit with `git show`).
- Static source/callgraph predicates for `validate`, `validate_step`,
  `native_site`, `site`, `command_output`, `_project_created_child`, and store
  `_validate`, using the already reviewed callgraph: PASS.
- JSON parse of this assessment, this manifest, the original assessment, the
  independent review, the App 1753 facts, the prior Runtime applicability
  artifact, and all JSON fenced C0 examples: PASS.
- `git hash-object`/SHA-256 comparison against the reviewed Runtime source
  manifest: PASS; reviewed auth/store blobs and hashes are unchanged.
- `git -C /home/user/work/wt/rt-pin-ab1e4f61 diff --no-index --quiet runtime_protocol/timeline_commit_auth.py /home/user/work/wt/rt-R2-created-read-correction-1814/runtime_protocol/timeline_commit_auth.py`: PASS (exit 0; auth source matches the qualified pin).
- `git diff --check`: PASS (exit 0).
- `git status --short`: PASS (clean; no Runtime product edits).

No pytest/provider/body run, named suite, full suite, socket/browser/tour/P4
qualification, collector, acquisition, or D130 SWAP/WAL/refused-path check
was run.
