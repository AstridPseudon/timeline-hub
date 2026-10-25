# D107 independent protected-purpose and whole-path review

Candidate: `tl/rt-D107-current-baseline-1530` at `b4b3805da5e8611490401122f986e203f67f21b4`.
Base: `20177e66564f9f91735ed1a11bac821682d60edf`.
Approved source-purpose reference: `2e3331ee2f035e302f5ca52488832cd0e22bb3aa` / prior 0715 source review.

## Verdicts

- Protected purpose: **PASS**.
- Whole path: **FAIL — behavior pending**.
- Functional GO: **NO**.
- Source cause: **UNKNOWN**; the evidence does not justify assigning the failure to Runtime merely because the compiler guard reports it.

## Protected-purpose review

The exact base diff has one modified file and only the requested history-baseline hunk:
the assertion changes `5` to `8`, and the comment records three genuine bootstrap entries plus five authored scenario entries. The original M1 file is unchanged (SHA-256 `23451aa80279f47d126e5e5699f51272a6418402ba559617c243bcd6b15041`). Candidate, base, and approved source all have 131 AST `assert` nodes and 5 `pytest.raises` contexts.

The count is supported by the real source order, not conservation alone. Runtime creates the bootstrap history row with `intent=bootstrap` and null records. The current fixture then submits `initial-commit`, `initial-word-anchor`, `retain-and-clear-word-anchor`, and `current-baseline-corrections`; the retained-case setup adds `Timeline conformance edit`; the candidate adds `NEW-OURS current word binding` and `NEW-OURS independent clip`. The prior authorized XML reached line 317 in both parameter cases, so the candidate's count/first/last history predicates passed before the shared guard stopped the journey.

No authored word/declaration, FPS, opaque extension, intent, or timing input changed. The exact two parameter IDs remain present and both reach the transcript-pin guard at candidate line 317 in the existing XML evidence.

## Whole-path finding

Existing authorized result:

```text
tests/editing_conformance/test_m1_current_equivalent.py::... [disjoint-rebase-undo]  FAIL at line 317
tests/editing_conformance/test_m1_current_equivalent.py::... [touched-basis-conflict] FAIL at line 317
error: exact transcript pin is missing or revoked or ambiguous
```

The production public provider's `astrid/sdk/timeline/commit.py:_hydrate` obtains
exact document pins from the canonical `dependency_manifest.documents` and calls
the authenticated `port.transcript_source(pin)`. The pure compiler guard in
`astrid/sdk/timeline/native_word_anchor.py:97-100` requires exactly one matching
capture. The passing current recipe seam instead manually supplies the genuine
pin to `capture_anchor` at `native_word_anchor_fixture.py:255-264`; that seam is
not proof that the restarted public daemon has the pin in its durable closure.

Therefore the bounded next owner is the Agent/Runtime authenticated hydration
seam, with the minimal missing genuine record being the exact transcript
`DocumentPin` carried from the persisted canonical dependency manifest into
`pinned_documents` after restart. The available evidence does not establish
whether the missing record is in Runtime persistence or Agent hydration, so the
source cause remains UNKNOWN. Do not claim a functional pass or merge approval.

## Validation commands and exact results

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/editing_conformance/test_m1_current_equivalent.py` — `All checks passed!`
- Ruff over base and approved `git show` sources via stdin — `All checks passed!` for both.
- `python3.11` AST parse/count and in-memory `compile()` — `PASS`; 131 assertions / 5 raises.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf` — `PASS`.
- No provider/full/new-body rerun was performed in this review; the two-case result above is the prior authorized XML at `workers/rt-D107-current-baseline-1530/evidence/current-equivalents.xml`.

No source or product edit was made by this review.
