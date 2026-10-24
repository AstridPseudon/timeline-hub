## READY — P5 D59 cut preflight

Prepared the durable candidate packet: [p5-cut-candidate-packet.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P5-main-bench-1244/p5-cut-candidate-packet.md).

- Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3...`; clean.
- Agent: `/home/user/work/agent`, `cba425b61958f380f25b7bdea83d23c92f627761`, tree `d19ce2e5...`; clean.
- Lock/artifact check: PASS; Agent lock points to current Runtime and producer digest.
- Imports resolved from the actual Runtime and Agent roots; client schema digest matches: `sha256:4118b1e2...`.
- Existing fixture custody verified; no new fixture, package, child environment, realm, or registry work.

Collect-only command:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT="$PWD" \
ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH="$PWD:/home/user/work/agent" \
/home/user/work/venv-runtime/bin/python -m pytest --collect-only -q \
-o addopts= -p no:cacheprovider \
tests/test_timeline_commit_integration.py tests/test_timeline_commit_crash.py
```

Result: **38 tests collected** — 14 integration and 24 crash-boundary nodes. Full named membership plus selector/body/parameter AST hashes are in the packet. Both test files are byte-identical to historical Runtime `62c454ac`; protected predicates remain unchanged.

Static checks:

```sh
git diff --check HEAD
PYTHONPYCACHEPREFIX=/tmp/.../pycache \
  /home/user/work/venv-runtime/bin/python -m py_compile \
  tests/test_timeline_commit_integration.py tests/test_timeline_commit_crash.py
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
```

All passed. No source changes were made; lint/typecheck are N/A.

Deferred central command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
rt-P5-main-bench-1244 marked-integration \
--files "tests/test_timeline_commit_integration.py tests/test_timeline_commit_crash.py") &&
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 45
```

No live service, original body, door, HTTP, full suite, gate, or runtime PASS claim was made. DONE marker and conventional commit message were written.