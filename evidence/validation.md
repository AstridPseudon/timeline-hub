# U4a D141 post-REG normal producer receiving

Status: `PASS_SOURCE_TOOLS`

The Agent candidate is `8585ed9c0404d0187b2ce70242d25114a32747c2` / tree
`92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`. The normal Runtime producer was
clean before and after adoption at `95d98f038320d5d46bd679ac000ab3e15825c935`
/ tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, with parents
`857e4c3bce8fd7fc862d7e6e5831e63f24e8cce5` and
`012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`.

The documented refresh route changed only the `runtime.lock.json` source
provenance from Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` to the
qualified normal producer. All 15 mapped consumer payloads stayed byte-identical
to the pre-adoption Agent tree, the final producer, and the independent 0513
producer-corrected map. No source, schema, generated payload, test, fixture,
manifest, or production caller was changed.

## Commands and results

| Command | Result |
|---|---|
| `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/runtime` | PASS, exit 0; refreshed from `95d98f038320` |
| `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime` | PASS, exit 0 |
| `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` | PASS, exit 0 |
| `TMPDIR=/tmp/w-2a352de4ce/rt-U4a-D141-postREG-host-0544/tmp XDG_CACHE_HOME=/tmp/w-2a352de4ce/rt-U4a-D141-postREG-host-0544/cache PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --basetemp=/tmp/w-2a352de4ce/rt-U4a-D141-postREG-host-0544/basetemp tests/test_vendor_lock.py tests/test_artifact_manifest.py` | PASS, `24 passed in 5.09s` |
| AST parse of the three vendor tools and two targeted test files | PASS, 5 files |
| `ruff check scripts/refresh_runtime_client.py scripts/vendor_lock.py scripts/artifact_manifest.py tests/test_vendor_lock.py tests/test_artifact_manifest.py` | PASS, all checks passed |
| `git diff --check` | PASS |

The first direct pytest collection lacked the required shared Runtime source on
`PYTHONPATH`; the corrected documented environment above passed. No full suite,
browser, live service, TypeScript typecheck, or release verification was run.
TypeScript typecheck is not applicable to this lock-only Python-tool provenance
change.

## Conservation

The product diff is exactly one line in `runtime.lock.json`; the four required
evidence files are the only additional task outputs. The Runtime producer stayed
clean. The lock has 15 entries, producer version
`sha256:084f3f2510edff28c18d33aac4a459f8aa6df3cb4fd71cba4fb292274ea8ade5`, and
all mapped hashes are recorded in `source-manifest.json`.

This is a source/provenance adoption result only. It does not claim product
proof, full-suite GO, release readiness, or a change to the C0 request/reply
contract or the existing generated-client-to-`commitTimeline` binding.
