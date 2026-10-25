# Portable whole-maker fixture validation

Source correction is complete; the genuine whole-maker body remains reserved
for the Agent receiving service after independent review and target
`--check-only`. The current machine has `4,990,287,872` bytes free, below the
unchanged `5,905,580,032` start reserve and above the unchanged 4GB stop line,
so no body was attempted.

Passed commands:

```text
PYTHONPYCACHEPREFIX=/tmp/.../pycache /usr/bin/python3.13 -m py_compile ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/support.py  PASS
bash -n ops-child-custody/e2e-fixtures/tiny/makers/{parent-0857,candidate-c3226b}/make-child-venv  PASS
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/support.py  PASS
/home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -v  PASS (40/40)
git diff --check  PASS
offline --no-isolation dependency wheel build with venv-agent  PASS; 1142/1136 bytes and pinned hashes exact
df parser positive and malformed/multiple/negative controls  PASS
parent/candidate maker hashes and STORE_VERIFY block equality  PASS
```

The negative check-only invocation used fresh `/tmp` paths, exited `2`, listed
all simultaneous missing helper/bootstrap/wheel/source/interpreter/reserve inputs, and
left orchestration, parent, and candidate roots absent. It reported
`mutating_setup_started=false`, `git_mutated=false`, `store_initialized=false`,
and `maker_started=false`.

No full suite, socket/browser test, package acquisition, venv creation,
production Store/request, or genuine parent/candidate maker run was performed.
The prior service27653 parent failure is consumed as the missing private
`tests/suites.conf` baseline; its stdout/stderr remain EXACTMISSING and were
not reconstructed.
