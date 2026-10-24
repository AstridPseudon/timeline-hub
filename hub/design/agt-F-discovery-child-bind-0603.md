Implemented [tools/run-discovery-original-0603.py](/home/user/work/wt/agt-F-discovery-child-bind-0603/tools/run-discovery-original-0603.py).

- Fail-closed bb50/f320 harness; no fallback to 3b5c.
- Binds installed origins, RECORD/direct URLs, client identity, Remotion profile/archive, discovery and original-body hashes.
- Preserves dropped `ASTRID_HOST_EXECUTION_PROFILE`.
- Produces durable before/after evidence and runs the exact production caller only after preflight.

Exact suite row:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
```

Checks passed:

```text
python3 -m py_compile tools/run-discovery-original-0603.py
ruff check --no-cache tools/run-discovery-original-0603.py
ruff format --check --no-cache tools/run-discovery-original-0603.py
git diff --check
```

Preflight was intentionally blocked: exit 2 because the required child receipt is absent; normal provisioning previously refused at `pinned-requirements` rc124. No original test, ten-probe run, render, or test-service request was made.

Hashes:

- Runner: `d92fdb1daca1a025b8ea72bfcc1a39c17cadc5e94ff00706438e950be145f889`
- Discovery source: `40ae7c5945529bb65dbeb3853a80b1b03650e7dcc5f4a60ddaa04c4dc9f37999`
- Discovery test: `9faabadd340c1b2df04f0ab6e83c9d00ac1e6f9cf68fd2f8ed2b81af7e108e5f`
- Original body: 9 assertions, 10 support calls, transition invocation 6.

Commit message and `DONE` marker were created.