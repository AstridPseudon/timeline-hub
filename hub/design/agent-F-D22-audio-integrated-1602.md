# F-D22 audio integrated proof

Verdict: **PASS**, bounded to the actual home `0ce8da2ab` and exactly the two
original audio fade selectors.

The integrated parent-to-HEAD delta is exactly the reviewed four-file set:
the two audio/docs design files from `e00c38fcf` and the test/fixture blobs
from `8d5a368f7`. Production `astrid` bytes remain exact to base `58316fd6e`;
the frozen normal producer/runtime `34eac004…`, canonical schema `d106…`,
and Composition artifact `819acf…` are unchanged.

Exact approved-profile command:

```text
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-9ce4242b PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider 'tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-in-needs-prepared-envelope-source]' 'tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-out-needs-prepared-envelope-source]'
```

Result: **2 passed in 3.70s**.

Checks: private mypy **1912/1912**; private Ruff **2149/2149**; vendor lock
**PASS**; artifact manifest **PASS**; diff checks **PASS**; source/profile/
body/origin checks **PASS**; start/end HEAD/tree unchanged and worktree clean.

No full/whole-40 claim. No files or shared environments were changed.
