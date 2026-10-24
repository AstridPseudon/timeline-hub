# Report

Verdict: **PASS — static cumulative review**. Runtime qualification remains unverified.

Reviewed the plan, prior 0626/0638 reports, whole-path review, current runner/wrapper, managed store, maker verifier, and normal test-service lease path.

Source and row:

- Agent pin: `bb50a43c915ec00c05c5ee34569a040bab8e817c`
- Runtime pin: `f3208b26b53c4d7053e5464eaa7c5e15b1505812`
- Runner SHA: `9e64aab7342ad3005bcd8e634c726920e523470e9787799886da6fbd9d92d4b8`
- Wrapper SHA: `fe48a6a55c02b8cad366353be26b5c074acbb92729174ee84832e63ae6274a35`
- Staged row SHA: `38b2cd712193e7ac6cad90a787971a844f8e606b55cb1634590c1e20c4edad33`
- Target source hashes match expected values.
- 9 assertions, 10 support calls, transition invocation 6, and 45-second watchdog are preserved.

Static checks passed:

```text
python -m py_compile tools/run-discovery-original-0603.py
ruff check --no-cache tools/run-discovery-original-0603.py
ruff format --check tools/run-discovery-original-0603.py
bash -n tools/run-discovery-original-0603.sh
git diff --check HEAD^ HEAD
mypy --follow-imports=skip tools/run-discovery-original-0603.py
```

The normal service statically acquires the managed bench lease before snapshot execution. The runner then verifies the exact registered child, source/client tuple, receipt, maker verifier, RECORD/direct URL metadata, profile lock/archive, Node 20, and resolved peers.

The genuine `bb50/f320` child does not exist yet. The normal maker previously refused at `pinned-requirements` with exit 124. The older `ba8f` child is correctly disqualified. No pytest, preflight, Node, build, install, probe, or original body ran.

Future caller remains the staged row command:

```text
test "$(sha256sum tools/run-discovery-original-0603.sh | cut -c1-64)" = fe48a6a55c02b8cad366353be26b5c074acbb92729174ee84832e63ae6274a35 && env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /bin/bash tools/run-discovery-original-0603.sh run --reviewed-harness-sha256 9e64aab7342ad3005bcd8e634c726920e523470e9787799886da6fbd9d92d4b8 --source-carrier /home/user/work/wt/agt-pin-bb50a43c --runtime-carrier /home/user/work/wt/rt-pin-f3208b26 --candidate-name venv-agent-child-discovery-bb50-f320 --managed-profile /home/user/work/runtimes/agent-remotion-v3-819acf-1110
```

No worktree changes were made by this review. Commit message and `DONE` marker are present.