# U4a D141 receiving review validation

## PASS

The final Agent worktree contains only the intended lock delta versus baseline
8585ed9c0404d0187b2ce70242d25114a32747c2. The required cleanup was verified
against exact Git bytes and modes.

## Commands and results

| Command | Result |
|---|---|
| /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime | PASS, exit 0 |
| /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check | PASS, exit 0 |
| PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-rt-U4a-D141-host-receiving-review-0549 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o cache_dir=/tmp/w-rt-U4a-D141-host-receiving-review-0549/cache --basetemp=/tmp/w-rt-U4a-D141-host-receiving-review-0549/basetemp tests/test_vendor_lock.py tests/test_artifact_manifest.py | PASS, 24 passed in 5.20s |
| Python AST parse of scripts/refresh_runtime_client.py, scripts/vendor_lock.py, scripts/artifact_manifest.py, tests/test_vendor_lock.py, and tests/test_artifact_manifest.py | PASS, 5 files |
| /home/user/work/venv-agent/bin/ruff check scripts/refresh_runtime_client.py scripts/vendor_lock.py scripts/artifact_manifest.py tests/test_vendor_lock.py tests/test_artifact_manifest.py | PASS, all checks passed |
| git diff --check | PASS, exit 0 |

The first pytest invocation lacked the Runtime source on PYTHONPATH and
failed collection with ModuleNotFoundError: runtime_protocol; it was
rerun with the corrected private temp/cache paths and passed. The assigned
harness tmpdir path was a regular file, so no files were placed there.

## Independent mechanical checks

- Runtime producer HEAD/tree: 95d98f038320d5d46bd679ac000ab3e15825c935 /
  78df31d62c5b9ba4c84dee4ea346e43a767718c1.
- Runtime clean before/after: PASS.
- Runtime manifest bytes equal committed HEAD: PASS.
- Runtime contract/artifacts.json unchanged from 6a to 95: PASS.
- 15/15 consumer payloads equal baseline, final Runtime source, and independent
  0513 corrected map: PASS.
- 15/15 mode checks: worktree 0644 permission bits equal Git 100644;
  producer source modes 100644: PASS.
- Existing generated-client-to-commitTimeline binding unchanged: PASS.
- Final git diff 8585...HEAD names only runtime.lock.json: PASS.

No full/core/P4/P5/browser/live-service suite was run, per task scope.
TypeScript typecheck is not applicable to this lock-only Python-tool
provenance change.

