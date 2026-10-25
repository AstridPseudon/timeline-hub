# D107 custody correction validation

## Result

**PASS for this corrected derivative evidence only.** This does not pass the
behavior. The historical 1550 packet remains non-clean and the independent
1640 review remains `FAIL` overall because the two authorized journeys still
fail at `tests/editing_conformance/test_m1_current_equivalent.py:317` with
`exact transcript pin is missing or revoked or ambiguous`.

The derivative corrects only the malformed 62-hex-character protected-file
value. It preserves the truthful `UNKNOWN` owner, `EXACTMISSING` persisted
record status, `source_review: PASS`, and `FAIL_BEHAVIOR_PENDING` outcome. No
historical receipt or review artifact was rewritten.

## Exact protected-file checks

Protected file:
`tests/editing_conformance/test_commit_runtime_m1.py`

Expected full SHA-256:
`23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`

Commands and results:

```text
git show 20177e66564f9f91735ed1a11bac821682d60edf:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS

git show b4b3805da5e8611490401122f986e203f67f21b4:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS

git show 2e3331ee2f035e302f5ca52488832cd0e22bb3aa:tests/editing_conformance/test_commit_runtime_m1.py | sha256sum
23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041  -
PASS
```

The old value was:
`23451aa80279f47d126e5e5699f51272a6418402ba559617c243bcd6b15041`
(62 hex characters). The corrected value inserts the omitted `b8`; the
original historical value is recorded here for custody transparency and is
not rewritten in the 1550 or 1640 artifacts.

## Invariance and preservation checks

```text
git diff --name-status 20177e66564f9f91735ed1a11bac821682d60edf b4b3805da5e8611490401122f986e203f67f21b4
M	tests/editing_conformance/test_m1_current_equivalent.py
PASS: candidate delta is limited to the authorized current-equivalent test;
no product, pin, or fixture path changed.

git diff --check
PASS: no whitespace errors in the Agent worktree.

python3 -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-custody-correction-1644/evidence/correction.json
PASS: derivative JSON is valid.
```

The Agent source-map hashes for `commit.py`, `_commit_patch.py`,
`native_word_anchor.py`, and `native_word_anchor_fixture.py` were recomputed
at `b4b380` and matched the independent 1640 source review. Runtime source
hashes and the whole-path/callgraph conclusion are carried forward from that
read-only review; no Runtime worktree, provider, collector, or behavior rerun
was performed.

The retained 1550 and 1640 evidence files were hashed before and after this
derivative was written; their SHA-256 values are recorded in
`correction.json` under `preserved_original_evidence` and remained unchanged.

## Scope and remaining status

- Original 1550 and 1640 artifacts: preserved byte-exact.
- New evidence: correction derivative only.
- Owner: `UNKNOWN`.
- Persisted record: `EXACTMISSING`.
- Failed journeys: `disjoint-rebase-undo` and `touched-basis-conflict`.
- Behavior: still pending/failing; no functional GO.
- Static tool: N/A; no helper or product code was authored.
