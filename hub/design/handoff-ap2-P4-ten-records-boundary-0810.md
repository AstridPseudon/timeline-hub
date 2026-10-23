# P4 ten-records boundary handoff

PASS, source-only correction ready for independent review.

Source: Agent worktree `/home/user/work/wt/ap2-P4-ten-records-boundary-0810`.

- Base SHA: `f5ec9ed242c6b84aa35743e9e3741088c3e96a87`
- Base tree: `75070cbab9b35173b0d6d88e7f3ca765f4c64bea`
- Candidate private-index tree: `b42919b24d27675b4da95339608b06147c244261`
- Changed blob: `94069d2cff0d0d479c19128b4e149bb8206855d7`
- Only changed path: `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`

The old `data["commands"] == request["commands"]` comparison crossed the
request/reply authority boundary. Agent execution enriches the authoritative
`records.commands[i].command`; Runtime projects reply `data["commands"]` from
that enriched command. The correction derives a pure expected plan from the
authenticated exact base closure and exact head, compares the reply projection
to the full authoritative record command list, and checks every submitted
field exactly within each nested command. It also compares complete stored
records and steps, retaining captures, effects, bindings, dependencies,
undo-state, and all prior ten-note/closure/history/undo assertions.

Evidence:

- Exact named-node collect-only: 1 collected, exit 0 (known `timeout` config warning).
- Scoped Ruff: PASS.
- Private-cache mypy: PASS, no issues.
- `py_compile`: PASS.
- `git diff --check`: PASS.
- Offline real Agent ten-command projection witness: PASS.
- Offline Runtime claim-auth tamper witness: PASS for every original command
  core field (`schema_version`, `op`, `version`, `select`, `args`).

Limits: no live HTTP/body/socket/service/browser/full-suite run. The named
integration body remains unverified and must be run once by the central test
service/owner after independent review. No product defect was found; no
product path was edited. The worker harness `tmpdir` was a regular file, so
the private mypy cache was placed in a separate `/tmp` directory.
