# Runtime R2r created-child return handoff

Status: PASS, Runtime-only correction complete.

The Luna1143 failure was classified as a real Runtime defect on a valid current full-v2 public call. The real Agent provider produced authenticated intermediate authoring identities across the sequential created-child boundary. Runtime's projection selected an accepted root by `next(...)` and then demanded a read binding for an identity that the provider had legitimately promoted through the next command. The authentication guard was retained; Runtime now authenticates the promotion through the unique next input binding whose content digest matches the intermediate image, updates the owner and parent edge, and rejects ambiguity or missing provenance.

The correction also requires a unique accepted shot root, exact accepted occurrence ownership, authored payload equality, and an authenticated parent allocation mapping. Existing future-root, before-image, foreign-source, ordering, sharing, omitted-binding, and unchanged-head/history controls remain in force. The focused test adds explicit ambiguous accepted-root and foreign accepted-owner refusals.

Public evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-created-child-return-1151/evidence/public-sequential-acceptance.json`. It contains module origins, actual full-v2 request, prepared records, input source, response/readbacks, effects, bindings, and history. The public witness accepted a real held image (`hold: 2`, `opaque: [null, false]`) through a real Agent provider and RuntimeService; history length was 3 and the final exact canonical readback matched the expected order and sharing.

Verification:

- Required targeted Runtime suite: `239 passed in 60.02s`.
- Ruff on both changed Python files: passed.
- Pyright on both changed Python files: `0 errors, 0 warnings, 0 informations`.
- AST parse and `git diff --check`: passed.
- Frozen edit-command schema digest unchanged at `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.

Only `runtime_protocol/timeline_commit_auth.py` and `tests/test_timeline_commit_authentication.py` changed. No full/browser/live-socket suite was run locally; central integration review should run the handoff against the integration worktrees.
