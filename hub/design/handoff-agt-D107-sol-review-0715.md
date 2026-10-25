# F-D86 D107 protected Sol review — PASS_SOURCE

Candidate reviewed: `2e3331ee2f035e302f5ca52488832cd0e22bb3aa`

Candidate parent: `9d3c7a1c3983e3b553acd5d1c08552fe3165c919`

Verdict: **PASS_SOURCE**.

This is a source-only protected review. It is not a functional PASS, normal-
ready decision, merge approval, or premature D107 retirement.

## Dependency disposition

`2154168d308bdf5b0903d150cd3855765685f92f` remains **HELD** and is not an
ancestor of captured integration. The current word-choice product dependency
must be released before MAIN proof. D108 still pauses the new family bodies;
D110 remains independent. Do not merge this candidate before that dependency
and meaningful MAIN proof.

## Source scope and conservation

Only `tests/editing_conformance/test_m1_current_equivalent.py` changes in the
candidate. The original
`tests/editing_conformance/test_commit_runtime_m1.py` is unchanged; its exact
SHA-256 is:

```text
23451aa80279f47d126e5e5699f51272a6418402ba559617c243bcd6b15041
```

The original has 87 AST `assert` nodes and eight `pytest.raises` contexts. The
candidate has 131 assertions. The supplied predicate TSV has 111 mapping rows
(112 lines including its header), covering original assertions/raises and the
nine helper-call purposes requested by the handoff. The original ten remain
unchanged. The exact archive-read `79c94` scope is separate and is not merged
into this current-equivalent combination.

## Predicate verdict

The candidate closes both prior Luna FAIL_SOURCE reports in one current-form
combination:

- It obtains the genuine current source through the retained native fixture and
  registered production provider, passes the existing declaration, stable word
  ID, offset, occurrence source and document pin, then commits that binding
  before the public SDK journey.
- It recreates the original audio topology through the current document
  emitter: `music-bed` is audio on `music-other`, retains `hold=5.5` and the
  exact opaque extension, uses the actual source media identity, and has an
  independent `music-other` peer.
- It uses the actual current CLI grammar, `edit film --clip ... --on 1`, and
  records CLI source plus exact canonical readback. It does not restore the
  retired `--publication` flag.
- A is submitted through the public registered provider; the durable 200 is
  followed by a lost ACK, with persisted flight path/key/body, pending A and
  exact retry path/key/body checked.
- B is queued while A remains unacknowledged, before restart. Its exact guard,
  order, chained base and pending state survive the peer write and restart.
- The disjoint branch proves a current `merged` result and preserves the peer
  field; the relevant-peer branch proves `value_conflict`, no new history, and
  retained pending/conflict/flight state.
- Foreign actor and realm are refused. A genuinely provisioned second editor
  cannot open the first editor's outbox; persisted bytes and history remain
  unchanged.
- Undo uses the current `undo film --commit RECEIPT_ID` route. The exact
  `timeline.inverse` command body, CLI source, canonical inverse, history
  provenance and guarded redo are checked.
- Accepted B is reread after undo through the full exact readback, then its
  original body/key is retried. The complete response, path/key/body and
  history remain unchanged, proving immutable accepted-B replay at source
  level.
- Exact document/shot/internal pins, dependency-manifest media equality,
  authored 1/2/3/4-second inputs, current `30000/1001` frame mapping and
  opaque values are retained. The current output mapping is explicitly
  `1.001/2.002/3.003/4.004`, and the inverse inspection is `[1001, 500]`;
  this is the correct current rational equivalent, not a changed authored
  input or a claim that the old integer output remains literal.

The static caller trace is real: `cli.py:_cmd_undo` calls
`cli_native.commit_edit(inverse=True)`, which verifies history and calls
`TimelineSession.undo`; public writes use `WorkspaceClient.commit_timeline`
through the registered `astrid` provider. Current signatures for `open`,
`queue_move`, `flush`, `_flight_body`, `undo`, transport commit and credential
provisioning match the candidate. No synthetic acceptance, direct history/CAS
write, mocked verifier, arbitrary credential authority, product writer or
schema/client/pin edit is present.

## Explicit semantic limit

The original M1 source contains no A→B→A intervening-write tail, equal-byte
inverse refusal, or whole-store row-count no-write guard. I independently
checked the original source inventory and did not invent an ABA scenario. The
existing genuine ABA tests remain unchanged, were not run, and are not claimed
to close this combination. C0's separate ABA obligation remains with those
tests.

The current native source has a genuine by-design refusal in
`tests/editing_conformance/test_native_word_anchor.py::test_native_move_refuses_anchor_basis_until_explicit_clear`
(source lines 662–676; guard in `native_word_anchor.py:40–45`). The candidate
binds the current native choice to `card`, then performs the original numeric
music-bed gesture sequence with independent `music-other`; it does not move
the natively bound card. This faithfully supplies D107's current word-bound
baseline plus the original gesture combination without pretending that a
native-bound target can move before explicit clear. It does not treat setup
failure as a refusal and does not claim the same-bound-target refusal closes
the combined M1 journey. Requiring a move of the bound card would be a
different current scope, whose exact by-design refusal is already cited.

## Static evidence

Source-only checks, all PASS:

```text
candidate / parent / original AST parse and in-memory compile: PASS
/home/user/work/venv-agent/bin/python -m ruff check --no-cache <candidate|parent|original via stdin>: PASS
/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir=/dev/null <candidate|parent|original via stdin>: PASS
git diff --check parent..candidate: PASS
```

No pytest, import/collection, helper/fixture/test-body execution, probe,
service, socket, browser, render, install, or full suite ran. Evidence is in
`workers/agt-F-D107-sol-protected-0715/evidence/`.

Recommended next steps: retain HELD status, release/verify dependency 2154,
run the two authorized current-equivalent parameter cases on MAIN, then run
the independent D108 gate. Do not claim the original legacy input itself was
recreated or that ABA is closed by this candidate.
