# F-D22 read-only integrated proof — 2026-10-23

## Verdict

PASS for the scoped integrated proof. The actual merge is the reviewed one-file
test-fixture change, the integrated tree preserves every other 280e source entry,
the original target passes under the authentic installed profile, and all nine
exact controls pass. No product source, production guard, contract, generated
file, pin, dependency, or test expectation was changed.

The full installed Remotion renderer transaction remains UNQUALIFIED. This proof
does not claim that separate renderer gate, and does not run unrelated
renderer/full/109/113/P1/P4/original-9 suites.

## Merge and preservation proof

Inputs checked:

- merge: 4ff762fda765bfa6c111fe571bed11ced03eae8b
- merge tree: ba657898a27786b10ad2bc20cc759695961e729f
- merge parents: 280e8669f56b41a1023e14219d5fad6eda006260 and
  4faad4bcb952cb71ea437e8441cdfa883dc9044e
- reviewed candidate parent: 63baa707b4bce52b36c06dc3345d2fd357b10f66

Commands:

    git show -s --format=fuller 4ff762fda765bfa6c111fe571bed11ced03eae8b
    git rev-list --parents -n 1 4ff762fda765bfa6c111fe571bed11ced03eae8b
    git diff --name-status 280e8669f56b41a1023e14219d5fad6eda006260 4ff762fda765bfa6c111fe571bed11ced03eae8b
    git ls-tree 4ff762fda765bfa6c111fe571bed11ced03eae8b tests/sdk/test_host_bootstrap_source_identity.py
    git ls-tree 4faad4bcb952cb71ea437e8441cdfa883dc9044e tests/sdk/test_host_bootstrap_source_identity.py
    git diff --check 4faad4bcb952cb71ea437e8441cdfa883dc9044e^ 4faad4bcb952cb71ea437e8441cdfa883dc9044e

Results:

- 280e… to 4ff…: exactly one path changed,
  tests/sdk/test_host_bootstrap_source_identity.py.
- merge/candidate test blob:
  19bbc23c0c3d5843711787f36c1137fda1ade8c5.
- 280e… test blob:
  10cde85f07d19899c0f8cf1605bec0429c3b9485.
- merge, base, and candidate trees each contain 3,418 entries.
- all 3,417 other current tree entries equal 280e… exactly.
- R1/R2 and inverse preservation was explicitly checked:

      astrid/sdk/timeline/commands.py       d349ebd4afc1764fa5db2f464ff234ce6c146b89
      astrid/sdk/timeline/inverse.py        209b6036b1158b1f4ba7ef40a23f1cbcc5831889
      astrid/sdk/timeline/_root_inverse.py  63bbdd9dd6e029eb59dc0d5b35bf172dcdb4f7ee
      astrid/sdk/timeline/_step_undo.py    505fe243fc2188b702245f037dfdabcd3d88ad1a
      astrid/sdk/timeline/commit.py         3f4a86567d053b4a5fa9ec3b44f35ef58e25ef23

  Each current hash equals its 280e… hash.

The reviewed source AST audit was repeated against 280e…: 29 top-level
functions, exactly one changed (the installed-profile identity test), and 28
unchanged. Changed target AST SHA-256 is
c33ddc7780351440d1f2f76ec5bb7502f5755a06a1a363566a95893c9c4242a0 versus base
8c72537c41c2bcb2b20c33439277a0844a22fcd77eab0c2e4d0b6d4a1245df20. The reused
bootstrap/restart helper AST is identical:
9fb0ea89263520058958e950e8c583d88964c041cc124c71ad574698ff831cee.
Assertion inventory is exact: 4 in the target plus 27 in the reused helper = 31
current and 31 base, with exact AST equality for the reused helper.

The one-file merge delta leaves the full C0 contract unchanged by preservation:
request api_version, project/timeline IDs, exact base pair, commands, label,
step id/label/intent/tags/command_ordinals/patch/reads, merge fields|atomic,
declared reads, key, dry_run, source, rationale, and group_id; accepted/merged
canonical and receipt records, bindings, effects, dependencies, history and undo
steps; and preview would_status plus structured error
code/path/head/hint/suggested_command.

## Authentic installed target

The worker-1659 harness was copied unchanged into the pointer-resolved private
tmpdir /tmp/w-8ab12ad843/fd22-integrated-1716. Only TMPDIR and the runner output
path were changed. The worker pointer file was read as a file; it contained
/tmp/w-8ab12ad843.

Profile locks and origins observed by the harness:

    python: /home/user/work/venv-agent-child-d22-8c3b926e/bin/python
    python: 3.13.16
    node: v20.19.4
    runtime commit: 9ce4242bc01f100bab9efc51032a73985cefb2b2
    runtime protocol SHA-256: 4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2
    composition version: 0.0.14
    profile archive SHA-256: 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
    profile lock SHA-256: f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
    installed files measured: 1,507

The isolated -I -c process resolved all three imports from child site-packages:

    astrid                 /home/user/work/venv-agent-child-d22-8c3b926e/lib/python3.13/site-packages/astrid/__init__.py
    runtime_protocol       /home/user/work/venv-agent-child-d22-8c3b926e/lib/python3.13/site-packages/runtime_protocol/__init__.py
    astrid_runtime_client  /home/user/work/venv-agent-child-d22-8c3b926e/lib/python3.13/site-packages/astrid_runtime_client/__init__.py

The test process asserted astrid from this worktree and runtime_protocol from
/home/user/work/wt/rt-pin-9ce4242b. The launch observer recorded the selected
child interpreter, -I -m astrid.core.execution.generic_host, no child
PYTHONPATH, and a test cwd unrelated to the fake source root. It recorded
host_status=ready, three launches, two retired hosts, and inventory reads:
['inventory-1', 'inventory-1', 'inventory-2', 'inventory-2', '', ''].

Exact target command body, with only the copied paths redirected:

    sh /tmp/w-8ab12ad843/fd22-integrated-1716/target-command.sh

Result: PASS, 1 passed in 1.15s, exit 0. The harness recorded custody
before=after, target exit code 0, and the five source hashes below unchanged
through the run.

## Exact nine controls

The copied controls-command.sh retained all nine selectors and the exact
installed environment, including -P -m pytest, -o addopts=, and
-p no:cacheprovider:

    sh /tmp/w-8ab12ad843/fd22-integrated-1716/controls-command.sh

Result: PASS, 9 passed in 1.50s, exit 0. No full suite, browser, live socket,
renderer, 109, 113, P1, P4, or original-9 run was requested.

## Production guard hashes before/after

The target harness custody assertion was true; an independent post-run check
also matched each current hash to 280e…:

    astrid/sdk/host_bootstrap.py                 50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07
    astrid/core/rendering/remotion_runtime.py   84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e
    astrid/core/rendering/_registry_origin.py   47af6b12421f44d943a2c00621fc2b08a3d0f2d29fbd66b3c150a328bed88ca2
    astrid/core/rendering/_effect_registry.py   a6938299241c6b21b8e882d812cf369e143636b40c72f841b547668db711aa85
    astrid/core/source_identity.py              5236481dab209f8803fe9dcd2c93c1610b664bea2102e4370148273ffa4b9a32

Each listed hash was identical before and after the target run and identical to
the 280e… source hash.

## Scoped quality checks

    env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-8ab12ad843/fd22-integrated-1716/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
    # Ruff findings: current=2149 baseline=2149

    env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-8ab12ad843/fd22-integrated-1716/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
    # Mypy findings: current=1912 baseline=1912

    /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
    # ok runtime.lock.json (matches producer manifest)

    /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
    # artifacts.json is current

    git diff --check
    # pass (no output)

All five checks passed. No venv build, manual provisioning, shared dependency write,
generated-file/pin change, source repair, deletion, Git write, merge queue action,
or daemon action was performed.

## Invocation note and limits

The copied command files have no executable bit. Directly invoking the copied
target file returned shell exit 126 (Permission denied) before running any
harness code. I then invoked the same unchanged command body with sh; no harness
body, environment assertion, origin assertion, or selector was changed. This
was a file-mode invocation issue, not a tool/classifier or sandbox permission
denial.

The isolated collaborator's None validation marker is intentional and is the
reviewed unit boundary: the fake source root is not an installed distribution.
The proof covers the real host_bootstrap.ensure_pack_host handoff and the real
installed-registry controls, but does not qualify the full installed Remotion
renderer transaction. Recommended next step is the separately scoped renderer
qualification when that gate is scheduled.

