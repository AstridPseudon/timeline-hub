# G5 guidance return

## Result

Updated only `astrid/packs/timeline/cli.py` user-facing guidance strings. The
three stale publish instructions identified by the independent 1137 review now
point at the supported `timelines apply <ref> --project <project> <sheet-file>`
entrypoint, while preserving the existing project, timeline/ref, and file-path
context. The workflow and navigation command-map key are `apply`.

No control flow, provider, writer, local merger, tests, pins, or contracts were
changed.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-guidance-return-1145 tests/sdk/test_scene_save_core.py`
  - **16 passed** in 3.92s.
- Direct parser smoke using `cli.build_parser(None)` and `shlex.split` for the
  navigation command and `_cmd_edit` follow-up form:
  - **passed**; both preserve `project-17`, `timeline-main`, and the supplied
    path (`/tmp/timeline-edit.json` or `<sheet-file>`).
- `git diff --check`
  - **passed**.
- `RUFF_CACHE_DIR=/tmp/agt-G5-guidance-return-1145-ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/timeline/cli.py`
  - Reports **15 pre-existing diagnostics** in this file, matching the review
    baseline; none are on the changed guidance lines.

No full, browser, socket, HTTP, native, or integration suite was requested or
run.

## Decisions and limits

- Used the existing `apply` parser because it is the supported ref/project/file
  entrypoint and parses the exact preserved context. No new flags or command
  route were introduced.
- Left ordinary `publication`/`published` terminology untouched; only
  executable stale guidance was changed.
- The detached checkout remains a guidance/migration context. This change does
  not alter its implementation or broaden the writer path.

## Next step

The orchestrator can review/merge this bounded guidance-only change after its
normal queue checks. The broader G5 deletion remains subject to the settled P1
gate and the other owners' publisher/local-merger/test-import work.
