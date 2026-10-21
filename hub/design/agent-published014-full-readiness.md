# Agent published014 full-environment readiness

Date: 2026-10-21

## Verdict

The published014 environment is sufficiently inventoried for the manager to prepare one exact child environment after the final inventory-source merge, but it is not ready for that full run yet. Do not request the full suite from this preflight.

The two actionable findings are:

1. A suite without the integration Runtime on `PYTHONPATH` fails during collection with `ModuleNotFoundError: runtime_protocol`. The minimal environment correction is `PYTHONPATH="$PWD:/home/user/work/runtime"` together with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`.
2. The current source tree still has five giant-file rationale counts outside the permitted 50-line drift. Refresh those counts after the final inventory merge, then rerun the cheap inventory node before the one full.

No source or shared dependency was changed, and no full, browser, renderer, broad matrix, or installation command was run.

## Exact source and dependency tuple

- Agent source: `091aa23ec83ea05ffd3b0115a640230d51c8c429`; tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.
- Runtime integration checkout: `/home/user/work/runtime`, `be8d254aef249cd421946cbf06ed86d58bc4b307`; tree `6d74348b66ee4a3602cfa4fd56b9b7c0ed7508e0`.
- Installed-client producer lock: Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`. The Agent `runtime.lock.json` and committed `artifacts.json` are unchanged and internally consistent.
- Exact Runtime producer checkout used for the vendor-lock check: `/home/user/work/wt/rt-pin-95bd3c5f`.
- Exact Remotion project: `/home/user/work/runtimes/agent-remotion-published14-091aa23e`, Node `20.19.4`, Remotion `4.0.509`, Composition `0.0.13`, package lock `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
- Remotion Composition artifact: `banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- VibeComfy exact read-only fixture: `/home/user/work/fixtures/vibecomfy`, detached commit `31f90bb03d330283b76e7dbdda51197be787090d`, tree `101744f0d87eebe5ddf6752c10f01f52dc94e3e9`, tracked status clean.

The Remotion external files byte-match the Agent 091 source blobs for `package.json`, `package-lock.json`, and the Composition artifact. Its hidden npm lock has the recorded hash `e207343a5c79a56e70516c493ec837a16bd8451ffad5d51cecbf1dd7abcfede7`; the 46 absent entries are normal hidden-lock representation differences, with no extra or mismatched package entries. The profile has no `.source-commit` or `.astrid-package-lock.sha256` marker, so the byte-identity checks are the source proof used here.

## Cheap evidence

All commands below were run with `PYTHONDONTWRITEBYTECODE=1` and no dependency mutation.

- `python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f`: passed, `ok runtime.lock.json (matches producer manifest)`.
- The same vendor check against `/home/user/work/runtime` refused the expected producer mismatch (`expected 95bd...660f, got be8d...b307`). This is intentional: the installed client artifacts remain the normal Runtime 95 producer while test execution uses the be8d integration checkout.
- `python scripts/artifact_manifest.py --check`: passed, `artifacts.json is current`.
- `git diff --check`: passed.
- Targeted Agent nodes with Runtime and child schema paths configured:

  `python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/astrid_motion/test_astrid_motion_pack.py tests/sdk/test_timeline_revision_diff_admission.py`

  Result: `10 passed in 13.00s`.

- The artifact/structure collection probe with the intended Runtime environment produced `2 passed, 1 failed`. The two artifact/architecture nodes passed. The giant inventory node failed on `astrid/sdk/invocation.py`: rationale `4665`, actual `4716`, delta `+51`.

The current giant-file scan found 36 large files and 36 rationale entries, with no missing or orphan entries. The five entries outside tolerance are:

| File | Rationale | Actual | Delta |
| --- | ---: | ---: | ---: |
| `astrid/core/rendering/remotion_runtime.py` | 1265 | 1387 | +122 |
| `astrid/packs/rendering/rendering/renderers/remotion/run.py` | 1867 | 1796 | -71 |
| `astrid/packs/timeline/cli.py` | 3993 | 4140 | +147 |
| `astrid/sdk/invocation.py` | 4665 | 4716 | +51 |
| `astrid/sdk/timeline_filmstrip.py` | 1251 | 1691 | +440 |

`filmstrip_execution.py` is actual 2065 versus rationale 2015, exactly the permitted `+50`, so it is not a current blocker. These are current source/document inventory findings, not stale relabeling of the older full result.

The same import-origin probe resolved `astrid` and `astrid_runtime_client` from the Agent worktree, `runtime_protocol` from `/home/user/work/runtime`, `banodoco_timeline_schema` from the child c13 site-packages, and `vibecomfy` from the exact fixture when the fixture root was included. This confirms the intended origin split.

The adopted `am-footage` and `am-presenter` descriptors were checked for declared resources: all 6 and 7 declared paths, respectively, exist. A generic project-pack import-closure helper reports the existing type-only import `@banodoco/timeline-composition/evaluation` in each scene as unsupported. This is a validator-boundary mismatch, not treated as a new full-environment blocker: the prior AM-footage qualification covered the built-in pack path and Remotion typecheck, and no source change was made here.

## Child environment for the next full

Do not create or request it during this preflight. After the final inventory merge, build a fresh immutable child from the final Agent commit using the orchestrator’s base freeze:

- Base requirements: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-s2.txt`, 164 lines, SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
- The existing `/home/user/work/venv-agent-child-c13-5c5173dc` is only evidence of the older `5c5173dc` source and must not be reused for the final full.
- Use a fresh name such as `venv-agent-child-published014-<final-agent-short-sha>` and the final merged Agent commit. The name must satisfy `venv-agent-child-*` and must not already exist.
- The child-venv helper’s automatic suite substitution only replaces `venv-agent-child-s2` and `agent-remotion-0012`. Therefore the base suite line must contain both placeholders in the Python executable, schema path, Remotion project path, and Node modules path. It must also contain the Runtime import path, which current reusable full lines omit.

The required base-suite environment additions are:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH="$PWD:/home/user/work/runtime"
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-s2/lib/python3.13/site-packages
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0012
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules
ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
/home/user/work/venv-agent-child-s2/bin/python -m pytest -q -n 3
```

Pass that placeholder-compatible base suite to the child-venv helper with the final Agent SHA and exact Remotion path `agent-remotion-published14-091aa23e`; its substitution will produce the new child schema path and exact Remotion project/module paths. Do not use `published014-integration-nodes` unchanged: it points schema imports at shared `venv-agent`, points Runtime at the producer pin, and is not a full-suite base. Do not use the existing `full-remotion12-s2-integration` unchanged either: it lacks the Runtime `PYTHONPATH` and its project-dir token is not the helper’s substitution placeholder.

## Next steps and limits

1. Merge the final inventory source batch.
2. Refresh only the five out-of-tolerance giant-file rationale counts and rerun the cheap artifact/structure/inventory nodes.
3. Provision the fresh child from the final Agent commit and run the manager’s one exact full with the environment above.

The full suite, browser/renderer paths, live sockets, and the final child environment were not verified in this worker. No assertion was weakened, skipped, deleted, or rewritten.
