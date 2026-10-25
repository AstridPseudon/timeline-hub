Implemented and completed F-D86 NEW13 proof.

- Ran one central D73 body: `rt-D86-new13-body-0611-fd86-new13-body-0611-1025061304-17724`
- Exact 13 selectors, pinned tuple, source hashes, profile/import preflight passed.
- Controls: positive exit 17 once; poison body invocation zero; body invoked once.
- Result: 4 failures, 9 errors; no safety/permission/classifier refusal observed. No semantic verdict assigned.
- Registry restored byte-for-byte; Runtime worktree remains clean.
- Evidence and safe summaries stored privately under the worker evidence directory (~1 MB).
- Wrote commit message and created `DONE`.
- No local pytest/full suite run; central service was used as required.