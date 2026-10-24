## F-ABA service whole-path report

Result: the failed service run did not execute the ABA test body. It failed during pytest conftest import because the explicit Runtime `PYTHONPATH` was scoped only to the preflight command.

Evidence:

- Service run: `agt-F-final-source-join-0816-authoring-current-becfe-nodes-1024083505-26998`
- Status: `fail`
- Exit: `4`
- Request: one exact selector, `test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
- Preflight passed Agent/Runtime origins, Runtime auth blob, auth-file hash, tree pins, Node, profile, and fixture guards.
- Pytest then failed at `tests/conftest.py:24` → `source_setup.py:22` → `atomic_io.py:16` with `ModuleNotFoundError: No module named 'runtime_protocol'`.
- `runner.log` was empty; `log.txt` contains only preflight output and the import failure.
- The original test file is byte-identical to target `0c2c28da`; the target test blob is `e55be12f…`, with 59 AST `assert` nodes. No original assertions changed.

Whole-path finding:

- `test-run:15` parses the registered row with `awk`.
- `test-run:17` appends the requested file selector to the command.
- `test-run:201/205` launches the command with outer `PYTHONPATH=$SNAP`.
- The failed row then runs:

  `cd pinned-source && env -i ... PYTHONPATH=agent:runtime ... preflight && pytest`

  `env -i` applies only to the preflight child. The following pytest inherits the outer snapshot-only `PYTHONPATH`, not the explicit Runtime path. Thus the single-file suffix is correct, but the pytest environment is not.

The known `authoring-current8ea-nodes` row keeps pytest inside the same `env -i` command and does not have this boundary.

Pin distinction:

- Actual service target was the fixed Agent worker at `0c2c28da`, tree `4ce9de…`; it was not this artifact branch (`bd635de`, tree `f12bb4…`).
- The row guards Runtime `becfe6db` / auth blob `979225ab`.
- The unchanged test body explicitly sets `ASTRID_RUNTIME_CHECKOUT` to `rt-pin-8ea0766f` at line 719 before `use_runtime()`.
- Therefore the row’s preflight auth pin and the test body’s eventual Runtime pin are not identical. The body never ran, so this is a static parity gap requiring owner resolution before another body run.

Checks performed:

- Read-only source and artifact inspection.
- Python `shlex` registry/argv analysis.
- AST assertion and source-byte comparison.
- `bash -n` on the candidate row and `test-run`.
- No product edits, test-body rerun, realm, browser, network, full suite, or new preflight were performed.

Recommendation: Existing Sol repair should keep the preflight and pytest under one explicit environment boundary, then resolve whether this ABA case is intentionally pinned to 8ea or should use becfe. No product repair was authored here.