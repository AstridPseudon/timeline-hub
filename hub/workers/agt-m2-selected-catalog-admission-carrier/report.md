Completed and marked `DONE`.

- Published the carrier trace: [agent-selected-catalog-normal-carrier.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-selected-catalog-normal-carrier.md)
- Sent peer response to App2/Runtime inboxes and flat note.
- Recorded exact `admit_project_pack`, CLI, `DocumentPin`, CAS snapshot, and generated retained-read signatures.
- Result: normal project-pack carrier **PASS**; hosted/system-pack `8e3a…` remains concretely **BLOCKED** without a full owner/revision/pin.
- Test:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-agent/bin/python -m pytest -q -rs \
  -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_params_reads_only_the_exact_selected_object
```

`1 passed in 2.35s`.

`git diff --check` passed; no product files changed. Report and commit metadata are in the worker directory.