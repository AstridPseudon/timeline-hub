# P4 ten-note wire source review — FAIL

Reviewed `b4f4ba00e` (`tl/ap2-P4-ten-note-wire-source-0334`). No Agent product
files were changed.

## Blocking finding

The source test's first selected inverse at
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py:233-238` calls
`reloaded.session.undo(..., steps={...})` through a `cast(Any, ...)`. The actual
public `TimelineSession.undo` in the current Agent tree is
`astrid/sdk/timeline/sync.py:408-422` with signature:

```text
(self, publications, *, idempotency_key=None, dry_run=False, via="python")
```

It has no `steps` parameter, and `Timeline` has no alternative per-step undo
method. The cast masks the incompatible call but cannot make the Runtime body
work; execution would fail with an unexpected-keyword `TypeError`. The exact
smallest owner seam is the public `TimelineSession.undo` signature/body, which
must adopt the contract §5 selector and emit it through the existing
`timeline.inverse` path. The test must not add a fake session/provider,
transport shortcut, or direct provider call.

## Review notes

The forward source otherwise uses the original `ten-notes-one-commit` fixture,
ten explicit `doc.patch` commands and ten ordered steps, explicit truthful
`reads=[]` / `merge="fields"`, G3 emission, `Timeline.commit`, the generated
client, and the existing daemon/Runtime HTTP handler. The isolated genesis
adds only an empty `p4_note` parent required by §2's missing-ancestor rule and
compares the non-note parent/closure payload back to the original. No fake
provider/transport, launcher, schema/pin edit, skip, or weakened assertion was
found. The requested body proof remains unverified because of the API blocker;
the held strict-envelope normal adoption plus compatible G3/R2/d106 remain
prerequisites.

## Evidence

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-780da6d6 PYTHONPATH=.:/home/user/work/wt/rt-pin-780da6d6 /home/user/work/venv-app2-native/bin/python -m pytest -q -m integration --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PASS: 1 test collected (exit 0; unknown pytest `timeout` config warning)

/root/.local/bin/ruff check tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PASS

/root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PASS: no issues found

git diff --check
PASS
```

No HTTP/body, socket, browser, full, or heavy suite was run. This is a source
review FAIL and does not claim P4/H3 acceptance.
