# App2 producer guarded MAIN handoff

Status: HOLD for independent command review. This is a guarded, source-only
handoff; no actual producer test, browser, build, install, socket, daemon, or
service run is authorized here.

## Identity

| Item | Binding |
| --- | --- |
| Repo | App (`app`) |
| Hub branch | `tl/integration` |
| Source commit | `5863411a8c2400db719b5385002b05af0a2b3891` |
| Source tree | `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89` |
| Source parent | `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` |
| Strict baseline (`APP_SHA`) | `17d2518c341c47a2d8634047b400399886da3a2a` |
| Baseline tree | `d63fe4f1e1f32a01acfc9d11cda6c29066fce162` |
| Keeper | `/home/user/work/wt/app-pin-5863411a` (detached, clean, KEEP held) |
| Shared install | `/home/user/work/app/node_modules` (read-only symlink target) |

The approved source delta is exactly these three paths:

```text
scripts/testing/run-producer-public13-list.sh
tests/e2e/local/producer-ownership-current-pin.spec.ts
tests/e2e/local/support/producer-ownership-current-pin.ts
```

Their SHA-256 values are respectively
`329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`,
`6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6`, and
`df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949`.
The config is unchanged and hashes to
`5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
Live callers changed: NONE; this is source/test-only.

## Guard chain and prerequisites

The private, rebound copy of the eight 0945 artifacts is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-new-topology-main-binding-1113/artifacts`

It retains the 0945 final chain’s 51 hash guards, 20 positive path guards,
and one Composition contract-version guard (`0.0.13`). Reverse binding to the
0945 artifact bytes passed. The final source identity is bound in every source,
physical, startup, and custody check; the computed two-link ancestry is
`parent(5863411a8c2400db719b5385002b05af0a2b3891)=b8cc7e1c7` and
`parent(b8cc7e1c7)=17d2518c3`.

The positive chain remains bound to Agent `8130a401bf44a518d5a40ae274d398b8c560be55`
(tree `236c3e57e0265c52b81ba8085de3193026176bff`) and Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree
`7ab412cc4bcbe517efcfa806e092336390312e18`). The locked existing graph is:

```text
graph: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph
archive: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar
archive SHA-256: 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Composition package SHA-256: 7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61
Composition evaluation SHA-256: e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155
```

The existing toolchain prerequisites are the shared App install above, TSX
under the keeper, `/home/user/work/venv-app2-native/bin/python`,
`/opt/pw-browsers`, and at least `10485760` KiB free on the keeper filesystem.
The existing runner allocates only private `npm-cache`, `pw-cache`,
`vite-cache`, browser-output, and short roots under `/tmp/tla-*`; it does not
write the shared install. Failure retention remains the 0945 helper, with new
evidence under the worker’s `evidence/` path. The prior 19080 packet is retained
unchanged.

## Guarded command

After independent review, the one permitted cheap preflight is:

```sh
cd /home/user/work/wt/app-pin-5863411a
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-new-topology-main-binding-1113/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

The expected forwarded list argv is exactly one Playwright file/config:

```text
playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

The existing list assertion is `Total: 1 test in 1 file`. Do not replace the
strict baseline with `HEAD`, do not run `run`, and do not add a new graph,
helper, pin, authority, or runner path.

The retained five-control names are `before`, `after`, `absent-output`,
`copy-failure`, and `success`. Their settled assertions are one custody-shell
dispatch with zero child/build dispatches for `before`; the four-shell order,
one child, and one build-stub dispatch for each other case. These are harness
controls only and do not authorize a browser or actual producer run.

## Evidence and HOLD

Passed before the attempted controls: private data-only rebind with reverse
proof; `python -m py_compile` for the control harness; `sh -n` for all six
shell artifacts; and `node --check` for both probe modules.

The single invocation of the retained 0935 five-control harness stopped in its
`before` fixture before dispatch (`0/5`; no `dispatch.jsonl`). Diagnosis:
the private copy omitted the existing `launch-tool-stub.py`, so the fixture
used system `git` and failed with `fatal: not a git repository`. This is a
harness packaging failure, not a product or guard result. Per the run rule, no
retry was made and the preflight was not started after that first failure.

Manager forwarding is therefore HOLD until an independent reviewer verifies the
exact command, restores the existing stub as a data-only harness prerequisite,
and authorizes one fresh preflight/control attempt. No actual/browser claim is
made.
