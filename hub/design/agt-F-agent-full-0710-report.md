# F-agent-full-0710 — Agent full-suite classification

**FAIL — collection blocked; not a product PASS.** Consumed only the
authorized `agent-full-1023071006-24096` result via `bin/wait-test`; no
duplicate suite or focused reproduction was run.

Result records:

- Request: `target=integration:agent`, `suite=full`, `files=''`, requested
  `2026-10-23T07:10:06Z`.
- Agent snapshot: commit
  `4edc4b321cae5cfc58252d7ed89e3f0408238646`, tree
  `f17b84c48bae3461dd11cedb8719bd17495a8210`.
- Runtime paired integration: commit
  `a5d4258312c979024865ee704da2d632ca5b2730`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`.
- Both integration worktrees were clean. The transient test snapshot was
  removed by the service after failure; `tests/<id>/snap` preserves its exact
  tree/worktree record.

Exact `wait-test` command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agent-full-1023071006-24096
```

Terminal: exit `4`, `fail`, `2s`. The service command was:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -n 3
```

Counts: `0` executed nodes, `0` passed, `0` failed nodes, `0` skipped, and
`1` collection error. First/only traceback:

```text
ImportError while loading conftest '/home/user/work/wt/.test-agent-full-1023071006-24096/tests/conftest.py'.
tests/conftest.py:24: in <module>
    from astrid.core.pack import source_setup
astrid/core/pack/source_setup.py:22: in <module>
    from astrid.core.foundation.atomic_io import read_json, write_json_atomic
astrid/core/foundation/atomic_io.py:16: in <module>
    from runtime_protocol import platform
ModuleNotFoundError: No module named 'runtime_protocol'
```

Classification: **test-service/environment**, not a demonstrated Agent
regression. The runner sets only `PYTHONPATH=$SNAP`, while Agent collection
eagerly imports Runtime's `runtime_protocol`; the Agent venv has no installed
Runtime package. Existing route repair: invoke the same full command with the
clean paired Runtime checkout on the import path, e.g.
`PYTHONPATH="$PWD:/home/user/work/runtime"`
and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`. No shared dependency,
product, test, schema, pin, or service file was changed here.

The default Agent pytest configuration excludes `integration`,
`darwin_native`, `live`, and `opt_in`; this run therefore cannot credit
Runtime/native/conformance proofs. The D14 two equal-text anchor-undo tests
and unmerged H9/V4 tests remain unchanged visible failures/open scope; they
were not reached due to collection and are not relabeled. Existing focused
proof in `design/agt-V2-child-integrated-0658.md` is reused without rerun.

Recommended next step: test-service owner repairs the paired Runtime import
environment and the orchestrator authorizes one replacement full run.
