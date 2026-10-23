# FAIL — COMPLETE production caller chain

The committed maker-only patch does not qualify the intended production command.

Evidence:

- Manifest command supplies 8 arguments.
- Actual unchanged requester `/tmp/.../orch/bin/request-runtime` accepts only `2|3|7` arguments at lines 14–17 and rejects 8 with its usage error.
- Unchanged dispatcher would forward the payload to `make-runtime`, but requester rejection prevents reaching it.
- Child2054 owns only `request-child-venv`/`make-child-venv`; it does not repair `request-runtime`.

Minimal gap: extend `request-runtime` to accept and validate the eighth safe absolute `NODE_BIN` argument while preserving 2/3/7 shapes. Recreate the lost TMPDIR fixture to prove requester→dispatcher→maker. No accepted production command can be returned.

Checks:

- `patch --fuzz=0` applied to two private maker copies; `cmp`: PASS.
- Patched maker: 27,925 bytes, SHA-256 `99cc86736e1adea335bbdbcc47b2c352f555c22ce79f73d706e2238128d033a0`.
- `bash -n` patched maker, actual requester, dispatcher: PASS.
- JSON validation and `git diff --check`: PASS.
- Artifact SHA-256: patch `0e6654677ac16c399ee75626c29e230a5b8ac42237a3ab2b290e51d1358ad3c2`; manifest `1d90cf95b3895e80d9e2f5a435ac9203b27e33c89b0ccf86f790380ba8a89204`.
- Author fixture is lost; author-reported fixture PASS is not independently reproducible. Approved Node absence is disclosed as unverified, not treated as a defect.
- No code repair, queue, daemon, build, install, or production call performed. Worktree remains clean.