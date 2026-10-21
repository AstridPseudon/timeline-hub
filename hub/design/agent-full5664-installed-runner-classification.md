# Agent full5664 installed-runner classification

Date: 2026-10-21 UTC

## Decision

The existing full5664 result is an execution of the exact 5c source/child
tuple. It was not run with the old a8 child. Its installed-runner identity is
therefore valid for source/runner attribution, although the suite itself is
red and does not constitute a passing full qualification.

The separately named generated suite
"venv-agent-child-c13-5c5173dc-full" is misbound: its retained command still
uses the a8 interpreter and a8 schema path. I found no request or result
directory for that alias. It must not be treated as an exact-5c installed
run, and there is no installed exact-5c result claim for that alias.

## Original full5664 execution evidence

The authoritative result directory is:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-full-c13-5c5173dc-integration-1021001510-5664

Its retained request says:

    target=integration:agent
    repo=agent
    suite=full-c13-5c5173dc-integration
    files=''
    requested=2026-10-21T00:15:10Z

Its retained snap says:

    tree=8626f868a3869b23baaca9814adb930e8952e4c7
    worktree=/home/user/work/agent

That tree is Agent commit
5c5173dcb57669a9d43e5add2674543333f1c6d2 (verified with git show; its
tree is 8626f868a3869b23baaca9814adb930e8952e4c7). The prior a8 full used
the different source tree b614c4d7036ad8b93517969fc595e9f43c9f8ff4.

The retained summary records the command actually used by the central test
runner:

    env -i HOME=/root LANG=C.UTF-8 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-9d1c43c6" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9d1c43c6 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-c13-5c5173dc/bin/python -m pytest -q -n 3

The execution-time tuple is consequently:

| Input | Retained execution identity |
|---|---|
| Agent source | commit 5c5173dcb57669a9d43e5add2674543333f1c6d2, tree 8626f868a3869b23baaca9814adb930e8952e4c7 |
| Python executable | /home/user/work/venv-agent-child-c13-5c5173dc/bin/python |
| Installed child marker | /home/user/work/venv-agent-child-c13-5c5173dc/.astrid-source-commit = 5c5173dcb57669a9d43e5add2674543333f1c6d2 |
| Installed schema path | /home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages |
| Runtime | immutable checkout /home/user/work/wt/rt-pin-9d1c43c6, commit 9d1c43c647301da48a6e86ad82e466b501bd2418, tree 50e74e3243c5da4cf77b6e6cc76605fae8aeb649 |
| Node | /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node, v20.19.4 |
| Remotion/Composition environment | /home/user/work/runtimes/agent-remotion-0013; public Composition 0.0.13 via its node modules |
| VibeComfy | /home/user/work/fixtures/vibecomfy |

The central run result was 6 failed, 14,884 passed, 452 skipped, 4
xfail, 84 warnings, 565 subtests passed; exit 1; 3,879.05 seconds. The
result scope is exactly that Agent snapshot and this 5c child command. It is
not a result for the moving current integration tip and not a result for the
generated alias.

The runner's PYTHONPATH="$PWD:..." is also material: the test snapshot was
the source checkout at the recorded tree, while the child executable and
installed schema/dependencies were the 5c profile. The result should not be
re-described as a generic source-only run or as proof that every Astrid
module was imported from site-packages.

## Generated-child alias distinction

make-child-venv documents that, when given BASE_SUITE, it substitutes only
the literal venv-agent-child-s2 (and the old Remotion runtime token) when it
appends NAME-full. The provisioning record confirms that
venv-agent-child-c13-5c5173dc itself was built non-editably from 5c:

    created /home/user/work/venv-agent-child-c13-5c5173dc (astrid from 5c5173dcb576, 164 pins, read-only); suite venv-agent-child-c13-5c5173dc-full

However, the generated line retained in tests/suites.conf for the alias is:

    agent venv-agent-child-c13-5c5173dc-full ... ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages ... /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -n 3

Thus the alias name says 5c, but both its interpreter and its schema path say
a8. This is distinct from the direct line:

    agent full-c13-5c5173dc-integration ... ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages ... /home/user/work/venv-agent-child-c13-5c5173dc/bin/python -m pytest -q -n 3

The original full5664 request names the direct
full-c13-5c5173dc-integration suite, and its result summary contains the
direct 5c command above. A scan of all retained test request files found no
request with suite=venv-agent-child-c13-5c5173dc-full, and no result directory
with that alias. Therefore there is no execution evidence that the misbound
alias ran.

The old full-c13-a8a40afd-integration result is separate: its request,
summary, and log all name the a8 child and record Agent tree
b614c4d7036ad8b93517969fc595e9f43c9f8ff4. It is not full5664 and should
remain attributed to the a8 source/runner tuple.

## Wrong-tree precedent and claim boundary

The owner-controlled delivery review at
design/runtime-delivery-final-review.md (the pinned-tip/wrong-branch finding)
records the applicable precedent:
the original tool could report PASS while reading a moving branch rather than
the pinned commit; even a same-tree case was not accepted as proof of the
wrong exported commit. The repair changed counts, expected tree, and bundle
verification to the exact pinned tip, with mismatches failing.

Applying that rule here:

* The generated alias would be an a8-installed execution if it were run. Any
  result from it would be invalid as an exact-5c installed qualification,
  regardless of the alias spelling; it could only be reported under the
  actual a8 runner identity after checking its source tree.
* The actual full5664 result has matching execution evidence: source tree
  8626/commit 5c, Python child 5c, and schema path 5c. It is not invalidated
  by the wrong-tree precedent on runner identity.
* The actual result is still red. "Exact 5c installed identity" means the
  source/runner provenance is exact; it does not turn the 6-failure result
  into a green qualification.

Potentially affected installed-child scope is limited to any tests submitted
under the generated venv-agent-child-c13-5c5173dc-full alias, if such a
request is made later: the whole command would use the old a8 interpreter and
schema. No such result exists in the retained artifacts, so no affected
alias-run result is reclassified here and no exact-5c claim is made for it.

## Checks performed

Read-only inspection only; no test, full suite, cancellation, withdrawal,
source edit, flag edit, test edit, or shared-dependency mutation was
performed. No new test evidence was generated.

