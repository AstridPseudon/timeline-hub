# P4 ten-note provider handoff

## Result

On dependency base `5a313eb88e8ddce1e9e033ed9cfde7ef433f7c55`, the only repo
change is the new test `tests/sdk/test_p4_ten_note_provider.py`.

It executes the collected ten review notes as one ten-command/ten-step commit
through the real Python provider, using the existing emitter for every
sequential bundle transition and the existing detached realm/port. Ten fresh
parameterized runs independently undo each selected step, verify exactly nine
notes remain plus all original mirrors/opaque/null/order/non-note content, and
redo to all ten. The original stored command/step history remains unchanged.
The additional same-note A→B→A later-write case refuses atomically with no
head/history/document mutation.

## Commands

All commands ran from `/home/user/work/wt/ap2-P4-ten-note-provider-0142`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_commit_cases.py
# 13 passed; one existing unknown pytest timeout-option warning
/root/.local/bin/ruff check tests/sdk/test_p4_ten_note_provider.py
# All checks passed
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_ten_note_provider.py
# Success: no issues found
git diff --check
# PASS
```

No full/live/browser/socket run was requested or performed.

## Honest boundary

The test directly exercises the Agent provider called by the production path
`tl.commit` → `Timeline.commit` → session/emitter/provider, but it is not a
public-facade or Runtime integration proof. The detached seam omits official
HTTP `Idempotency-Key`, authenticated Runtime/HTTP IDs and authorization,
`merged` reply spelling, authoritative reply steps/dependencies/merge mode,
history listing, structured invalid code/path/hint/suggested command, and
dry-run preview wire. CLI/sheet/live Runtime/full front-door journeys remain
unverified. No H3 or full P4 completion claim.
