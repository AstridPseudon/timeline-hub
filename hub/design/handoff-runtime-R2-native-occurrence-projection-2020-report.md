# R2 native occurrence inverse projection

Implemented the narrow Runtime repair on base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (tree `f79a2355cfb39d9ada7721978bd20d5702105778`). Only `runtime_protocol/timeline_commit_auth.py`, additive tests in `tests/test_timeline_inverse_stage_authentication.py`, and a 145,292-byte lossless finite JSON fixture changed.

Independent cause finding: exact retained 060 input reaches the original native/effect coverage refusal on unchanged 2a9. Recursive comparison at that exception differs ONLY at `parent.occurrences[0..2].shot_revision_id`; physical root sets and every other payload byte match. Runtime authenticated the physical rows, stripped the pins for comparison with the authored native capture, then projected that capture directly back to the physical collection. Agent f27 and f120 have identical `astrid/` production bytes (`git diff --quiet ... -- astrid`, exit 0); their State.set requires an exact authored-row permutation. The competing Agent-emission attribution is not supported by this capture and was independently retracted in `design/agent-G5-c271-cause-return-2017.md`.

The correction accepts only a present collection with the same unique occurrence membership and exact per-ID authored rows, including owner/shot and every unknown field. It reorders deep copies of the already-authenticated physical input rows. No pin is taken from a claim, no identity is inferred from equal payloads, and no stage root is overlaid. Existing source/range/history/before/effect coverage checks remain in place. The unchanged Runtime coordinator/store invokes the existing auth.validate path; no DTO, command, writer, store, schema, contract, generated/client or frozen34e change.

Added one exact retained-input positive and 23 refusal cases: duplicate/missing/foreign rows, changed shot/authored payload/unknown field, injected native pin, malformed/absent after, changed before, wrong order, forged/swapped canonical physical pins, changed internal pin/owner, effect before/after/coverage, native/effect ranges, missing/foreign/tampered source history. Each refusal requires invalid_records and lossless inputs; nine assert the new permutation guard specifically. All existing test/fixture bodies, assertions and marks are unchanged (AST comparison against HEAD).

## Custody and no-write evidence

Flat original archive:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-c271-cause-review-2013-packets-a8dcf1d1.tar.gz`

Verified SHA256 `a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4`, 14,794,303 bytes, 85 members. Adjacent manifest SHA256 `e44a72454b1f641c385dcc0ba0177bd40bc58ae009b2301b69ba6a6fcac361d5` verified.

Exact member `./run/cases/060-port-prepared.json`: SHA256 `58051ef4e6e23f717c07fdce2d12e8d2b74caa106eb8422fe6e1c604c34f9d4d`, 5,268,985 bytes. Extracted only in TMPDIR. The new fixture is its exact request/prepared, exact captured expected-head source closure, and only `records.undo_of` entries selected from captured `before.history.items`; object equality verified with no request/candidate/history rewriting. Fixture SHA256 `50d9e08be8efa3e9f4d1d789ab99fd2c76d7e92bbeacfba543f65d2a331145c0`. JSON whitespace/duplicate packet views are excluded, all selected finite JSON values retained.

Captured Runtime auth origin is `/home/user/work/wt/rt-pin-2a9e347f/runtime_protocol/timeline_commit_auth.py`, SHA256 `3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef`. Captured Agent origin is agt-G5-c271-isolated-2010/f27; exact relevant source hashes and current source hashes are in the flat custody JSON. Packet `no_write`, `head_unchanged`, `history_unchanged` are true, and its complete captured `before == after` (including SQL) was verified. Offline positive and every forged-input negative also preserve all inputs. This does not claim a new durable store acceptance/no-write run.

## Validation

Final exact requested command, from this worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:$PWD/packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py
```

PASS: **141 passed in 44.44s**, exit 0, all marks, no baseline failures/skips/xfails. Earlier candidate runs before the last two negative additions passed 139/139 in 45.84s and 44.76s; the first targeted 22 new cases passed in 1.26s.

Unchanged-parent regression: copied runtime_protocol into `/tmp/w-1573be8190/baseline`, replacing its auth module with exact `git show HEAD:runtime_protocol/timeline_commit_auth.py`. From TMPDIR:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-1573be8190/baseline:/home/user/work/wt/rt-R2-native-occurrence-projection-sol-2020:/home/user/work/wt/rt-R2-native-occurrence-projection-sol-2020/packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -c 'import runtime_protocol.timeline_commit_auth as auth; print("AUTH ORIGIN", auth.__file__, flush=True); assert auth.__file__ == "/tmp/w-1573be8190/baseline/runtime_protocol/timeline_commit_auth.py"; import pytest; raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "/home/user/work/wt/rt-R2-native-occurrence-projection-sol-2020/tests/test_timeline_inverse_stage_authentication.py", "-k", "retained_occurrence_order_inverse_preserves_authenticated_physical_pins"]))'
```

Expected RED: **1 failed, 138 deselected in 1.11s**, exit 1, original `inverse stage native writes do not cover its authenticated effect image` at baseline auth line 1373. The regression body is unchanged afterward; two negative cases were subsequently added. Explicit normal pre-import pins the baseline package before pytest prepends the test root; an earlier direct `python -m pytest` overlay attempt resolved the candidate instead and its 1-pass result was discarded as baseline evidence. No module swapping or auth monkeypatch.

```sh
/home/user/work/venv-agent/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
git diff --check
python - <<'PY'
from pathlib import Path
for f in ['runtime_protocol/timeline_commit_auth.py','tests/test_timeline_inverse_stage_authentication.py']:
    compile(Path(f).read_bytes(), f, 'exec')
    print('in-memory compile PASS', f)
PY
```

All PASS, exit 0. Repo pyproject/CI has no Python typechecker configuration; in-memory compilation performed per brief. No full suite, socket/browser/live suite, original c271 body, SDK FOUR, public undo/redo or heavy matrix was run.

## Handoff and next action

No blocker. Independent Luna review next, then Runtime harness commit/integration and Agent's meaningful changed joined body. Public c271/G5/P1 status is not promoted by this offline result. Existing source-only coordinator/ABI behavior outside this projection is unchanged and not requalified here.

Flat durable artifacts (absolute prefix):
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-R2-native-occurrence-projection-2020-`

- `report.md`: this report.
- `source.patch`: entire own source/test/fixture diff, SHA256 `0f521b1eec89179887253bbf13225d36c8264301a85b6e56e404f6b947a4f9ed` (153,283 bytes).
- `custody.json`: original/member/fixture/own source hashes, origins, source publication and no-write facts.
- `tests.txt`: final commands/results and old RED/new GREEN summary.

Decisions: retain physical rows only after the existing authentication succeeds; enforce exact authored permutation rather than add physical pins to Agent captures. This follows PLAN R2/C0c and the verified source boundary. No approval wait, Git mutation or shared dependency write performed.
