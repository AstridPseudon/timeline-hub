Implemented the bounded Runtime producer and launch custody. **Agent joining remains outstanding; external launches fail closed without its consumer hook.**

Owner-only private state now authorizes the exact repository, checkout, revision, subpath, tree, inventory and selected definitions. Runtime captures source bytes, rejects aliases/collisions, and rechecks materialization through existing one-use launch custody. Production preparation obtains admission before opening child transport.

Private interface:

```python
_write_owner_grants(service, grants, *, identity)
OwnerSourceCapture(*, preparation, config)

# Agent-owned hook, invoked before _cli()/discovery:
generic_host._consume_runtime_external_sources(*, sources)

sources.inventory() -> bytes
sources.select(
    *, scope, selected_profile_digest, root, definition
) -> bytes
```

The canonical payload contains `scope` (`operation_id`, `channel_id`, `owner_epoch`, `custody_scope`), `selected_profile_digest`, and `sources`. Each source carries repository/revision/subpath/tree/root, file pins, selected definitions, base64 captured contents, materialization identities and ancestor identities.

Validation:

- Direct final run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --basetemp="$TMPDIR/source-tests-type-final" tests/test_external_pack_sources.py
  ```

  **38 passed.**

- Central service final run:

  ```bash
  /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_external_pack_sources.py tests/test_verified_host_launch.py tests/test_local_execution_supervisor.py tests/test_local_worker_composition.py tests/test_local_worker.py
  ```

  **317 passed, 2 deselected**, request `rt-R2r-D40-source-admission-sol-0219-targeted-1024023208-4861`, tree `31ae1bdfc5025a4fcbfce08409554a5cae2fdcc8`.

- Ruff: parent/final **32/32** diagnostics; Pyright: **55/55**. Zero new normalized identities against `45c3a7f47`.
- `/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` and `git diff --check`: **passed**.

The production test exposed an existing owner-identity projection error. I projected native observations to the required `pid`/`uid`/`birth_id` fields plus Runtime epochs, preserving the exact-field guard.

C0v2, schemas, clients and pins are unchanged. Agent guards and attack bodies were untouched and not rerun. No full suite or installed-host positive qualification ran.

Next: review this producer, then implement the Agent hook and captured-byte consumption through its existing execution path. No joined acceptance is claimed.

Required `commit-msg` and empty `DONE` were written.