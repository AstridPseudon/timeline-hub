# Report — F D141z return

Implemented F2–F6 corrections in private `ops-d141z-build-stop/` only:

- Immutable sampler binding/descriptor custody with append-final `--fd` validation.
- Removed private heavy lock and second dispatch gate; admission remains normal dispatcher-owned.
- Acceptance now exercises `main → D68 wrapper → harmless stub builder`.
- Added early-leader, descendant KILL/reap, cancellation, sampler, signal, and custody controls.
- Deleted only the two tracked `.pyc` files.

Validation passed:

- `bash ops-d141z-build-stop/check.sh` — PASS, exit 0.
- AST parse, private-cache `py_compile`, `bash -n`, Ruff F, `git diff --check` — PASS.

F1 remains explicitly blocked on Runtime-owned runner, inventory, and production wrapper inputs; none were fabricated. No real build, install, service request, full suite, ZIP, or `wait-test` was run.

Evidence artifacts are under the requested worker `evidence/` directory. The initial sampler started after the first read and its PTY close was honestly recorded; a later bounded sampler completed with explicit TERM/wait/reap. `DONE` and commit message were created.