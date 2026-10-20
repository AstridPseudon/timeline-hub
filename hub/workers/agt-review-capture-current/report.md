**APPROVE the bounded Agent port** `92427b3af0bfaba2ff604791cf3e5165125b6d54`, tree `525bdabe863a42bc177f5ff331560133f77ce634`.

The pure hook, full saved graph/output preservation and host handoff match the approved design. No product edits. Review written to `design/agent-review-capture-current.md`; detailed report, commit message and `DONE` completed.

Exact source checks:

```bash
git rev-parse HEAD HEAD^{tree}
git diff 92427b3a^ 92427b3a -- astrid/core/execution/generic_host.py astrid/core/rendering/verified_source.py astrid/sdk/timeline/commit.py astrid/sdk/timeline_filmstrip.py
git diff --check
```

Confirmed reviewed host-file equality, unchanged `project_capture`, preserved public12/Runtime pins and clean diff checks.

Exact independent tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_capture_projection.py tests/packs/rendering/test_verified_source.py tests/sdk/test_timeline_filmstrip.py tests/core/execution/test_generic_host_contract.py -m 'not integration'
# 143 passed, 9 deselected; exit 0.

ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_capture_projection.py
# 9 passed, 34 deselected; exit 0. Fixture archives Runtime 4bb1d0f7.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_capture_closure_source.py -k 'not sdk_capture_reference_admission'
# 23 passed, 2 deselected, 3 strict xfailed; exit 0.

ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0012 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py
# 59 passed; exit 0.
```

Keep the duplicate verifier until Runtime’s corrected exact-source pair passes, including the 09:58 negatives. Four renderer propagation requirements and three SDK guards remain unmet. Existing central evidence has 23 capture passes/four renderer xfails, plus two expected client/schema handshake failures. No full suite or duplicate Runtime 20-case run was requested; certification and release gates remain open.