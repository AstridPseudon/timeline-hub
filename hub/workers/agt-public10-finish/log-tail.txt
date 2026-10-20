The task is blocked, not done. The exact-pair Runtime suite passes and the 0.0.8 tarball is removed. The Node-env node suite is 11 passed, 1 failed, and the failure comes from an environment drift in a shared runtime directory, which I did not change.

**What I did**
- **Tarball:** `git rm remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz` succeeded. Nothing in the tree references 0.0.8 now except the new design doc, which mentions it as history.
- **Design doc:** `design/m2-public10-adoption.md` did not exist in any worktree, so I wrote it fresh. It records the SHAs, digests, test results, and open items.
- **Commit message:** written to `workers/agt-public10-finish/commit-msg`. It has no model names, so I left out the Co-Authored-By trailer from the system reminder, following your rule.
- **BLOCKED:** written to `workers/agt-public10-finish/BLOCKED`.

**Test results** (run through the test service, no full suite requested)

| Suite | Result |
|---|---|
| `bundle1-runtime6be9706-integration` | **pass**, 48 passed in 70.40s, exit 0. Runtime guard confirmed `6be97063`. |
| `remotion-0010-nodes` (5 targets incl. `test_remotion_gate.py`) | **fail**, 1 failed, 11 passed, exit 1 |

The failing node is `TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`. It checks that the runtime `package-lock.json` matches the committed one. In `/home/user/work/runtimes/agent-remotion-0010` it is missing 8 `libc` arrays. Versions, `resolved` and `integrity` all match. That is an npm-version artifact from the install, and the test correctly refuses it. Fixing it means reinstalling that shared directory from the committed lock with npm 10.8.2 and Node 20.19.4. That is outside my scope, so I did not do it, and I did not weaken the test.

**Not verified**
- **Vendor lock script:** the sandbox blocks Python execution, so `scripts/vendor_lock.py check` did not run. I reproduced its checks with `jq`/`sha256sum`: all 17 entries match, and the producer is clean at `6be97063`. Please rerun it in an unrestricted shell.
- **Remotion gate:** `install`/`typecheck`/`parity` did not run. `install` would `npm ci` into my worktree. Its unit tests did pass.
- **Digest `4e52f7df`:** your brief names it, but it is not in the Agent tree or in Runtime `b2a1d9fd`. Agent's client schema digest is `89a396aa…`, which equals Runtime `6be97063`. Runtime `tl/integration` is at `7486348f…`. I left Agent's vendor lock where it is.

**Decisions for you**
- Reinstall `agent-remotion-0010` from its committed lock, then rerun `remotion-0010-nodes`.
- Confirm where `4e52f7df` came from before the Agent lock moves to `b2a1d9fd`.

**Housekeeping:** I could not delete my three scratch files in the scratchpad (`rm` was denied). They are outside the worktree and hold no build output.
