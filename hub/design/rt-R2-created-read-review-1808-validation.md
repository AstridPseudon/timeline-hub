# R2 created-read contract review

## Result

`FAIL` for the author assessment's contract interpretation; `NO PRODUCT CHANGE`.

The assessment's statement that C0 only permits post-creation images for a
subsequent command and leaves same-command visibility undefined is too broad.
C0:314-322 makes every command operand/change sequential, including preceding
creations/removals. C0:356-367 expressly permits subsequent patches in the same
batch to address semantic-command-created roots. C0c:2825-2837 says the
intermediate image must exist before a subsequent *qualified operand* uses it,
or unsupported input may be refused. These rules define the public sequential
contract without limiting the word operand to a separately numbered command.

The narrower source conclusion survives. The graph fixture's `test.create-roots`
handler creates roots and then selects, reads, binds, and writes
`occurrence:new-occ/clip:title` in one command (Agent
`test_recorded_graph_roots.py:112-123`). Agent `Recording.read` retains the
staged `self.state` observation (`_recording.py:93-99`), while
`finish(capture=True)` projects public guards from `command_input`
(`_recording.py:246-255`). This is the App 1753 correction: staged reads remain
in `record["reads"]`; public guards are command-input projections.

Runtime currently seeds the first command boundary from the source closure and
validates captured reads against that boundary (`timeline_commit_auth.py:2891-2915,
393-442`). Its occurrence resolver therefore rejects a child alias when the
created occurrence is absent (`:150-156`); the exact-created-root exception only
skips an absent read of the root itself (`:396-399`). Runtime does have an
authenticated projection for a later command in the same step
(`_project_created_child`, `command_output`:1896-1910, 2189-2209), but not a
general intra-handler raw-read boundary.

That is a source applicability limit, not proof that C0 is ambiguous or that
Runtime must widen trust. C0 requires provider facts and preserved evaluation
boundaries for captured reads (112-155, 603-612), but does not turn every raw
post-handler observation into a public command-input guard. A producer can meet
the existing public contract by putting child access in a subsequent qualified
operand/patch with authenticated intermediate bindings, or by refusing
unsupported input. No amendment, guard, alias, root, ownership, recorder, test,
fixture, or provider change is authorized here.

## Evidence boundary

Prior execution only: graph `8 PASS / 1 FAIL` on `5e9ad`; original True case
failed on `ab1e`. This review did not rerun it. Accepted `records.commands` and
`records.steps`, failing read/path/state and ordinal, intra-command boundary,
stage ranges, physical bindings, continuations, and paired history receipts are
`EXACTMISSING`; no such facts are inferred.

## Checks

- AST parse and compile-in-memory: PASS for current Runtime auth/store and the
  four pinned Agent source/test files.
- JSON parsing: PASS for 20 fenced C0 examples and all cited author/App/prior
  review JSON artifacts.
- Static contract/source predicates and auth callgraph symbols: PASS after
  whitespace normalization.
- Runtime auth/store match qualified `ab1e` source pins: PASS.
- `git diff --check`: PASS.
- Product/provider/pytest/full/socket/browser/tour/P4 tests: not run per the
  read-only brief.
