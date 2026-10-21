# Parent/selected single-lock registration correction

## Result

The smallest correction is identified and intentionally unapplied. Remove only the outer
flock -n /home/user/work/.app-m1-browser.lock prefix from the parent registration
command. The existing inner flock -w 600 in the owned runner remains the sole actual
browser-stage owner. No App source, runner body, timeout, guard, pin, build prefix,
assertion, retention, or environment value was changed.

No browser, build, package install, IPC, socket, central test-service, or actual was
run or registered.

## Exact one-line registration delta

Old command, extracted from the retained 590 registration log:

    flock -n /home/user/work/.app-m1-browser.lock env -i HOME=/tmp/tl-pv-parent-1145-central/home LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/bin:/bin TMPDIR=/tmp/tl-pv-parent-1145-central/tmp XDG_RUNTIME_DIR=/tmp/tl-pv-parent-1145-central/xdg NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE=/home/user/work/venv-app2-native/bin/python NORMAL014_LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph NORMAL014_LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar APP_ROOT=/home/user/work/wt/app-pin-6707a30f NORMAL014_RECORD_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/evidence-central-corrected NORMAL014_RUN_ROOT_PARENT=/tmp/tl-pv-parent-1145-central PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/artifacts/final-keeper-gate.base.sh run

Proposed new command, review-ready but not executed:

    env -i HOME=/tmp/tl-pv-parent-1145-central/home LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/bin:/bin TMPDIR=/tmp/tl-pv-parent-1145-central/tmp XDG_RUNTIME_DIR=/tmp/tl-pv-parent-1145-central/xdg NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE=/home/user/work/venv-app2-native/bin/python NORMAL014_LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph NORMAL014_LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar APP_ROOT=/home/user/work/wt/app-pin-6707a30f NORMAL014_RECORD_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/evidence-central-corrected NORMAL014_RUN_ROOT_PARENT=/tmp/tl-pv-parent-1145-central PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/artifacts/final-keeper-gate.base.sh run

One-line diff: delete exactly the leading
flock -n /home/user/work/.app-m1-browser.lock and retain the rest byte-for-byte.
Reverse diff: restore that same leading prefix.

Command hashes, including the terminating newline:
- old: b5034575c1c949a241b520732060572800a89aae71d7cab0098cd9a99f459834
- proposed: c015cd2beb8c8615e36ff630cd4a737b81b0491aef1a063eca612ddd3fb1acad

## Lock topology

Parent590's retained actual command acquired the shared lock externally with flock -n,
then ran the gate. The owned parent runner reaches
normal014-app-central.bound.sh:160-161:

    flock -w 600 /home/user/work/.app-m1-browser.lock \
      node node_modules/playwright/cli.js test "$@"

The parent held the lock while its child attempted the same lock. The child was never
launched; status 1 was the inner lock timeout, not a Playwright or product result.

Selected1206 was stopped before registration. Its retained runner has:
- selected-runner-6416-source.sh:476-477: nonblocking preflight probe only;
- selected-runner-6416-source.sh:715: existing flock -w 600 around the browser child;
- selected-p1-driver.sh:171-172: legacy selected driver has the same single inner owner.

The preflight probe returns before build/body execution. Selected therefore has the same
topology if registered with the old outer prefix, and needs the same minimal correction.
Selected runner hashes retained unchanged: source 6416f65db7b8f247bd8610b504435c8a18c4139ded1b8bbcf4fc7ae3da83e5ed;
previously prepared 8 GiB build-prefix variant 8cd735c4d8322b588fade70ebbf6d64ca6af811ed50347e9442cf62a63a4ca43.

## Packet paths and controls

- Parent590 packet:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/evidence-central-corrected/run/
- Parent590 result:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590/
- Selected1206 retained WIP, with no actual packet:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-corrected-seed-one-central-1206/record/
  source manifest: record/sourceHASH-manifest.txt
- Frozen old1384 evidence, untouched:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-exact-one-central-1126/record/

Known short-lived roots:
- /tmp/tl-pv-parent-1145-central/source-run.XXXXXX and tmp.XXXXXX
- /tmp or TMPDIR/ap2-m2-selected-final95-owned.XXXXXX
- /tmp or TMPDIR/ap2-m2-selected-p1.XXXXXX
- /tmp/ap2-m2-selected-clean-keeper-main-port-1120-central-trace
Runtime data, realm data, caches, browser output, and child socket paths are below the
owned run root; none were created by this worker.

Preserved controls include exact App source/tree and selected contract, Agent
6efc81500a0e0688c2bb41e736503f0fc3e04abb, Runtime
95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c, locked graph archive SHA
895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30, Composition
tarball SHA 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738,
Node v22.22.0, Vite 5.4.21, Vitest 4.1.5, Playwright 1.60.0, the 8 GiB
build prefix, exact argv/list1, zero-test refusal, credential/origin checks,
source/graph guards, retention ordering, and original assertions. Actual lock
timeout remains 600 seconds.

## Offline real-flock proof

Exact proof invocation was a bash stdin script using a private
/tmp/timeline-single-lock-proof.XXXXXX lockfile. It:
1. ran flock -w 2 around a child that marked ownership, slept, and exited 37;
2. attempted a competing flock -n child and asserted it could not enter;
3. asserted flock -n preflight refused while busy and accepted after release;
4. ran the old double acquisition under timeout 2s with inner test-only timeout 0.20s.

Result:

    exclusive-owner=PASS child-failure-propagation=PASS competing-process=REFUSED nonblocking-preflight=REFUSED-THEN-ACCEPTED
    old-double-acquisition=TIMEOUT-AND-FAIL rc=1 test_timeout=0.20s elapsed_ms=209 actual_timeout_unchanged=600s

This proves one owner inside the child, competing-process refusal, nonblocking
preflight refusal then acceptance, and fast old-double-acquisition failure. The
production 600-second timeout was not changed or exercised.

## Verification and gate

- git status --short --branch -> clean App worktree on
  tl/ap2-m2-parent-selected-single-lock-source-1209.
- No App source, docs, or .gitignore files were changed.
- Read-only rg, nl, sha256sum, and diff -u -> confirmed the lock topology and
  one-prefix delta.
- Private offline flock proof -> passed.
- No App test suite was run because the scope forbids build/browser/actual/full/
  test-service execution.
- Independent Luna review remains required before any actual registration. The
  proposed command is review-ready but was not executed.
- Parent590, old1384, and selected1206 retained artifacts remain untouched.

## Minimal recommendation

After independent review, register the proposed command exactly once with the existing
runner and guards. Do not add a second lock, change 600, alter runner body, or change
source/geometry/fixture data.
